import scrapy
from scrapy.http import FormRequest
from ..utils.auth_utils import get_credentials, is_logged_in
from pyairtable import Api
import os

class BaseAuthenticatedSpider(scrapy.Spider):
    name = 'base_spider'
    """Base spider that handles authentication for all child spiders"""
    login_url = 'https://sped.fusionpl.us/login/'
    dashboard_url = 'https://sped.fusionpl.us/dashboard/'
    
    def __init__(self, *args, **kwargs):
        super(BaseAuthenticatedSpider, self).__init__(*args, **kwargs)
        credentials = get_credentials()
        self.username = credentials['username']
        self.password = credentials['password']
        
        # Initialize Airtable connection
        self.airtable_api_key = os.getenv('AIRTABLE_API_KEY')
        self.base_id = os.getenv('AIRTABLE_BASE_ID')
        self.table_name = os.getenv('AIRTABLE_TABLE_NAME')
        
        if not all([self.airtable_api_key, self.base_id, self.table_name]):
            raise ValueError("Missing required Airtable environment variables")
            
        self.airtable = Api(self.airtable_api_key).table(self.base_id, self.table_name)

    def start_requests(self):
        """Start by checking if we're already logged in"""
        yield scrapy.Request(
            url=self.dashboard_url,
            callback=self.check_auth_status,
            dont_filter=True,
            meta={'handle_httpstatus_list': [302, 401, 403]}  # Handle redirects and auth errors
        )
    
    def check_auth_status(self, response):
        """Check if we're already authenticated"""
        if is_logged_in(response):
            self.logger.info("Already logged in, proceeding with scrape")
            yield from self.authenticated_requests()
        else:
            self.logger.info("Need to log in first")
            # Otherwise, go to login page
            yield scrapy.Request(
                url=self.login_url,
                callback=self.parse_login_page,
            )
    
    def parse_login_page(self, response):
        """Parse the login page and submit credentials"""
        self.logger.info("Submitting login form")
        
        yield FormRequest.from_response(
            response,
            formdata={
                'username': self.username,
                'password': self.password,
            },
            callback=self.after_login
        )
    
    def after_login(self, response):
        """Handle post-login actions"""
        if is_logged_in(response):
            self.logger.info("Login successful")
            yield from self.authenticated_requests()
        else:
            self.logger.error("Login failed")
    
    def authenticated_requests(self):
        """
        This method should be implemented by child spiders
        to start their specific scraping tasks after authentication
        """
        raise NotImplementedError("Subclasses must implement authenticated_requests()")

    def send_to_airtable(self, data):
        """
        Send scraped data to Airtable
        Args:
            data (dict): Dictionary containing student data to be inserted
        Returns:
            dict: Response from Airtable
        """
        try:
            response = self.airtable.create(data)
            self.logger.info(f"Successfully sent data to Airtable: {response['id']}")
            return response
        except Exception as e:
            self.logger.error(f"Failed to send data to Airtable: {str(e)}")
            raise
