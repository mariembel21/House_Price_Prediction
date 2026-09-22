import scrapy
from housescraper.items import HouseItem

class ImmobilierspiderSpider(scrapy.Spider):
    name = "immobilierspider"
    allowed_domains = ["www.immobilier.com.tn"]
    start_urls = ["https://www.immobilier.com.tn/resultat-recherche"]

    def parse(self, response):
        houses = response.css("div.col-12.layout-list a.annonce-card")

        for house in houses:
            house_item = HouseItem()

            house_item["titre" ] = house.css("h3::text").get()
            house_item["prix"] = house.css("div.price span::text").get()
            house_item["ville"] = house.css("small::text").get()
            house_item["surface"] = house.xpath(".//i[contains(@class, 'icon-area')]/following-sibling::text()").get()
            house_item["chambres"] = house.xpath(".//i[contains(@class, 'icon-bedrooms')]/following-sibling::text()").get()
            house_item["type_bien"] = house.css("ul.amenities li:last-child::text").get()
            house_item["type_transaction"] = "À Vendre"
            house_item["source"] = "immobilier"

            yield house_item

        next_page = response.css("a[aria-label='Page suivante']::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)



