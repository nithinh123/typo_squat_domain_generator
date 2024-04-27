"""
    Main module for running the full 
    generation and categorization of domain
        
"""

import time
import asyncio
import argparse
import pandas as pd
from scrape_data import ScrapeData
from get_domain_details import AsyncAPICall
from vt_report import VTReport
from levenshtein_distance import LevenshteinDistance
from domain_categorise import CategoriseDomain


class TyposquatData:
    
    def __init__(self, domain, api_key):
        self.domain = domain
        self.api_key = api_key
        self.domain_list = list()
    
    def main(self):
        start = time.time()
        print("Scraping Data from dnstwist started")
        scrape_data = ScrapeData(self.domain, "chrome").scrape_domain_data()
        if scrape_data["status"]:
            print("Scraping Data Completed")
            print("Fetching domain registration and geo location")
            async_obj = AsyncAPICall(scrape_data["data"])
            data = asyncio.run(async_obj.main())
            self.domain_list = async_obj.merge_domain_details(data)
            print("Fetching domain registration and geo location completed")
        else:
            print("Failed to scrape data: ", scrape_data["message"])
            exit(-1)
        print("Fetching Virus Total Report started")
        for item in self.domain_list:
            status, vt_data = VTReport(item['ip'], self.api_key).main()
            print(status, vt_data)
            if status:
                item.update(vt_data['last_analysis_stats'])
        print("Fetching Virus Total Report completed")
        vt_df = pd.DataFrame(self.domain_list)
        print("Writing the vt data to csv in progress")
        vt_df.to_csv("domain_vt.csv")
        print("Writing the vt data to csv completed")
        print("Calcualting Levenshtein distance and reordering the data started")
        self.domain_list = LevenshteinDistance(self.domain_list, self.domain).domain_levenshtein_sort()
        print("Calcualting Levenshtein distance and reordering the data completed")
        ld_df = pd.DataFrame(self.domain_list)
        print("Writing the ld data to csv in progress")
        ld_df.to_csv("domain_ld.csv")
        print("Writing the ld data to csv completed")
        date_threshold = '2000-01-01'
        print("Categorizing Domains started")
        self.domain_list = CategoriseDomain(self.domain_list, date_threshold).categorise_domain()
        print("Categorizing Domains completed")
        c_df = pd.DataFrame(self.domain_list)
        print("Writing the categorized domain data to csv in progress")
        c_df.to_csv("domain_cat.csv")
        print("Writing the categorized domain data to csv completed")
        print("Category Details: ")
        print(c_df["category"].value_counts())
        end = time.time()
        print("Total time", end - start)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="An argparse example")
    parser.add_argument('domain_name', help='Domain Name')
    parser.add_argument('api_key', help='Encoded Virustotal api key')
    args = parser.parse_args()
    TyposquatData(args.domain_name, args.api_key).main()
