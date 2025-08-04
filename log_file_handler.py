import json
import argparse
from json import JSONDecodeError

from tabulate import tabulate
from reports import report_total, report_avg

class LogHandler:
    """
    Обработчик лог файлов формирующий отчеты в удобочитаемую таблицу
    """

    def __init__(self, *args):
        self._files: list[str] = list(args)
        self.content: list[dict] = list()
        self.all_reports: dict = dict()

        '''десериализация'''
        try:
            for file in self._files:
                with open(file, 'r', encoding='utf-8') as f:
                    for line in f.readlines():
                            self.content.append(json.loads(line))
        except JSONDecodeError as e:
            raise TypeError('Не верный формат файла')
        except FileNotFoundError:
            raise TypeError('Нет такого файла')

        self.all_handlers = [line_dict['url'] for line_dict in self.content] #полный список эндпоинтов
        self.handlers = list(set(self.all_handlers)) # список уникальных эндпоинтов

    def add_report(self) -> dict:
        """
        Метод содержит словарь, содержащий 2 экземпляра класса Report,
         которые формируют отчет total и avg_response_time,
         однако в этот словарь можно добавить функцию, либо класс для расширения
         формирующегося отчета
         :returns: dict
        """

        dict_reports = {
        'total': report_total.get_report(
                all_handlers=self.all_handlers,
                handlers=self.handlers,
            ),

        'avg_response_time': report_avg.get_report(
                handlers=self.handlers,
                content = self.content
            )
        }
        self.all_reports.update(dict_reports)
        return self.all_reports

    def form_table(self, *args) ->str:
        """
        метод form_table возвращает функцию tabulate которая формирмирует словари, списки
        в удобочитаемую таблицу в строковом виде
        :returns: str
        """
        columns = {'handler': self.handlers}
        for i in args:
            columns.update({i: self.add_report()[i]})
        return tabulate(columns, headers='keys')


parser = argparse.ArgumentParser()
parser.add_argument("--file", nargs="+", help='подгрузит файлы в экземпляр класса LogHandler')
parser.add_argument("--report", nargs="+", help="сформирует отчет исходя из переданных аргументов")

if __name__ == '__main__':
    get_args = parser.parse_args()
    if get_args.file:
        log = LogHandler(*get_args.file)
    if get_args.report:
        print(log.form_table(*get_args.report))
