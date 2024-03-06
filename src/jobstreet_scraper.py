import pandas as pd
import requests

from bs4 import BeautifulSoup

from job_scraper import JobScraper

class JobStreetScraper(JobScraper):

    def __init__(self, job, config):
        super().__init__(job, config)
        self.base_url = config['url']['jobstreet']

    def parse_url(self):
        filters = self.config['filters']
        # jobstreet_config = config['jobstreet']
        url = f'{self.config['url']['jobstreet']}/{self.job}-jobs'

        if filters['location']:
            url = f'{url}/in-{filters['location']}'

        if filters['daterange']:
            url = f'{url}?daterange={filters['daterange']}'

        return url
    
    def scrape_site(self, url):

        job_listings = []
        page_number = 1
        page_url = url
        while True:
            response = requests.get(page_url)
            soup = BeautifulSoup(response.text, 'html.parser')

            for job_card in soup.find_all(attrs={"data-automation":"normalJob"}):
                job_title = getattr(job_card.find(attrs={"data-automation":"jobTitle"}), 'text', None)
                company_name = getattr(job_card.find(attrs={"data-automation":"jobCompany"}), 'text', None)
                salary = getattr(job_card.find(attrs={"data-automation":"jobSalary"}), 'text', None)
                job_link = job_card.find(attrs={"data-automation":"jobTitle"})['href']

                job_listings.append({
                    'job_title': job_title,
                    'company_name': company_name,
                    'salary': salary,
                    'job_link': f'{self.base_url}{job_link}'
                })

                page_number += 1

            if soup.find(attrs={'data-automation':f'page-{page_number}'}):
                print("next page exists")
                page_url = f'{url}?page={page_number}'
            else:
                break

        df = pd.DataFrame(job_listings)
        return df
