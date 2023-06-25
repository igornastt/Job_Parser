from headhunterh import HeadHunterAPI
from ison_job_file import JsonJobFile
from superjobh import SuperJobApi
from vacancy import Vacancy
from exception_job_parse_x import JobParseXNoObjectError, JobParseXNoDataError


class JobParseX:
    """
    Класс для взаимодействия с пользователем. Главная страница.
    """

    def __call__(self, *args, **kwargs) -> None:
        while True:
            self.title_page()
            try:
                command = int(input().strip())
                if command == 1:
                    Page1()()
                elif command == 2:
                    Page2()()
                elif command == 0:
                    print("Завершение работы программы")
                    exit()
                else:
                    raise ValueError
            except ValueError:
                print("Недопустимая команда")

    def title_page(self) -> None:
        """
        Описание первой страницы
        """
        print("JobParseX - программа для поиска и подбора вакансий\n", "_" * 50)
        print("Введите команду:\n"
              "1. - обновить базу данных с платформами\n"
              "2. - работа с вакансиями из базы данных\n"
              "0. - выход из приложения")

class Page1:
    """
    Класс для работы с вакансиями. Первая страница (api).
    """
    __slots__ = ("apis", "data", "path")

    def __init__(self) -> None:
        self.apis = [SuperJobApi, HeadHunterAPI]
        self.data = []
        self.path = [JsonJobFile]

    def __call__(self) -> None:
        while True:
            print("Вы выбрали запрос вакансий к платформам SuperJob и HeadHunter\n", "_" * 60)
            print("Введите команду:\n"
                  "1. - запрос к платформе SuperJob\n"
                  "2. - запрос к платформе HeadHunter\n"
                  "3. - запрос ко всем платформам\n"
                  "0. - назад")
            try:
                command = int(input().strip())
                if command == 1:
                    keywords = input("Введите поисковый запрос: ")
                    self.search_vacancies(self.apis[0](keywords=keywords))
                elif command == 2:
                    keywords = input("Введите поисковый запрос: ")
                    self.search_vacancies(self.apis[1](keywords=keywords))
                elif command == 3:
                    keywords = input("Введите поисковый запрос: ")
                    for api in self.apis:
                        self.search_vacancies(api(keywords=keywords))
                elif command == 0:
                    return
                else:
                    raise ValueError
            except ValueError:
                print("Недопустимая команда")

    def search_vacancies(self, api: object) -> None:
        """
        Функция для получения вакансий от api
        """
        api.get_vacancies()
        vacancies = api.vacancies
        self.data.clear()

        self.data.extend(vacancies)

        if len(self.data) > 0:
            print("Вакансии успешно загружены\n"
                  "1. - перезаписать базу данных\n"
                  "2. - добавить в базу данных\n"
                  "0. - выйти")
            user_choice = int(input().strip())

            if user_choice == 1:
                self.path[0]().add_vacancy(self.data, data_append=False)
            elif user_choice == 2:
                self.path[0]().add_vacancy(self.data, data_append=True)
            elif user_choice == 0:
                return
        else:
            print("Вакансия не найдена. Повторите запрос")

class Page2:
    """
    Класс для работы с вакансиями. Вторая страница (Vacancy).
    """

    def __init__(self) -> None:
        self.data = None
        self.path = JsonJobFile()
        self.vacancies = []

    def __call__(self) -> None:
        while True:
            print("Вы выбрали работу с вакансиями из базы данных\n", "_" * 50)
            print("Введите команду:\n"
                  "1. - загрузить вакансии из базы данных\n"
                  "2. - сортировать вакансии по зарплате\n"
                  "3. - сортировать вакансии по дате\n"
                  "4. - вывести топ N вакансий позарплате\n"
                  "5. - удалить вакансию по идентификатору\n"
                  "0. - назад")
            try:
                command = int(input().strip())
                if command == 1:
                    self.load_vacancies()
                elif command == 2:
                    self.sort_vacancy_payment()
                elif command == 3:
                    self.sort_vacancy_date()
                elif command == 4:
                    self.return_top_vacancies()
                elif command == 5:
                    self.delete_vacancy()
                elif command == 0:
                    return
                else:
                    raise ValueError
            except JobParseXNoObjectError:
                print("Вакансия не найдена, обновите базу данных или уточните запрос!!!\n", '_' * 60)
            except JobParseXNoDataError:
                print('\nЗагрузите вакансии из базы данных!!!\n', '_' * 50)
            except ValueError:
                print("Недопустимая команда")

    def load_vacancies(self) -> None:
        """
        Функция для поиска вакансий в файле
        """
        self.vacancies.clear()
        search_query = input("Введите поисковый запрос: ")
        data_tmp = self.path.get_vacancies(search_query=search_query)
        if len(data_tmp) > 0:
            for item in data_tmp:
                vacancy = Vacancy(item)
                if not any(v.id == vacancy.id for v in self.vacancies):
                    print(vacancy, "\n", "_" * 50)
                    self.vacancies.append(vacancy)
        else:
            raise JobParseXNoObjectError

    def sort_vacancy_payment(self) -> None:
        """
        Функция для сортировки вакансий по зарплате
        """
        if self.vacancies:
            self.vacancies.sort(key=lambda vacancy: vacancy.get_payment())
            for vacancy in self.vacancies:
                print('_' * 50)
                print(vacancy)
        else:
            raise JobParseXNoDataError

    def sort_vacancy_date(self) -> None:
        """
        Функция для сортировки вакансий по дате
        """
        if self.vacancies:
            self.vacancies.sort(key=lambda vacancy: vacancy.date_published, reverse=False)
            for vacancy in self.vacancies:
                print('_' * 50)
                print(vacancy)
        else:
            raise JobParseXNoDataError

    def return_top_vacancies(self):
        """
        Функция возвращает топ n вакансий, по зарплате
        """
        if self.vacancies:
            n = int(input("Введите количество вакансий: ").strip())
            self.vacancies.sort(key=lambda vacancy: vacancy.get_payment())
            if 0 < n <= len(self.vacancies):
                for i in range(n, len(self.vacancies)):
                    print('_' * 50)
                    print(self.vacancies[i])
            elif n > len(self.vacancies):
                print(f'Всего загружено вакансий - {len(self.vacancies)}')
                n = len(self.vacancies)
                for i in range(n):
                    print('_' * 50)
                    print(self.vacancies[i])
            else:
                print("Введите положительное число")
        else:
            raise JobParseXNoDataError

    def delete_vacancy(self) -> None:
        """
        Функция для удаления вакансий
        """
        if not self.vacancies:
            raise IndexError
        vacancy_id = input("Введите идентификатор вакансии для удаления: ").strip()
        try:
            if vacancy_id.isdigit():
                deleted_vacancies = []
                filtered_vacancies = filter(lambda vacancy: int(vacancy.id) == int(vacancy_id), self.vacancies)
                for vacancy in filtered_vacancies:
                    deleted_vacancies.append(vacancy)
                    self.path.remove_vacancy(vacancy_id=vacancy_id)
                    print(f"Вакансия успешно удалена из загруженных")

                if len(deleted_vacancies) > 0:
                    self.vacancies = [v for v in self.vacancies if v not in deleted_vacancies]
                else:
                    raise ValueError("Вакансия не найдена. Введите корректный идентификатор вакансии.")
            else:
                raise ValueError("Идентификатор вакансии должен состоять только из цифр.")
        except ValueError as error:
            print(str(error))


if __name__ == "__main__":
    JobParseX()()
