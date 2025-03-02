import scrapy
from .base_spider import BaseAuthenticatedSpider
from ..items import CavaItem
from scrapy.exceptions import CloseSpider

import re
import json

class MergedSpider(BaseAuthenticatedSpider):
    name = 'merged'
    custom_settings = {
        'ITEM_PIPELINES': {
            'cavaspider.pipelines.AirtablePipeline': 301,
        }
    }

    def __init__(self, student_id=None, *args, **kwargs):
        super(MergedSpider, self).__init__(*args, **kwargs)
        self.student_id = student_id
        
    @staticmethod
    def get_isas_endpoint(display_start=10, display_length=10, search_term=None):   
        base_url = 'https://sped.fusionpl.us/isas/_retrieve_server_data/-1/-1'       
        params = {
            'sEcho': 1,
            'iColumns': 12,
            'sColumns': '',
            'iDisplayStart': display_start,
            'iDisplayLength': display_length,
            'mDataProp_0': 0,
            'mDataProp_1': 1,
            'mDataProp_2': 2,
            'mDataProp_3': 3,
            'mDataProp_4': 4,
            'mDataProp_5': 5,
            'mDataProp_6': 6,
            'mDataProp_7': 7,
            'mDataProp_8': 8,
            'mDataProp_9': 9,
            'mDataProp_10': 10,
            'mDataProp_11': 11,
            'sSearch': search_term if search_term else '',
            'bRegex': 'false',
            'sSearch_0': '',
            'bRegex_0': 'false',
            'bSearchable_0': 'true',
            'sSearch_1': '',
            'bRegex_1': 'false',
            'bSearchable_1': 'true',
            'sSearch_2': '',
            'bRegex_2': 'false',
            'bSearchable_2': 'true',
            'sSearch_3': '',
            'bRegex_3': 'false',
            'bSearchable_3': 'true',
            'sSearch_4': '',
            'bRegex_4': 'false',
            'bSearchable_4': 'true',
            'sSearch_5': '',
            'bRegex_5': 'false',
            'bSearchable_5': 'true',
            'sSearch_6': '',
            'bRegex_6': 'false',
            'bSearchable_6': 'true',
            'sSearch_7': '',
            'bRegex_7': 'false',
            'bSearchable_7': 'true',
            'sSearch_8': '',
            'bRegex_8': 'false',
            'bSearchable_8': 'true',
            'sSearch_9': '',
            'bRegex_9': 'false',
            'bSearchable_9': 'true',
            'sSearch_10': '',
            'bRegex_10': 'false',
            'bSearchable_10': 'true',
            'sSearch_11': '',
            'bRegex_11': 'false',
            'bSearchable_11': 'true',
            'iSortCol_0': 0,
            'sSortDir_0': 'asc',
            'iSortingCols': 1,
            'bSortable_0': 'true',
            'bSortable_1': 'true',
            'bSortable_2': 'true',
            'bSortable_3': 'true',
            'bSortable_4': 'true',
            'bSortable_5': 'true',
            'bSortable_6': 'true',
            'bSortable_7': 'true',
            'bSortable_8': 'true',
            'bSortable_9': 'true',
            'bSortable_10': 'true',
            'bSortable_11': 'true'
        }
         
        import urllib.parse
        query_string = urllib.parse.urlencode(params)
        return f"{base_url}?{query_string}"

    @staticmethod
    def update_isa(isa_id):
        url = f'https://sped.fusionpl.us/isas/isa/{isa_id}'
        data = {
            "id": isa_id,
            "name": "Laila Windemuth", 
            "title": "Psych Lead"
        }
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
        return {
            'url': url,
            'method': 'PUT',
            'data': data,
            'headers': headers
        }
    
    def authenticated_requests(self):
        """Start the scraping process after authentication"""
        if self.student_id:
            # If student_id is provided, go directly to student details
            self.logger.info(f"Starting to scrape student data for ID: {self.student_id}")
            url = f'https://sped.fusionpl.us/students/student/{self.student_id}'
            yield scrapy.Request(
                url=url,
                callback=self.parse_student_detail,
                dont_filter=True
            )
        else:
            # Start with ISA data collection
            self.logger.info("Starting to fetch ISA data")
            url = self.get_isas_endpoint(1)
            yield scrapy.Request(
                url=url,
                callback=self.parse_isas,
                dont_filter=True
            )

    def parse_isas(self, response):
        self.logger.info(f"Received ISA response with status: {response.status}")
        
        try:
            data = response.json()
            self.logger.info(data)
            for row in data.get('aaData', []):
                html_content = row[0]
                link = re.findall(r'href="([^"]+)"', html_content)
                yield from response.follow_all(link, self.parse_links)
                
        except ValueError:
            self.logger.error("Invalid JSON response")

    def parse_links(self, response): 
        try:
            if 'sign' in response.url:
                self.logger.info("Found sign link: %s", response.url)
               # yield self.sign_isa(response)
            if 'view' in response.url:
                self.logger.info("Processing URL: %s", response.url)
                return self.get_data_from_link(response)
            
        except ValueError:
            self.logger.error("Invalid JSON response")
            with open('error_response.html', 'w') as f:
                f.write(response.text)

    def get_data_from_link(self, response):
        item = CavaItem()
        item['student_name'] = response.css('select#student-list-view option::text').get()
        item['iep_due_date'] = response.css('input#iep-due-date::attr(value)').get()
        item['student_id'] = response.css('input#student-id::attr(value)').get()
        item['iep_service'] =  response.css('select#service-list-view option::text').get()
        item['mode'] = response.css('select#delivery-mode option::text').get()
        
        if item['student_id']:
            yield item
            # After getting ISA data, fetch student details
            url = f'https://sped.fusionpl.us/students/student/{item["student_id"]}'
            yield scrapy.Request(
                url=url,
                callback=self.parse_student_detail
            )

    def sign_isa(self, response):
        try:
            # Extract the ISA ID from the URL
            match = re.search(r'/isas/sign/([a-f0-9]+)', response.url)
            if not match:
                self.logger.error("Could not extract ISA ID from URL")
                return
                
            isa_id = match.group(1)
            self.logger.info(f"Processing ISA signature for ID: {isa_id}")
            
            # Get request configuration from endpoints
            config = self.update_isa(isa_id)
            
            return scrapy.Request(
                url=config['url'],
                method=config['method'],
                body=json.dumps(config['data']),
                headers=config['headers'],
                callback=self.handle_isa_update,
                dont_filter=True
            )
               
        except Exception as e:
            self.logger.error(f"Error in sign_isa: {str(e)}")
            return None
        
    def handle_isa_update(self, response):
        try:
            if response.status == 200:
                result = response.json()
                self.logger.info(f"Successfully updated ISA: {result}")
                return result
            else:
                self.logger.error(f"Failed to update ISA. Status: {response.status}")
                self.logger.error(f"Response: {response.text}")
                return None
                
        except json.JSONDecodeError:
            self.logger.error(f"Invalid JSON response: {response.text}")
            return None
        except Exception as e:
            self.logger.error(f"Error handling ISA update: {str(e)}")
            return None
            
    def parse_student_detail(self, response):
        """Extract data from individual student page"""
        item = CavaItem()
        
        item['student_id'] = self.student_id or response.css('input.form-control[placeholder="Student ID"]::attr(value)').get()
        item['first_name'] = response.css('input.form-control[placeholder="First Name"]::attr(value)').get()
        item['last_name'] = response.css('input.form-control[placeholder="Last Name"]::attr(value)').get()
        item['gender'] = response.xpath("//div[contains(@class, 'col-md-6') and .//input[@checked]]/label/text()").get()
        item['birthday'] = response.css('input.form-control[placeholder="Birthday"]::attr(value)').get()
        item['ethnicity'] = response.css('input.form-control[placeholder="Ethnicity"]::attr(value)').get()
        item['race'] = response.css('input.form-control[placeholder="Race"]::attr(value)').get()
        item['grade'] = response.css('input.form-control[placeholder="Grade"]::attr(value)').get()
        item['address'] = response.xpath('//label[contains(text(), "Home Address")]/following::input[1]/@value').get()
        item['phone'] = response.xpath('//label[contains(text(), "Home Phone")]/following::input[1]/@value').get()
        item['school'] = response.css('input.form-control[placeholder="School"]::attr(value)').get()
        item['primary_teacher'] = response.css('input.form-control[placeholder="Primary Teacher"]::attr(value)').get()
        item['primary_disability'] = response.css('#s2id_primary-disability .select2-choice span::text').get()
        item['secondary_disability'] = response.css('#s2id_secondary-disability .select2-choice span::text').get()
        item['notes'] = response.css('textarea#notes::text').get()


        
        # Clean the data
        for key in item.keys():
            if isinstance(item[key], str):
                item[key] = item[key].strip()
        
        yield item
        raise CloseSpider('Successfully retrieved student details')