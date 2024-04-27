import Levenshtein

LEVENShTEIN_THRESHOLD = 4

class LevenshteinDistance:
    """
        This Class calculates Levenshtein Distance and 
        sort the domain list
    """
    def __init__(self, domain_data, domain):
        self.domain_data = domain_data
        self.domain = domain

    def domain_levenshtein_sort(self):
        """
            This Method calculates the levenstein distance and sort the domain 
            details list with ascending order of levenshtein distance by removing
            domains with levenshtein distance greater than the LEVENSTEIN_THRESHOLD 
        
        """
        output_data = []
        for item in self.domain_data:
            distance = Levenshtein.distance(self.domain, item["domain"])
            if distance <= LEVENShTEIN_THRESHOLD and item["domain"] != 'www.google.com':
                item['levenshtein_distance'] = distance
                output_data.append(item)
        sorted_data = sorted(output_data, key=lambda x: x['levenshtein_distance'])
        return sorted_data
