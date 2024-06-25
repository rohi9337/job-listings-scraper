import scrapy
from scrapy_selenium import SeleniumRequest
import urllib.parse

class JobSpider(scrapy.Spider):
    name = 'job_spider'
    
    def __init__(self, search_term='django', *args, **kwargs):
        super(JobSpider, self).__init__(*args, **kwargs)
        self.search_term = search_term

    def start_requests(self):
        encoded_search_term = urllib.parse.quote(self.search_term)
        start_url = f'https://www.linkedin.com/jobs/search?keywords={encoded_search_term}'
        yield SeleniumRequest(url=start_url, callback=self.parse)

    def parse(self, response):
        self.logger.info(f"Scraping URL: {response.url}")
        job_listings = response.css('ul.jobs-search__results-list li')
        
        if not job_listings:
            self.logger.warning("No job listings found")
        else:
            for job in job_listings:
                yield {
                    'title': job.css('h3::text').get().strip(),
                    'company': job.css('h4 span::text, h4 a::text').get().strip(),
                    'location': job.css('.job-search-card__location::text').get().strip(),
                    'date_posted': job.css('time::attr(datetime)').get(),
                    'link': job.css('a::attr(href)').get(),
                }

        next_page = response.css('a[aria-label="Next"]::attr(href)').get()
        if next_page:
            yield SeleniumRequest(url=response.urljoin(next_page), callback=self.parse)










# import scrapy
# from scrapy_selenium import SeleniumRequest

# class JobSpider(scrapy.Spider):
#     name = 'job_spider'
#     start_urls = ['https://www.linkedin.com/jobs/search?keywords=django']

#     def start_requests(self):
#         for url in self.start_urls:
#             yield SeleniumRequest(url=url, callback=self.parse)

#     def parse(self, response):
#         self.logger.info(f"Scraping URL: {response.url}")
#         job_listings = response.css('ul.jobs-search__results-list li')
        
#         if not job_listings:
#             self.logger.warning("No job listings found")
#         else:
#             for job in job_listings:
#                 yield {
#                     'title': job.css('h3::text').get().strip(),
#                     'company': job.css('h4 span::text, h4 a::text').get().strip(),
#                     'location': job.css('.job-search-card__location::text').get().strip(),
#                     'date_posted': job.css('time::attr(datetime)').get(),
#                     'link': job.css('a::attr(href)').get(),
#                 }

#         next_page = response.css('a[aria-label="Next"]::attr(href)').get()
#         if next_page:
#             yield SeleniumRequest(url=response.urljoin(next_page), callback=self.parse)
