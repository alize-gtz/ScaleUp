import requests
from requests import Response
import json
import time
import csv

from ScaleUp.exceptions.exceptions import UnknownCompany, UnhandledStatuscode



with open('ScaleUp/ressources/SIC_list_en.csv', mode='r') as infile:
    reader = csv.reader(infile)
    with open('ScaleUp/ressources/SIC_list_en.csv', mode='w') as outfile:
        writer = csv.writer(outfile)
        SIC_CODES_LIST = {rows[0]:rows[1] for rows in reader}


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
        sic = output["SIC_code"]
        business_activities = []
        
        if sic:
            for s in sic:
                business_activities.append(SIC_CODES_LIST[s])
            return business_activities
        return ""
    
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
        print(output)
        
        output.update( [('Activity', 
                        CompaniesHouse._get_business_activity(output))] )
                
        
        return output
    
        
CompaniesHouse("37d329d8-1701-4a77-91b3-5830388c9e7d").get_company_data("tesco")
    