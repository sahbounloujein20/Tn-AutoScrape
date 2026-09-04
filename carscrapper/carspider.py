import scrapy
from carscrapper.items import VoitureItem

class OccasionSpider(scrapy.Spider):
    name = "occasion"
    allowed_domains = ["automobile.tn"]
    start_urls = ["https://www.automobile.tn/fr/occasion"]
    custom_settings = {
        "DOWNLOAD_DELAY": 1.5,
        "CONCURRENT_REQUESTS": 2,
    }

    def parse(self, response):
        page_num = response.meta.get("page", 1)
        self.logger.info(f"--- Scraping page {page_num} ---")

        annonces = response.css("div.occasion-item-v2")

        if not annonces:
            self.logger.info("Aucune annonce trouvée, fin du scraping.")
            return

        for annonce in annonces:
            item = VoitureItem()
            item["titre"] = annonce.css("div.thumb-caption h2 ::text").get("").strip()
            lien_relatif = annonce.css("a.occasion-link-overlay::attr(href)").get()
            item["lien"] = response.urljoin(lien_relatif) if lien_relatif else ""
            item["image"] = annonce.css("img.thumb::attr(src)").get("")
            item["cote"] = annonce.css("div.cote-appreciation::text").get("").strip()
            item["kilometrage"] = " ".join(annonce.css("li.road::text").getall()).strip()
            item["annee"] = " ".join(annonce.css("li.year::text").getall()).strip()
            item["boite"] = " ".join(annonce.css("li.boite::text").getall()).strip()
            item["puissance"] = " ".join(annonce.css("li.horsepower::text").getall()).strip()
            item["energie"] = " ".join(annonce.css("li.fuel::text").getall()).strip()
            item["transmission"] = " ".join(annonce.css("li.transmission::text").getall()).strip()
            item["prix"] = " ".join(annonce.css("div.price::text").getall()).strip()
            item["page"] = page_num

            # Suivre le lien de l'annonce pour récupérer le Gouvernorat dans la page de détail
            if item["lien"]:
                yield response.follow(
                    item["lien"],
                    callback=self.parse_detail,
                    meta={"item": item}
                )
            else:
                item["gouvernorat"] = ""
                yield item

        # Pagination : chercher la page suivante
        next_page = response.css("a.next::attr(href)").get()
        if not next_page:
            next_page = response.css("ul.pagination li:last-child a::attr(href)").get()

        if next_page:
            self.logger.info(f"Page suivante trouvée : {next_page}")
            yield response.follow(
                next_page,
                callback=self.parse,
                meta={"page": page_num + 1},
            )

    def parse_detail(self, response):
        item = response.meta["item"]
        
        # Extraction du gouvernorat depuis la page de détail de la voiture
        gouvernorat = (
            response.xpath('.//li[span[contains(@class, "spec-name") and contains(text(), "Gouvernorat")]]/span[@class="spec-value"]/text()').get()
            or response.xpath('//span[contains(text(), "Gouvernorat")]/following-sibling::span/text()').get()
            or response.xpath('//*[contains(text(), "Gouvernorat")]/following::text()[1]').get()
            or ""
        )
        item["gouvernorat"] = gouvernorat.strip()
        
        yield item

from scrapy.crawler import CrawlerProcess
if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(OccasionSpider)
    process.start()