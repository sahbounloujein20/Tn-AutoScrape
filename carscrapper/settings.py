BOT_NAME = "carscrapper"
SPIDER_MODULES = ["carscrapper.spiders"]
NEWSIPDER_MODULE = "carscrapper.spiders"

# Respecter robots.txt
ROBOTSTXT_OBEY = False   # automobile.tn bloque les bots via robots.txt

# Délai entre requêtes (soyez respectueux du serveur)
DOWNLOAD_DELAY = 2
CONCURRENT_REQUESTS = 1
DNS_RESOLVER = 'scrapy.resolver.CachingThreadedResolver'

DEFAULT_REQUEST_HEADERS = {
   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
   "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
}
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'


FEEDS = {
    "occasions.json": {"format": "json",      "encoding": "utf8", "overwrite": True},
    "occasions.csv":  {"format": "csv",                           "overwrite": True},
}


# Activer le pipeline
ITEM_PIPELINES = {
    'carscrapper.pipelines.NettoyagePipeline': 200,
    'carscrapper.pipelines.SQLServerPipeline': 400,
}

# Paramètres SQL Server
SQLSERVER_HOST = 'DESKTOP-6VJE48K'
SQLSERVER_PORT = 1433
SQLSERVER_DB = 'voitures_db'
