from abc import ABC, abstractmethod
from decimal import Decimal


class Report(ABC):
    @abstractmethod
    def get_report(self, *args, **kwargs) -> list:
        """
        Метод генерации отчета
        :param: *args **kwargs
        :return: list
        """


class ReportTotal(Report):
    """
    Формирует список количества запросов на каждый эндпоинт
    """

    def get_report(self, *args, **kwargs) -> list:
        return [kwargs["all_handlers"].count(i) for i in kwargs["handlers"]]


class ReportAvg(Report):
    """
    Формирует список среднего времени отклика на каждый эндпоинт
    """

    def get_report(self, *args, **kwargs) -> list:
        response_time_list = []  # список 'response_time' на каждый эндпоинт
        avg_response_time_list = []
        for handler in kwargs["handlers"]:
            for line in kwargs["content"]:
                if handler in line["url"]:
                    response_time_list.append(line["response_time"])
            avg_response_time = Decimal(
                sum(response_time_list) / len(response_time_list)
            )
            rounded = avg_response_time.quantize(Decimal("1.000"))
            avg_response_time_list.append(rounded)
        return avg_response_time_list


report_total = ReportTotal()
report_avg = ReportAvg()
