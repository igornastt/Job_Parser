from abc import ABC, abstractmethod


class JobAPI(ABC):
    """
    Абстрактный класс для работы с платформами по поиску вакансий по API.
    """
    @abstractmethod
    def get_vacancies(self):
        pass
