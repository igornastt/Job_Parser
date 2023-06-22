from configparser import ParsingError
import requests
from abstract import JobAPI
from pprint import pprint


class SuperJobApi(JobAPI):
    """ Класс для подключения к API superjob.ru"""
    url = "https://api.superjob.ru/2.0/vacancies/"

    def __init__(self, keyword):
        self.params = {
            "text": keyword,
            "area": False,
            "per_page": 100,
            "page": None,
        }
        self.headers = {
                        "X-Api-App-Id": "v3.r.137614145.cb26bfdfa58f9da553a2e2914a14330a40f30d5e.c39d10f2ffd5e1eae7f5da48af569f7b7a09b985"
        }
        self.vacancies = []

    def get_request(self):
        """Метод получения вакансий"""
        response = requests.get(self.url, headers=self.headers, params=self.params)
        if response.status_code != 200:
            raise ParsingError("Ошибка получения вакансий")
        return response.json()["objects"]

    def get_form_vacancies(self):
        """Метод форматирования вакансий"""
        form_vacancies = []

        for vacancy in self.vacancies:
            form_vacancy = {
                "employer": vacancy["firm_name"],
                "title": vacancy["profession"],
                "url": vacancy["link"],
                "api": "SuperJob",
                "salary_from": vacancy["payment_from"] if vacancy["payment_from"] and vacancy["payment_from"] != 0 else None,
                "salary_to": vacancy["payment_to"] if vacancy["payment_to"] and vacancy["payment_to"] != 0 else None,
            }
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

