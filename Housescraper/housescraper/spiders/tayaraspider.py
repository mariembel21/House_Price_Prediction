import scrapy
from housescraper.items import HouseItem
from urllib.parse import urljoin
import re


class TayaraspiderSpider(scrapy.Spider):
    name = "tayaraspider"
    allowed_domains = ["www.tayara.tn"]
    start_urls = ["https://www.tayara.tn/listing/c/immobilier"]

    def parse(self, response):
        houses = response.css("article.mx-0")

        for house in houses:

            prix = house.css("data::attr(value)").get()

            link = house.css("a::attr(href)").get()
            if link:
                full_link = urljoin(response.url, link)

            yield response.follow(
                full_link,
                callback=self.parse_detail,
                meta={
                    "prix": prix 
                }
            )

        
        
        if '?page=' in response.url:
            current_page = int(response.url.split('?page=')[1])
            next_page = current_page + 1
        else:
            current_page = 1
            next_page = 2

        if next_page <= 317:
            next_page_url = f"https://www.tayara.tn/listing/c/immobilier/?page={next_page}"
            yield response.follow(next_page_url, self.parse)

    def parse_detail(self, response):
            house_item = HouseItem()
        
            house_item["titre"] = response.css("h1::text").get()
            house_item["prix"] = response.meta.get("prix")
            house_item["type_bien"] = response.xpath("//ul[contains(@class, 'hidden md:flex')]/li[2]/span/text()").get()
            house_item["ville"] = response.xpath("//ul[contains(@class, 'hidden md:flex')]/li[3]/span/text()").get()
            house_item["surface"] = response.xpath("//span[contains(., 'Superficie')]/../span[last()]/text()").get()
            house_item["chambres"] = response.xpath("//span[contains(., 'Chambres')]/../span[last()]/text()").get()
            house_item["type_transaction"] = response.xpath("//span[contains(., 'Type de transaction')]/../span[last()]/text()").get()
            house_item["source"] = "tayara"
            yield house_item