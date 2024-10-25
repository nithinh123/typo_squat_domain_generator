# Typesquat Domain Generation Project

This project generates potential typesquatted domains for a given target domain and performs analysis on the generated domains. The primary objective is to identify domains that may be used for phishing, brand impersonation, or other types of online fraud. The project leverages various algorithms and external tools to generate, categorize, and analyze these domains.

## Project Structure

The project contains the following files:

- `generate_domains.py`: Generates typesquatted domains based on the given target domain, leveraging techniques such as character swapping, replacement, omission, and insertion.
- `domain_categorise.py`: Categorizes generated domains based on predefined types or patterns.
- `get_domain_details.py`: Extracts detailed information about the generated domains, including registration data, and other relevant metadata.
- `get_typesquat_data.py`: Gathers and compiles data relevant to typesquatting for analysis and pattern identification.
- `levenshtein_distance.py`: Calculates the Levenshtein distance between domain names to determine similarity levels.
- `scrape_data.py`: Scrapes relevant data from various sources to enhance domain analysis and categorization.
- `vt_report.py`: Uses VirusTotal to fetch reputation reports on generated domains, providing insight into potential malicious activity.

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/nithinh123/typo_squat_domain_generator.git
    cd typesquat-domain-generation
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Configure API keys (if required, for example, for VirusTotal) in the respective files, or set them as environment variables.

## Usage

1. **Generate Domains**: Use `generate_domains.py` to generate a list of typesquatted domains for a target domain.
    ```bash
    python generate_domains.py --target <target_domain>
    ```

2. **Categorize Domains**: Categorize generated domains using `domain_categorise.py`.
    ```bash
    python domain_categorise.py --input <generated_domains_file>
    ```

3. **Analyze Domains**: Get detailed information about each domain using `get_domain_details.py`.
    ```bash
    python get_domain_details.py --input <generated_domains_file>
    ```

4. **Check Levenshtein Distance**: Measure similarity between domains using `levenshtein_distance.py`.
    ```bash
    python levenshtein_distance.py --input <generated_domains_file>
    ```

5. **Fetch VirusTotal Reports**: Run `vt_report.py` to obtain reputation data from VirusTotal.
    ```bash
    python vt_report.py --input <generated_domains_file>
    ```