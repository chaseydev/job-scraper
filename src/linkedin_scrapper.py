import pandas as pd
import time

from bs4 import BeautifulSoup
from retrying import retry
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from custom_exceptions import ExpectedPageNotFound
from job_scrapper import JobsScrapper

class LinkedInScrapper(JobsScrapper):

    def __init__(self, job, config):
        super().__init__(job, config)
        self.base_url = config['url']['linkedin']

    def parse_url(self):
        url = f'{self.base_url}/jobs/search?keywords={self.job}'

        filters = self.config['filters']

        if filters['location']:
            url = f'{url}&location={filters['location']}'

        if filters['daterange']:
            # convert days to seconds to match linkedin url syntax
            daterange = int(filters['daterange']) * 24 * 60 * 60
            url = f'{url}&f_TPR=r{daterange}'

        return url
    
    @retry(stop_max_attempt_number=10, retry_on_exception=lambda x: isinstance(x, ExpectedPageNotFound), wait_fixed=2000)
    def scrape_site(self, url):
        browser = webdriver.Chrome()
        browser.get(url)
        time.sleep(2)

        elem = browser.find_element(By.TAG_NAME, "body")
        job_cards = []

        max_iterations = 100 # to avoid an infinite loop
        iteration = 0
        job_cards_len = 0

        # end loop when max_iterations is reached or there are no more new cards found
        while (iteration < max_iterations) or (len(job_cards) != job_cards_len):
            browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)

            job_cards = elem.find_elements(By.CLASS_NAME, 'base-card')
            
            if len(job_cards) == 0:
                print('page not found... retrying')
                browser.quit()
                raise ExpectedPageNotFound('No cards found')

            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            job_cards_len = len(job_cards)

            iteration += 1

        job_cards = [job_card.get_attribute('outerHTML') for job_card in job_cards]
        browser.quit()

        job_listings = []
        for job_card in job_cards:
            job_card = BeautifulSoup(job_card,'html.parser')
            job_title = getattr(job_card.find(class_='base-search-card__title'), 'text', None)
            company_name = getattr(job_card.find(attrs={'data-tracking-control-name':'public_jobs_jserp-result_job-search-card-subtitle'}), 'text', None)
            salary = getattr(job_card.find(class_='job-search-card__salary-info'), 'text', None)
            job_link = job_card.find('a')['href']

            job_listings.append({
                'job_title': job_title,
                'company_name': company_name,
                'salary': salary,
                'job_link': job_link
            })

        df = pd.DataFrame(job_listings)

        return df
    
    def refine_data(self, df):
        df = df.replace('\n ', '', regex=True)

        df['job_title'] = df['job_title'].str.strip()
        df['company_name'] = df['company_name'].str.strip()
        df['job_link'] = df['job_link'].str.strip()
        
        # the scapper sometimes retrieves duplicate jobs with the same entry but different link IDs
        df = df.drop_duplicates(subset=['job_title', 'company_name', 'salary']).reset_index(drop=True)
        return df