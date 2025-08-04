from log_file_handler import LogHandler
from reports import report_total, report_avg

testing_log_handler = LogHandler('example1.log')

total = report_total.get_report(
    all_handlers=testing_log_handler.all_handlers,
    handlers=testing_log_handler.handlers
)
avg = report_avg.get_report(
    content=testing_log_handler.content,
    handlers=testing_log_handler.handlers
)

print(avg)

def test_total_report():
    """
    Метод возваращает список количества запросов на каждый эндпоинт
    :return: list
    """
    assert len(total) == 5
    assert isinstance(total, list)

def test_avg_report():
    """
    Метод возваращает список количества запросов на каждый эндпоинт
    :return: list
    """
    assert len(total) == 5
    assert isinstance(avg, list)
