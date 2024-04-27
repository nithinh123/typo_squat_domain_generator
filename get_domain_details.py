import aiohttp
import asyncio

API_ENDPOINT = "http://20.67.244.20:8000"

class AsyncAPICall:
    """
        This class does Asynchronous API Calls and returns 
        the response of all the requests in a list
        
    """
    
    def __init__(self, domain_list: list):
        self.domain_list = domain_list

    async def fetch_domain_data(self, session, url):
        """
            This method uses session.get() to make an asynchronous HTTP GET request
            and returns the API response in json format
        
        """
        async with session.get(url) as response:
            return await response.json()

    async def main(self):
        """
            This method is the main function which creates ClientSession for 
            making asynchronous HTTP requests
            
            'asyncio.gather()' runs the tasks concurrently and gather their results
        
        """
        results = []
        async with aiohttp.ClientSession() as session:
            url = f"{API_ENDPOINT}/get_domain_details"
            tasks = [self.fetch_domain_data(session, f"{url}/{domain['domain']}") for domain in self.domain_list]
            results = await asyncio.gather(*tasks)
        return results
    
    def merge_domain_details(self, data_async: list) -> list:
        """
            This function merges the async api output list 
            with the input domain list

        Args:
            data_async (list): async api output

        Returns:
            list: merged input list of domain dict with the 
            l     location and registartion date
        """
        new_dict = {x['domain']: x for x in self.domain_list}
        for item in data_async:
            if item['domain'] in new_dict:
                new_dict[item['domain']].update(item)
            else:
                new_dict[item['domain']] = item
        merged_list = list(new_dict.values())
        return merged_list
