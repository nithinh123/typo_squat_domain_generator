import tldextract
from lib import constants


class GenerateDomainName:
    """
    A class to generate domain names using
    diffrent type squatting methods

    ...

    Attributes
    ----------
    domain : str
        domain that need to be searched for
        Typosquatting related entries

    Methods
    -------
    parse_domain():
        parse a domain into three parts domain_prefix,
        domain_without_tld and domain_tld

    append_prefix_suffix():
        appends domain_prefix and domain_tld to domain name

    get_letters_numbers():
        generates numbers [0-9] and letter [a-z]

    addition():
        adds single characters from [a-z] and [0-9]
        to the domain name

    omission():
        removes a charactor from the domain name

    repetition():
        using all characters that already exists in the
        domain name one by one to create new domain name

    replacement():
        replaces a charactor in the domain name

    replace_char():
        replaces a charactor with multiple occurrence
        one at a time in a string with another charactor

    homoglyphs():
        replaces all possible homoglyphs using
        the mapping data

    bit_squatting():
        flips the jTh bit in iTh charactor of any domain to
        generate multiple possible bit-squatting

    main():
        main method that calls all the
        functions to generate domain names

    """

    def __init__(self, domain: str):
        self.domain = domain
        prefix, domain_name, tld = self.parse_domain()
        self.domain_prefix = prefix
        self.domain_name = domain_name
        self.domain_tld = tld
        self.domain_list = []

    def parse_domain(self) -> tuple:
        """
            This method splits domain to domain_prefix,
            domain_without_tld and domain_tld

        Returns:
            tuple: domain_prefix, domain_without_tld, domain_tld
        """
        domain_extract = tldextract.extract(self.domain)
        domain_prefix = domain_extract.subdomain + "."
        domain_without_tld = domain_extract.domain
        domain_tld = "." + domain_extract.suffix
        return domain_prefix, domain_without_tld, domain_tld

    def append_prefix_suffix(self, name: str) -> str:
        """
            This method appends the domain prefix and tld
            to generated domain name

        Returns:
            list: domain name with prefix and tld
        """
        return self.domain_prefix + name + self.domain_tld

    @staticmethod
    def get_letters_numbers() -> list:
        """
            This method generates numbers [0-9] and letter [a-z]

        Returns:
            list: list of numbers [0-9] and letters [a-z]
        """
        number_strings = [str(i) for i in range(10)]
        letter_strings = [chr(ord('a') + i) for i in range(26)]
        combined_list = number_strings + letter_strings
        return combined_list

    def addition(self) -> list:
        """
            This method adds single characters from [a-z] and [0-9]
            to the domain name to create possible domain names

        Returns:
            list: list of type squatted domains
        """
        combined_list = self.get_letters_numbers()
        for addition_string in combined_list:
            for j in range(0, len(self.domain_name)):
                domain_variation = self.append_prefix_suffix(self.domain_name[:j] + \
                                                             addition_string + self.domain_name[j:])
                if domain_variation not in self.domain_list:
                    self.domain_list.append(domain_variation)
                if j == len(self.domain_name) - 1:
                    domain_variation = self.append_prefix_suffix(self.domain_name + \
                                                                 addition_string)
                    self.domain_list.append(domain_variation)
        return self.domain_list

    def omission(self) -> list:
        """
            This method removes a charactor from the domain name
            to create possible domain names

        Returns:
            list: list of type squatted domains
        """
        for i in range(0, len(self.domain_name)):
            domain_variation = self.append_prefix_suffix(self.domain_name[0:i] +
                                self.domain_name[i + 1:len(self.domain_name)])
            if domain_variation not in self.domain_list:
                self.domain_list.append(domain_variation)
        return self.domain_list

    def repetition(self) -> list:
        """
            This method uses all characters that already exists in the
            domain name one by one to create possible domain names

        Returns:
            list: list of type squatted domains
        """
        for i, letter in enumerate(self.domain_name):
            domain_variation = self.append_prefix_suffix(self.domain_name[:i]
                                                         + letter + self.domain_name[i:])
            if domain_variation not in self.domain_list:
                self.domain_list.append(domain_variation)
        return self.domain_list

    def replacement(self) -> list:
        """
            This method replaces a charactor in the domain name
            to create possible domain names

        Returns:
            list: list of type squatted domains
        """
        letters_numbers = self.get_letters_numbers()
        for replacement_string in letters_numbers:
            for j in range(0, len(self.domain_name)):
                first = self.domain_name[:j]
                last = self.domain_name[j + 1:]
                domain_variation = self.append_prefix_suffix(first + 
                                            replacement_string + last)
                if domain_variation not in self.domain_list:
                    self.domain_list.append(domain_variation)
        return self.domain_list

    @staticmethod
    def replace_char(original_string: str, target: str, replacement: str) -> list:
        """
            This method replaces a charactor with multiple occurrence
            one at a time in a string with another charactor

        Returns:
            list: list of possible strings after replacement
        """
        index = []
        new_strings = []
        for i, char in enumerate(original_string):
            if char == target:
                index.append(i)
        for item in index:
            if item != -1:
                new_string = original_string[:item] + replacement + \
                            original_string[item + 1:]
                new_strings.append(new_string)
            else:
                return [original_string]
        return new_strings

    def homoglyphs(self) -> list:
        """
            This method replaces all possible homoglyphs using
            the mapping data to create possible domain names

        Returns:
            list: list of type squatted domains
        """
        for item in self.domain_name:
            if item in constants.SIMILAR_CHAR:
                for glyph in constants.SIMILAR_CHAR[item]:
                    modified_domains = self.replace_char(self.domain_name,
                                                         item, glyph)
                    for modified_domain in modified_domains:
                        domain_variation = self.append_prefix_suffix(modified_domain)
                        if domain_variation not in self.domain_list:
                            self.domain_list.append(domain_variation)
        return self.domain_list

    def bit_squatting(self) -> list:
        """
            This method flips the jTh bit in iTh charactor of any domain to
            generate multiple possible bit-squatting

        Returns:
            list: list of type squatted domains
        """
        for i, _ in enumerate(self.domain_name):
            for j in range(8):
                bit_squatted_char = chr(ord(self.domain_name[i]) ^ (1 << j))
                if bit_squatted_char.isalnum():
                    domain_variation = self.append_prefix_suffix(
                        self.domain_name[:i] + bit_squatted_char + self.domain_name[i + 1:])
                    if domain_variation not in self.domain_list:
                        self.domain_list.append(domain_variation)
        return self.domain_list

    def main(self) -> list:
        """
            This method is the main method that calls all the
            functions to generate domain names

        Returns:
            list: list of type squatted domains
        """
        self.addition()
        self.omission()
        self.repetition()
        self.replacement()
        self.homoglyphs()
        self.bit_squatting()
        return self.domain_list


if __name__ == '__main__':
    possible = GenerateDomainName("www.google.com").main()
    print(possible)