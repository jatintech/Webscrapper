# Twitter Trending Scraper

This project automates the process of logging into Twitter (X.com), scraping trending hashtags, and storing the scraped data into a MongoDB collection.

## 📌 Features

- Logs into Twitter using Selenium and scrapes trending topics.
- Stores the scraped trends along with timestamp and UUID into a MongoDB collection.
- Utilizes a rotating proxy and customizable credentials.
- Saves the entire run as a JSON document.
- Headless configuration ready (optional).

## 🔧 Requirements

- Python 3.7+
- Chrome browser installed
- MongoDB running locally (or accessible via URI)
- Twitter credentials
- Proxy details (optional)

## 📦 Libraries Used

```bash
pip install selenium pymongo webdriver-manager
