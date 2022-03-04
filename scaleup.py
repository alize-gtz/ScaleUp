from tqdm import tqdm
import pandas as pd
import numpy as np

from ScaleUp.companieshouse.companieshousesAPI import CompaniesHouse as CH
from ScaleUp.scaleupinstitute.scaleupinstitute import get_companies
from ScaleUp.exceptions.exceptions import UnknownCompany



class ScaleupUK_Dataset:
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.companies = get_companies()
        self.companies_data = self.get_all_companies_data()
        self.companies_not_retrieved = []
    
    def get_all_companies_data(self):
        dataset = []
        for company in tqdm(self.companies):
            try:
                data = CH(self.api_key).get_company_data(company)
                dataset.append(data)
            except UnknownCompany:
                self.companies_not_retrieved.append(company)
        return dataset
    
    def get_all_companies_data_table(self):
        dataset = self.companies_data
        df = pd.DataFrame(dataset)
        df.fillna("",inplace=True)
        df_sic = pd.DataFrame(df["SIC_code"].tolist(), index= df.index).add_prefix('SIC_')
        df_activity = pd.DataFrame(df["Activity"].tolist(), index= df.index).add_prefix('Activity_')
        
        df = pd.concat([df.drop(["SIC_code", "Activity"], axis = 1), df_activity, df_sic], axis = 1)
        
        
        return df.replace(to_replace=[None, r'^\s*$'], value=np.nan, inplace=True)