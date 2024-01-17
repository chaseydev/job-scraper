# Template Class
from abc import ABC, abstractmethod

class JobsScrapper(ABC):
    
    @abstractmethod
    def __init__(self, job, config):
        self.job = job
        self.config = config

    @abstractmethod
    def parse_url(self):
        pass

    @abstractmethod
    def scrape_site(self):
        pass

    def refine_data(self, df):
        # By default just returns the same dataframe for when refinement
        # is not needed but can be overriden by concrete classes
        return df

    @classmethod
    def get_jobs(cls, job, config):
        instance = cls(job, config)

        url = instance.parse_url()
        df = instance.scrape_site(url)
        df = instance.refine_data(df)
        return df