from datetime import datetime

SUSPICIOUS_COUNTRIES = ["KR"]

class CategoriseDomain:
    """
        This class categorises the domain
    """
    def __init__(self, domain_data, reg_date_threshold):
        self.domain_data = domain_data
        self.reg_date_threshold = datetime.strptime(reg_date_threshold, '%Y-%m-%d')
        
    def categorise_domain(self) -> list:
        """
            This method categorises the domain based on multiple conditions
        """
        categorise_data = []
        for item in self.domain_data:
            reg_date_flag = self.check_registration_date(item["reg_date"])
            if item["malicious"] > 0:
                categorise_data.append({"domain":item["domain"],"category":"malicious"})
            elif (item["suspicious"] > 0 or item["levenshtein_distance"] == 1) \
                    or (reg_date_flag and self.check_registered_country(item["country"])):
                categorise_data.append({"domain":item["domain"],"category":"suspicious"})
            else:
                categorise_data.append({"domain":item["domain"],"category":"benign"})
        return categorise_data
    
    def check_registration_date(self, registration_date) -> bool:
        """
            This method checks if the domain's registration 
            date is less than the threshold registration date
        """
        if registration_date != '':
            registration_date = datetime.strptime(registration_date, '%Y-%m-%d')
            if registration_date < self.reg_date_threshold:
                return True
        return False
    
    def check_registered_country(self, country) -> bool:
        """
            This method checks if the domain's registration 
            country belongs to suspicious countries list
        """
        if country in SUSPICIOUS_COUNTRIES:
            return True
        return False
