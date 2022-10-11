"""Задача №2.

В нашей школе мы не можем разглашать персональные данные пользователей, но чтобы преподаватель и ученик смогли объяснить нашей поддержке, кого они имеют в виду (у преподавателей, например, часто учится несколько Саш), мы генерируем пользователям уникальные и легко произносимые имена. Имя у нас состоит из прилагательного, имени животного и двузначной цифры. В итоге получается, например, "Перламутровый лосось 77". Для генерации таких имен мы и решали следующую задачу:
Получить с русской википедии список всех животных (https://inlnk.ru/jElywR) и вывести количество животных на каждую букву алфавита. Результат должен получиться в следующем виде:
А: 642
Б: 412
В:....

"""

import requests
from bs4 import BeautifulSoup as BS4


def parser() -> list:
    """Парсинг всех животных

    Returns:
        list: список всех животных
    """
    list_animals = parse_first_page()
    while True:
        list_animals += parse_all_other_pages(list_animals)
        if list_animals[-1].startswith('Я'):
            list_animals += parse_all_other_pages(list_animals)
            break
    return list_animals


def parse_first_page() -> list:
    """Получаем список животных с первой страницы

    Returns:
        list: первая часть списка животных, полученных с помощью парсера
    """
    BASE_URL = 'https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту'
    req = requests.get(BASE_URL)
    html_content = req.text
    parser = BS4(html_content, "html.parser")
    elements = parser.select("ul")
    list_animals = elements[2].text.split('\n')
    return list_animals


def parse_all_other_pages(list_animals: list) -> list:
    """Дополняем список животных с остальных страниц

    Args:
        list_animals (list): первая часть списка животных

    Returns:
        list: результирующий список животных
    """
    element = list_animals[-1].split()
    result = '+'.join(element)
    CURRENT_URL = f"https://ru.wikipedia.org/w/index.php?title=Категория:Животные_по_алфавиту&pagefrom={result}"
    req = requests.get(CURRENT_URL)

    html_content = req.text
    parser = BS4(html_content, "html.parser")
    elements = parser.select("ul")
    new_part_of_list_animals = elements[2].text.split('\n')
    
    if 'ЖивотныеОрганизмы по алфавиту' != elements[3].text:
        return new_part_of_list_animals + elements[3].text.split('\n')
    return new_part_of_list_animals


def counting_animals(list_animals: list) -> dict:
    """Подсчитываем число животных для каждой буквы и записываем в словарь

    Args:
        list_animals (list): список животных

    Returns:
        dict: число животных на каждую букву алфавита
    """
    dict_counting_animals = {}
    rus_alphabet = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О',
                    'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']
    count = 0
    for letter in rus_alphabet:
        for res in list_animals:
            if res.startswith(letter):
                count += 1
        dict_counting_animals[letter] = count
        count = 0
    return dict_counting_animals


def dict_to_correct_output(some_dict: dict) -> str:
    """Приводим словарь к заявленному в задаче виде

    Args:
        some_dict (dict): входной словарь

    Returns:
        str: выходная строка, соответствующая заявленному в задании виду
    """
    string_of_correct_output = ''
    for key, value in some_dict.items():
        string_of_correct_output += f"{key}: {value}\n"
    return string_of_correct_output


if __name__ == '__main__':
    list_animals = parser()
    dict_counting_animals = counting_animals(list_animals)
    output_str = dict_to_correct_output(dict_counting_animals)
    print(output_str)
