import scrapy
from housescraper.items import HouseItem
from urllib.parse import urljoin


class MubawabspiderSpider(scrapy.Spider):
    name = "mubawabspider"
    allowed_domains = ["www.mubawab.tn"]
    start_urls = ["https://www.mubawab.tn/en/cc/real-estate-for-sale"]

    def parse(self, response):
        houses = response.css("div.listingBox")

        for house in houses:

            link = house.css("h2.listingTit a::attr(href)").get()
            prix = house.css("div.priceBar span.priceTag::text").get()

            if link:
                full_link = urljoin(response.url, link)
                yield response.follow(
                    full_link,
                    callback=self.parse_detail,
                    meta={
                        "prix": prix,
                        }
                )

        # Pagination
        if ':p:' in response.url:
            current_page = int(response.url.split(':p:')[1])
        else:
            current_page = 1
        
        next_page = current_page + 1
        
        if next_page <= 280:
            if next_page == 2:
                next_url = "https://www.mubawab.tn/en/cc/real-estate-for-sale:p:2"
            else:
                next_url = response.url.replace(f':p:{current_page}', f':p:{next_page}')
            
            yield response.follow(next_url, self.parse)

    def parse_detail(self, response):
        house_item = HouseItem()
        house_item["titre"] = response.css("h1.searchTitle::text").get()
        house_item["type_bien"] = response.xpath("//p[contains(text(), 'Type of property')]/following-sibling::p/text()").get()
        house_item["prix"] = response.meta.get("prix")
        house_item["ville"] = ville = response.css("h3.greyTit::text").get()
        house_item["surface"] = response.css('.adDetailFeature .icon-triangle + span::text').get()
        house_item["chambres"] = response.css('.adDetailFeature .icon-bed + span::text').get()
        house_item["type_transaction"] = "À Vendre"
        house_item["source"] = "mubawab"
        
        yield house_item
