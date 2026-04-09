"""
Prefect Flow.
Оркестратор, который связывает скрапинг и анализ в единый пайплайн
и позволяет запускать их по расписанию.
"""
from prefect import flow, task
from src.scraper import run_scraper
from src.analyzer import run_analysis

@task(name="Scrape Data", retries=2, retry_delay_seconds=10)
def task_scrape_data():
    """Задача скрапинга с автоматическим ретраем при ошибках."""
    run_scraper()

@task(name="Analyze Data")
def task_analyze_data():
    """Задача анализа данных (выполняется после скрапинга)."""
    run_analysis()

@flow(name="Continuous Scraping Pipeline")
def main_flow():
    """Главный флоу процесса."""
    scrape_state = task_scrape_data()
    task_analyze_data(wait_for=[scrape_state])

if __name__ == "__main__":
    # Локальный запуск флоу для тестирования
    main_flow()
    
    # Раскомментируйте код ниже, чтобы создать локальный деплоймент
    # для регулярного запуска (например, каждые 10 минут)
    # from prefect.deployments import Deployment
    # from prefect.server.schemas.schedules import IntervalSchedule
    # from datetime import timedelta
    # deployment = Deployment.build_from_flow(
    #     flow=main_flow,
    #     name="scraper-deployment",
    #     schedule=IntervalSchedule(interval=timedelta(minutes=10)),
    # )
    # deployment.apply()