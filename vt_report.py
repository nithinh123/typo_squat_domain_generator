"""
Virus Total API integration module

"""
import re
import json
import base64
import requests


VT_ENDPOINT = "https://www.virustotal.com"

class VTReport:
    """
        This class checks an IP on Virus Total

    Attribute:
        domain: IP Address
        api_key: VirusTotal API key
    """
    def __init__(self, ip: str, api_key: str):
        self.ip = ip
        self.api_key = api_key

    def decode_api_key(self):
        """
            This method decodes base64 encoded api_key

        Returns:
            str: decoded api_key
        """
        return base64.b64decode(self.api_key)
    
    def update_api_key(self):
        """
            This method updates the api_key with the decoded api_key
        
        """
        self.api_key = self.decode_api_key()
        
    def get_domain_report(self) -> tuple:
        """
            This method get the Virus Total report for an IP

        Returns:
            Returns the required Virus Total report details
            Eg:
            True,
            {
                last_analysis_stats:{
                                "malicious": 5,
                                "suspicious": 0,
                                "harmless": 60
                            }
            }
        """
        try:
            url = f"{VT_ENDPOINT}/api/v3/ip_addresses/{self.ip}"
            headers = {
                "accept": "application/json",
                "x-apikey": self.api_key
            }
            response = requests.get(url, headers=headers, timeout=60)
            vt_data = json.loads(response.text)
            if response.status_code == 200:
                if "data" in vt_data and \
                    "attributes" in vt_data['data'] and \
                    "last_analysis_stats" in vt_data['data']['attributes']:
                    last_analysis_stats = vt_data["data"]["attributes"]["last_analysis_stats"]
                    del last_analysis_stats["timeout"]
                    del last_analysis_stats["undetected"]
                    whois_data = vt_data["data"]["attributes"]["whois"]
                    return True, {"last_analysis_stats":last_analysis_stats, \
                                  "whois_data": whois_data}
                else:
                    return False, "Required details not found in the api response"
            else:
                return False, str(response.content)
        except Exception as e:
            return False, f"Exception: {str(e)}"
        
    def process_whois(self, whois: str) -> tuple:
        country = ""
        reg_date = ""
        country_pattern = r"Country: (\w+)"
        regdate_pattern = r"RegDate: (\d{4}-\d{2}-\d{2})"
        country_match = re.search(country_pattern, whois)
        if country_match:
            country = country_match.group(1)
        regdate_match = re.search(regdate_pattern, whois)
        if regdate_match:
            reg_date = regdate_match.group(1)
        return country, reg_date

    def main(self) -> tuple:
        """
            Main function to generate a domain VT report
        """
        self.update_api_key()
        return self.get_domain_report()

"""  
if __name__ == '__main__':
    for item in new_output:
        #Base64 encoded VirusTotal API Key
        encoded_api_key = "ZjkzNzIxOGJjOTE0YmIxMGE4YWM1ZDkzMTRkMGZjNjIxZWRkYjVmNDZlMmQ5NGUwOGE1ZTQzMGNjNzJjNDg4YQ=="
        status, data = VTReport(item['ip'], encoded_api_key).main()
        if status:
            item.update(data['last_analysis_stats'])
    print(new_output)
"""