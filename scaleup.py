from tqdm import tqdm
from json import JSONDecodeError

from ScaleUp.companieshouse.companieshousesAPI import CompaniesHouse as CH
from ScaleUp.scaleupinstitute.scaleupinstitute import get_companies



class ScaleupUK_Dataset:
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.companies = get_companies()
        self.companies_data = self.get_all_companies_data()
    
    def get_all_companies_data(self):
        dataset = []
        for company in tqdm(self.companies):
            try : 
                data = CH(self.api_key).get_company_data(company)
                dataset.append(data)
            except JSONDecodeError:
                print(company)
        return dataset
  
    
  
    

test = ScaleupUK_Dataset(api_key = "37d329d8-1701-4a77-91b3-5830388c9e7d")

test.api_key
len(test.companies)
