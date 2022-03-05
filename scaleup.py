from tqdm import tqdm
import logging

from data_retrieval.companieshousesAPI import CompaniesHouse as CH
from data_retrieval.scaleupinstitute import get_companies
from exceptions.exceptions import UnknownCompany



class ScaleupUK_Dataset:
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.companies = get_companies()
        self.companies_data = self.get_all_companies_data()
    
    def get_all_companies_data(self):
        logging.getLogger().setLevel(logging.INFO)
        dataset = []
        for company in tqdm(self.companies):
            try:
                data = CH(self.api_key).get_company_data(company)
                dataset.append(data)
            except UnknownCompany:
                logging.info(f"Company {company} not found.")
        return dataset
