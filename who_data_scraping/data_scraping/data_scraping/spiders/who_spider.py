"""CSC110 Fall 2020 Course Project: Scraping Spider

Authors: Michele Massa, Nischal Nair, Nathan Zavys-Cox

Description: this module contains functions that conduct the needed procedures to
scrape the needed data from the 3 different WHO sites. To generate the json file,
read instructions at the end of the file.

This file is copyright (c) 2020 Michele Massa, Nischal Nair and Nathan Zavys-Cox."""

import scrapy
from ..items import UsingScrapyItem


# take key facts
class WHOSpider(scrapy.Spider):
    """ Scrappy.Spider subclass that scrapes data for 3 different respiratory diseases
    that are in some way related to the air quality (and therefore are impacted by CO2
    emissions, from 3 different World Health Organization (WHO) websites."""
    name = 'who_site'

    disease_1 = 'asthma'
    disease_2 = 'pneumonia'
    disease_3 = 'chronic-obstructive-pulmonary-disease-(copd)'

    # Since there are 3 urls, we use the same url root + the specific disease to extract data from the needed page.
    start_urls = ['https://www.who.int/news-room/fact-sheets/detail/' + disease_1]

    def parse(self, response, **kwargs):
        """ Extract data from the websites."""

        items = UsingScrapyItem()

        all_key_facts = response.css('.separator-line li::text').extract()
        items['key_facts'] = all_key_facts
        yield items

        next_disease = 'https://www.who.int/news-room/fact-sheets/detail/' + str(WHOSpider.disease_2)
        yield response.follow(next_disease, callback=self.parse)

        next_next_disease = 'https://www.who.int/news-room/fact-sheets/detail/' + str(WHOSpider.disease_3)
        yield response.follow(next_next_disease, callback=self.parse)

# USAGE INSTRUCTIONS (if user wants to see how scraping works)

# 1. Go to terminal.
# 2. In the terminal use 'cd <folder_name>' until the folder 'FINAL_PROJECT_2' is reached.
# 3. In the terminal, activate the spider and store the scraped data by calling the following command:
# 'scrapy crawl who_site -o disease_data.json'

# This will create a json file with the scraped data inside the 'who_data_scraping' folder. This means that to be used
# by our program, it will have to be taken to the 'FINAL_PROJECT' folder (which should be marked as sources root). The
# json file is already there, placed by us, but this is just for evaluation purposes, to see that the file was created
# using our most important library Scrapy.

# There is no real way of testing the spider's functionality apart from creating a json file with it and comparing
# it to the one that we have included.

# Since this file is not meant to be run in the console, but rather the terminal, we decided to not include doctests
# nor python-TA, as we have already explained how the testing is done.
