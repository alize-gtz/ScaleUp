import requests
import json
import time
import re

from exceptions.exceptions import UnknownCompany, UnhandledStatuscode


class CompaniesHouse:
    
    
    def __init__(self, api_key: str):
        self.api_key = api_key
 
    def _make_api_request(self, base_url:str, query:str, max_attempts : int = 3) -> dict:
        key = self.api_key
        
        for _ in range(max_attempts):
        
            response = requests.get(base_url.format(query), auth=(key,''))
            if response.status_code == 200:
                return json.JSONDecoder().decode(response.text)
            
            elif response.status_code == 429:
                print("The number of requests limit (600 per 5 minutes) "\
                      "has been reached. Programm will resume in 5 minutes.")
                time.sleep(300)
                continue
            else: 
                raise UnhandledStatuscode(response)
             
    
    def _search_company_number(self, company_name:str) -> str:
        base_url = "https://api.companieshouse.gov.uk/search/companies?q={}"
        api_results = self._make_api_request(base_url, company_name)
        
        if not api_results['items']:
            raise UnknownCompany(company_name)
        else : 
            return api_results['items'][0]["company_number"]
            
    @staticmethod
    def _extract_data_if_dictpath_exists(dictionary : dict, *keys : str) -> str:
        for key in keys:
            try:
                dictionary = dictionary[key]
            except KeyError:
                return ""
        return dictionary
    
    @staticmethod
    def _get_business_activity(output: dict) -> dict:
        with open('ressources/SIC_list.json', 'r') as fp:
            SIC_CODES_LIST = json.load(fp)
            
        sic = output["SIC_code"]
        business_activities = []
        valid_sic_codes = list(SIC_CODES_LIST.keys())
        
        for s in sic:
            if s in valid_sic_codes:
                business_activities.append(SIC_CODES_LIST[s])
        return business_activities

    
    def get_company_data(self, company_name:str) -> dict:
        
        company_number = self._search_company_number(company_name)
        base_url = "https://api.company-information.service.gov.uk/company/{}"
        company_data = self._make_api_request(base_url, company_number)
        
        output =  {"Name" : company_name,
                
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
                
                "SIC_code" : CompaniesHouse._extract_data_if_dictpath_exists(
                    company_data,
                    "sic_codes"),
                  }
        
        output.update( [('Activity', 
                        CompaniesHouse._get_business_activity(output))] )
                
        
        return output


