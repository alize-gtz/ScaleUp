import requests
import json


class CompaniesHouse:
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        
 
    def _make_api_request(self, base_url:str, query:str) -> dict:
        key = self.api_key
        response = requests.get(base_url.format(query), auth=(key,''))
       
        #check status_code
        
        return json.JSONDecoder().decode(response.text)
        
    def _search_company_number(self, company_name:str) -> str:
        base_url = "https://api.companieshouse.gov.uk/search/companies?q={}"
        api_results = self._make_api_request(base_url, company_name)
        #check if empty response
        return api_results['items'][0]["company_number"]
            
    @staticmethod
    def _extract_data_if_dictpath_exists(dictionary : dict, *keys : str) -> str:
        for key in keys:
            try:
                dictionary = dictionary[key]
            except KeyError:
                return ""
        return dictionary
    
    def get_company_data(self, company_name:str) -> dict:
        
        company_number = self._search_company_number(company_name)
        base_url = "https://api.company-information.service.gov.uk/company/{}"
        company_data = self._make_api_request(base_url, company_number)
        
        return {"Name" : company_name,
                
                "CH_Name" : CompaniesHouse._extract_data_if_dictpath_exists(
                    company_data,
                    "company_name"),
                
                "Status" : CompaniesHouse._extract_data_if_dictpath_exists(
                    company_data,
                    "status"),
                
                "Type" : CompaniesHouse._extract_data_if_dictpath_exists(
                    company_data,
                    "type"),
                
                "City" : CompaniesHouse._extract_data_if_dictpath_exists(
                    company_data,
                    "registered_office_address", "locality"),
                
                "SIC_codes" : CompaniesHouse._extract_data_if_dictpath_exists(
                    company_data,
                    "sic_codes"),
                  }
    
        
    