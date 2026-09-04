# Tn-AutoScrape

**Used Car Market in Tunisia — scraping, database & Power BI dashboard**

TunisAutoScrape automatically collects used-car listings published on [automobile.tn](https://www.automobile.tn), stores them in a SQL Server database, and visualizes them in an interactive Power BI dashboard: price, fuel type, mileage, horsepower, gearbox, and distribution by governorate.

---

## 📊 Dashboard Preview

### Overview
![Overview](screenshots/page1-overview.png)

### Geographic Analysis
![Geographic Analysis](screenshots/page2-geography..png)

### Price Analysis
![Price Analysis](screenshots/page3-prix..png)

> 🎬 An animated demo of the interactive filters (fuel type, gearbox, governorate) is available at `screenshots/demo.gif`.

---

## ⚙️ How It Works

The project runs in 3 stages:

1. **Scraping** — A Scrapy spider crawls automobile.tn's listing pages (with automatic pagination) and follows each listing individually to extract its governorate.
2. **Cleaning & storage** — A pipeline cleans the fields (price, mileage, accent encoding) then inserts each listing into a SQL Server table, skipping duplicates.
3. **Visualization** — Power BI connects to the database and displays the data as a multi-page dashboard.

---

## 🗂️ Project Structure
