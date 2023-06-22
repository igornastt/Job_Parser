from configparser import ParsingError
import requests
from abstract import JobAPI
from pprint import pprint


class HeadHunterAPI(JobAPI):
    """ Класс для подключения к API hh.ru"""
    url = "https://api.hh.ru/vacancies"

    def __init__(self, keyword):
        self.params = {
            "text": keyword,
            "area": False,
            "per_page": 100,
            "page": None,
        }
        self.headers = {"User-Agent": "MyImportantApp 1.0"}
        self.vacancies = []

    def get_request(self):
        """Метод получения вакансий"""
        response = requests.get(self.url, headers=self.headers, params=self.params)
        if response.status_code != 200:
            raise ParsingError("Ошибка получения вакансий")
        return response.json()["items"]

    def get_form_vacancies(self):
        """Метод форматирования вакансий"""
        form_vacancies = []

        for vacancy in self.vacancies:
            form_vacancy = {
                "url": vacancy["alternate_url"],
                "title": vacancy["name"],
                "employer": vacancy["employer"]["name"],
                "api": "HeadHunter",
            }
            salary = vacancy["salary"]
            if salary:
                form_vacancy["salary_to"] = salary["to"]
                form_vacancy["salary_from"] = salary["from"]
                form_vacancy["currency"] = salary["currency"]

            else:
                form_vacancy["salary_to"] = None
                form_vacancy["salary_from"] = None
                form_vacancy["currency"] = None
            form_vacancies.append(form_vacancy)

        return form_vacancies

    def get_vacancies(self, pages_count=4):
        self.vacancies = []   # Очищаем список вакансий
        for page in range(pages_count):
            page_vacancies = []
            self.params["page"] = page
            print(f"({self.__class__.__name__}) Парсинг страницы {page} -", end=" ")

            try:
                page_vacancies = self.get_request()
            except ParsingError as error:
                print(error)
            else:
                self.vacancies.extend(page_vacancies)
                print(f"Загружено вакансий: {len(page_vacancies)}")

            if len(page_vacancies) == 0:
                break
