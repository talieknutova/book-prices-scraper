"""
Модуль скрапинга.
Собирает данные с целевого сайта и сохраняет их в CSV файл.
Настроен на дозапись, чтобы формировать временной ряд (time series).
"""
import csv
import logging
from datetime import datetime
from typing import List, Dict

import requests
from bs4 import BeautifulSoup

from src.config import TARGET_URL, RAW_DATA_FILE

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def fetch_page(url: str) -> str:
    """Загружает HTML страницу по URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logger.error(f"Ошибка при загрузке страницы {url}: {e}")
        raise


def parse_items(html: str) -> List[Dict[str, str]]:
    """Парсит HTML и извлекает нужные данные."""
    soup = BeautifulSoup(html, 'html.parser')
    items = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    articles = soup.find_all('article', class_='product_pod')
    
    for article in articles:
        try:
            title = article.h3.a['title']
            price_str = article.find('p', class_='price_color').text
            price = float(price_str.replace('£', '').replace('Â', '').strip())
            availability = article.find('p', class_='instock availability').text.strip()
            
            items.append({
                'timestamp': current_time,
                'title': title,
                'price': price,
                'availability': availability
            })
        except Exception as e:
            logger.warning(f"Ошибка при парсинге одного из элементов: {e}")
            continue
            
    return items


def save_to_csv(data: List[Dict[str, str]], filepath: str) -> None:
    """Сохраняет или дозаписывает данные в CSV."""
    if not data:
        logger.warning("Нет данных для сохранения.")
        return

    file_exists = filepath.exists()
    
    with open(filepath, mode='a', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['timestamp', 'title', 'price', 'availability'])
        if not file_exists:
            writer.writeheader()
        writer.writerows(data)
    
    logger.info(f"Успешно сохранено {len(data)} записей в {filepath}")


def run_scraper() -> None:
    """Основная точка входа для процесса скрапинга."""
    logger.info("Начало работы скрапера...")
    html = fetch_page(TARGET_URL)
    data = parse_items(html)
    save_to_csv(data, RAW_DATA_FILE)
    logger.info("Скрапинг успешно завершен.")


if __name__ == "__main__":
    run_scraper()