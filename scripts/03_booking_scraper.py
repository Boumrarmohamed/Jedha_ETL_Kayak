import os 
import logging
import scrapy
from scrapy.crawler import CrawlerProcess
import sys
import re

ville = str(sys.argv[1])

class BookingSpider(scrapy.Spider):
    def __init__(self, ville):
        self.ville = ville
    
    name = "booking"
    start_urls = ['https://www.booking.com/index.fr.html']
    
    def parse(self, response):
        logging.debug(self.ville)
        return scrapy.FormRequest.from_response(
            response,
            formdata={'ss': self.ville},
            callback=self.after_search
        )
    
    def after_search(self, response):
        hotels = response.xpath('/html/body/div[4]/div/div[2]/div/div[2]/div[3]/div[2]/div[2]/div[3]/div')
        
        if not hotels:
            hotels = response.xpath('//div[@data-testid="property-card"]')
        
        for hotel in hotels:
            
            if hotel.xpath('div[1]/div[2]/div/div/div[1]/div/div[1]/div/h3//a/@href').get():
                try:
                    next_page = hotel.xpath('div[1]/div[2]/div/div/div[1]/div/div[1]/div/h3/a').attrib["href"]
                except KeyError:
                    hotel_link = hotel.xpath('div[1]/div[2]/div/div/div[1]/div/div[1]/div/h3//a/@href').get()
                    logging.info(f'Problème pour passer sur la page de l hotel : {hotel_link}')
                else:
                    yield response.follow(next_page, callback=self.page_hotel)
            # Méthode de secours pour les nouveaux sélecteurs
            elif hotel.xpath('.//a[contains(@href, "/hotel/")]/@href').get():
                hotel_link = hotel.xpath('.//a[contains(@href, "/hotel/")]/@href').get()
                yield response.follow(hotel_link, callback=self.page_hotel)
    
    def page_hotel(self, response):
        html_content = response.text
        
        pattern_name = r'header__title">([^<]+)<'
        match_name = re.search(pattern_name, html_content)
        
        pattern_latlon = r'data-atlas-latlng="([^"]+)"'
        match_latlon = re.search(pattern_latlon, html_content)
        
        pattern_score = r'Avec une note de (.\..)'
        match_score = re.search(pattern_score, html_content)
        
        pattern_description = r"property-description\" class=\"[^\".]*\">(.+)</p></div></div>\n"
        match_description = re.search(pattern_description, html_content, flags=re.MULTILINE+re.DOTALL)
        
        if match_latlon:
            lat_lon = match_latlon.group(1)
            yield {
                'name': match_name.group(1) if match_name else 'Nom non trouvé',
                'latitude': lat_lon.split(",")[0],
                'longitude': lat_lon.split(",")[1],
                'score': match_score.group(1) if match_score else 'Score non trouvé',
                'url': response.url,
                'description': match_description.group(1) if match_description else ''
            }
        else:
            logging.debug(f"n'a pas trouvé le pattern data-atlas-latlng : {html_content}")

filename = "data/result_booking_"+str(ville)+".json"
if filename in os.listdir('data/'):
    os.remove(filename)

process = CrawlerProcess(settings = {
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'LOG_LEVEL': logging.INFO,
    'LOG_FILE': "data/log_file_booking.txt",
    'LOG_FILE_APPEND': False,
    "FEEDS": {
        filename: {"format": "json"},
    },
    'AUTOTHROTTLE_ENABLED': True,
    'AUTOTHROTTLE_START_DELAY': 1.0,
    'AUTOTHROTTLE_MAX_DELAY': 10.0,
    'AUTOTHROTTLE_TARGET_CONCURRENCY': 1.0,
    'AUTOTHROTTLE_DEBUG': True,
    'COMPRESSION_ENABLED': False,  
})

process.crawl(BookingSpider, ville)
process.start()