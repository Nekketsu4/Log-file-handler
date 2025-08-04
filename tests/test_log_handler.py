import pytest
import json
from log_file_handler import LogHandler
from reports import report_total

testing_files = ['example1.log',]
testing_handler = LogHandler(*testing_files)
testing_handler.form_table('total')

@pytest.fixture()
def read_file():
    get_data = []
    for file in testing_files:
        with open(file, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                get_data.append(json.loads(line))
    return get_data


def test_input_files(read_file):
    """
    проверка на десериализацию файлов
    """
    assert testing_handler.content == read_file
    assert isinstance(testing_handler.content, list)


def test_add_report():
    """
    Метод содержит словарь, содержащий 2 экземпляра класса Report,
     которые формируют отчет total и avg_response_time,
     однако в этот словарь можно добавить функцию, либо класс для расширения
     формирующегося отчета
    """
    assert isinstance(testing_handler.add_report(), dict)
    assert len(testing_handler.add_report()) == 2

    '''добавили дополнительный класс в отчет'''
    testing_handler.add_report().update({'new_total': report_total.get_report(
        all_handlers=testing_handler.all_handlers, handlers=testing_handler.handlers)})

    assert len(testing_handler.add_report()) == 3


def test_form_table():
    """
    метод form_table возвращает функцию tabulate которая формирмирует словари, списки
    в удобочитаемую таблицу в строковом виде
    """
    assert isinstance(testing_handler.form_table(), str)
