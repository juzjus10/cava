import json
import scrapy

class DataTableEndpoints:
    @staticmethod
    def get_isas_endpoint(display_start=0, display_length=1, search_term=None):
     
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
    def get_students_endpoint(display_start=0, display_length=10, search_term=None, student_id=None):

        base_url = 'https://sped.fusionpl.us/students/_retrieve_server_data'
        
        # If student_id is provided, use it as the search term
        final_search = student_id or search_term or ''
        
        params = {
            'sEcho': 1,
            'iColumns': 8,
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
            'sSearch': final_search,
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
            'bSortable_7': 'true'
        }
        
        # Use urllib.parse to create a properly formatted query string
        import urllib.parse
        query_string = urllib.parse.urlencode(params)
        
        return f"{base_url}?{query_string}"
    
  
    @staticmethod
    def update_isa(isa_id):
        """
        Creates a request configuration for updating an ISA
        Args:
            isa_id (str): The ID of the ISA to update
        Returns:
            dict: Request configuration including URL, method, data, and headers
        """
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
    
def get_all_isas(spider):
    """Example function to fetch all ISAs using pagination"""
    url = DataTableEndpoints.get_isas_endpoint(display_start=0, display_length=100)
    return scrapy.Request(
        url=url,
        callback=spider.parse_isas_data,
        headers={
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': 'application/json'
        }
    )

def search_student_by_id(spider, student_id):
    """Example function to search for a specific student by ID"""
    url = DataTableEndpoints.get_students_endpoint(student_id=student_id)
    return scrapy.Request(
        url=url,
        callback=spider.parse_student_data,
        headers={
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': 'application/json'
        }
    )