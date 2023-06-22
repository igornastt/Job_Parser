from abc import ABC, abstractmethod


class JobAPI(ABC):
    @abstractmethod
    def get_request(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass
