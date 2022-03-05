# ScaleUp

The repository provides the code to retrieve ScaleUp companies in the UK from the ScaleUp Institute website, using Selenium, and their information with the Companies House API.

## How to use

To use this code, it is necessary to register an app through the [Commpanies House website](https://developer.company-information.service.gov.uk), in order to obtain an API key. 

The following code will instantiate an object of class ScaleupUK_Dataset.

```python
API_KEY = ***
    
from scaleup import ScaleupUK_Dataset

sc = ScaleupUK_Dataset(API_KEY)

dataset = sc.companies_data
```

It is also possible to retrieve data for one specific company:

```python
from data_retrieval.companieshousesAPI import CompaniesHouse as CH

zoopla_data = CH(self.API_KEY).get_company_data("zoopla")

```
Or to retrieve ScaleUp companies in one of the UK's individual countries (England, Wales, Scotland or Northern-Ireland):

```python
from data_retrieval.scaleupinstitute import get_companies

wales_sc = get_companies("wales")
```

## Output data

The final data is available in the output_data file.

## Known issues

The function retrieving data from the Companies House API uses the *company search* endpoint, which returns results in an order of relevance, and takes the first result. However, it sometimes fails to associate the right company.

Future versions will likely solve this issue, and provide a way to find a better match in the Companies House's search results.
