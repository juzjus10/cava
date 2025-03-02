# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from itemadapter import ItemAdapter
import json
from pyairtable import Api
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

class CavaspiderPipeline:
    def process_item(self, item, spider):
        return item

class BasePipeline:
    def process_item(self, item, spider):
        return item

class AirtablePipeline:
    def __init__(self):
        # Replace these with your actual Airtable credentials
        self.api_key = os.getenv('AT_API_KEY')
        self.base_id = os.getenv('AT_BASE_ID')
        self.table_id = os.getenv('AT_TABLE_ID')
        
        if not all([self.api_key, self.base_id, self.table_id]):
            raise ValueError("Missing required Airtable credentials")
        
        self.api = Api(self.api_key)
        self.table = self.api.table(self.base_id, self.table_id)

        self.field_mapping = {
            'student_id': 'Student ID',
            # 'first_name': 'Student First Name',
            # 'last_name': 'Student Last Name',
            'gender': 'Student Gender',
            #'birthday': 'Date of Birth',
            'ethnicity': 'Student Race/Ethnicity',
            'race': 'Student Race/Ethnicity',
            'grade': 'Grade',
            'address': 'Student Address',
            'phone': 'Parent 1 Phone',
            #'school': 'School',
            'primary_teacher': 'Case Carrier Name',
            #'primary_disability': 'Current Eligibility',
            #'secondary_disability': 'Suspected Eligibility',
            'notes': 'Notes',
            'iep_due_date': 'Due Date / IEP Date',
            #'iep_service': 'Evaluation Type',
            'student_name': 'Student Name',
            'mode': 'Mode'
        }
    
    def process_item(self, item, spider):
        # Create a record dictionary
        record = {self.field_mapping[key]: value for key, value in dict(item).items() if key in self.field_mapping}
        
        if 'Student Name' in record:
            record['Student Name'] = f"TEST TEST"
        if 'Date of Birth' in record and record['Date of Birth']:
            try:
                date_obj = datetime.strptime(record['Date of Birth'], '%m/%d/%Y')  # Adjust format for Airtable
                record['Date of Birth'] = date_obj.strftime('%Y-%m-%d')
            except ValueError:
                spider.logger.error(f"Invalid date format for Birthday: {record['Date of Birth']}")
        
        # Check if student already exists
        existing_records = self.table.all(formula=f"{{Student ID}}='{record['Student ID']}'")
        
        if existing_records:
            # Update existing record
            self.table.update(existing_records[0]['id'], record)
        else:
            # Create new record
            self.table.create(record)
            
        return item