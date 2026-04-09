"""
Файл конфигурации проекта.
Здесь хранятся основные настройки, пути к файлам и URL для скрапинга.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
ARTIFACTS_DIR = DATA_DIR / "artifacts"

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

RAW_DATA_FILE = RAW_DATA_DIR / "scraped_data.csv"
SUMMARY_FILE = ARTIFACTS_DIR / "summary_stats.csv"
PLOT_FILE = ARTIFACTS_DIR / "price_trend.png"

TARGET_URL = "http://books.toscrape.com/catalogue/category/books/travel_2/index.html"
BASE_SITE_URL = "http://books.toscrape.com/catalogue/category/books/travel_2/"