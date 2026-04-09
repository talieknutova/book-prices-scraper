"""
Модуль анализа данных.
Берет сырые данные, агрегирует их и строит графики.
"""
import logging
import pandas as pd
import matplotlib.pyplot as plt

from src.config import RAW_DATA_FILE, PLOT_FILE, SUMMARY_FILE

logger = logging.getLogger(__name__)

def run_analysis() -> None:
    """Основная функция анализа данных и генерации артефактов."""
    if not RAW_DATA_FILE.exists():
        logger.error(f"Файл с данными не найден: {RAW_DATA_FILE}")
        return

    logger.info("Начало анализа данных...")

    df = pd.read_csv(RAW_DATA_FILE)

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['date'] = df['timestamp'].dt.date
    
    summary = df.groupby('date').agg(
        avg_price=('price', 'mean'),
        total_items=('title', 'count')
    ).reset_index()

    summary.to_csv(SUMMARY_FILE, index=False)
    logger.info(f"Сводная таблица сохранена в {SUMMARY_FILE}")

    plt.figure(figsize=(10, 6))
    plt.plot(summary['date'], summary['avg_price'], marker='o', linestyle='-', color='b', label='Средняя цена')
    
    plt.title('Динамика средней цены по дням', fontsize=14)
    plt.xlabel('Дата', fontsize=12)
    plt.ylabel('Цена (£)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(PLOT_FILE)
    plt.close()
    logger.info(f"График сохранен в {PLOT_FILE}")
    logger.info("Анализ успешно завершен.")

if __name__ == "__main__":
    run_analysis()