import scrapy

class VoitureItem(scrapy.Item):
    titre        = scrapy.Field()
    prix         = scrapy.Field()
    annee        = scrapy.Field()
    kilometrage  = scrapy.Field()
    boite        = scrapy.Field()
    energie      = scrapy.Field()
    transmission = scrapy.Field()
    puissance    = scrapy.Field()
    carrosserie  = scrapy.Field()
    vendeur      = scrapy.Field()
    gouvernorat  = scrapy.Field()
    cote         = scrapy.Field()
    lien         = scrapy.Field()
    image        = scrapy.Field()
    page         = scrapy.Field()