import re
import requests
from bs4 import BeautifulSoup

def is_valid_url(url):
    """ Check if the input is a valid URL """
    url_pattern = re.compile(
        r'^(https?://)?(www\.)?([a-zA-Z0-9_-]+)+(\.[a-zA-Z]+)+(\/[a-zA-Z0-9#_-]*)*$'
    )
    return bool(url_pattern.match(url))

def extract_job_details(url):
    """ Crawl the URL and extract job details """
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        job_details = {
            'companyName': extract_company_name(soup),
            'jobDescription': extract_job_description(soup),
            'requiredSkills': extract_skills(soup),
            'mandatorySkills': extract_mandatory_skills(soup),
            'locationType': extract_location(soup),
            'payRange': extract_pay_range(soup),
            'experienceNeeded': extract_experience(soup),
            'education': extract_education(soup),
            'immigrationSupport': extract_immigration_support(soup)
        }
        
        return job_details
    except Exception as e:
        print(f"Error extracting job details: {e}")
        return None

# Helper functions to extract specific information
def extract_company_name(soup):
    """ Extracts the company name from the page """
    return soup.find('h1').text if soup.find('h1') else 'Not Available'

def extract_job_description(soup):
    """ Extracts the job description """
    return soup.find('div', {'class': 'job-description'}).text if soup.find('div', {'class': 'job-description'}) else 'Not Available'

# Similarly, define the following functions:
# extract_skills, extract_mandatory_skills, extract_location, extract_pay_range, 
# extract_experience, extract_education, extract_immigration_support
