# Job Scraper

This project is a Python-based web scraper designed to extract job listings from LinkedIn and Jobstreet (and potentially more sites in the future), consolidating them into a single CSV file. It employs the Template Method Design Pattern, with the abstract/interface class `JobScrapper` and concrete subclasses `LinkedInScrapper` and `JobstreetScrapper`. This architecture allows for easy integration of additional job sites by creating new concrete subclasses.

## Features
- Scrapes job listings from LinkedIn and Jobstreet
- Consolidates job listings into a single CSV file
- Easily extensible to add support for additional job sites

## Installation
To use this scraper, follow these steps:
1. Clone the repository to your local machine.
2. Create a virtual environment.
3. Install the dependencies listed in `requirements.txt`.
4. Run `src/test_scrapper.ipynb` to execute the scraper and generate the CSV output.

## Requirements
- Python 3.x
- Beautiful Soup
- Selenium
- Pandas
- Requests
- Retry

## Usage
1. Navigate to the `src` directory.
2. Run `test_scrapper.ipynb` using Jupyter Notebook or any compatible environment.
4. Once completed, the consolidated job listings will be saved as a CSV file.

## Future Improvements
- Enhance error handling and logging mechanisms.
- Improve performance by optimizing scraping algorithms.
- Add support for additional job sites.
- Implement advanced filtering and sorting options for job listings.

## Disclaimer
This project is for personal and non-commercial use only. Scraping websites may violate their terms of service, so use this tool responsibly and ensure compliance with legal regulations and ethical standards.
