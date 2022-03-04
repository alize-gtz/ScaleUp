class UnsupportedLocation(Exception):

    def __init__(self, location):
        self.message = (
            f"This function retrives ScaleUp companies in the UK. "
            f"{location} is not a valid region. "
            f"Please enter England, Wales, Northern-ireland or Scotland."
        )

    def __str__(self):
        return self.message
    
    

class UnknownCompany(Exception):

    def __init__(self, company_name):
        self.message = (f"{company_name} could not be found in Companies "
                        "House's Database.")

    def __str__(self):
        return self.message