from datetime import datetime


class Vacancy:
    """
    Класс для работы с вакансиями
    """
    __slots__ = ('id', "platform", "title", "company", "url", "area", "address", "candidat",
                 "vacancy_rich_text", "date_published", "payment", "priority")

    def __init__(self, vacancy: dict) -> None:
        try:
            if vacancy:
                self.platform = vacancy.get('platform', 'нет данных')
                self.id = vacancy.get("id")
                self.title = vacancy.get('title', 'нет данных')
                self.company = vacancy.get('company', 'нет данных')
                self.url = vacancy.get('url', 'нет данных')
                self.area = vacancy.get('area', 'нет данных')
                self.address = vacancy.get('address', 'нет данных')
                self.candidat = vacancy.get('candidat', 'нет данных')
                self.vacancy_rich_text = vacancy.get('vacancyRichText', 'нет данных')
                self.payment = vacancy.get('payment', 'нет данных')
                date_str = vacancy.get('date_published')
                self.date_published = datetime.strptime(date_str, '%Y.%m.%d %H:%M:%S')
                self.priority = False
            else:
                raise ValueError("Недопустимые данные о вакансии")
        except ValueError as error:
            print(str(error))

    def __str__(self) -> str:
        return f'id: {self.id}\n' \
               f'Title: {self.title}\n' \
               f'Payment: {self.get_payment()} {self.payment["currency"]}\n' \
               f'Area: {self.area}\n' \
               f'URL: {self.url}\n' \
               f'Date: {self.date_published}\n' \
               f'Platform: {self.platform}'

    def __lt__(self, other: object) -> bool:
        """
        Переопределенный метод для сравнения зарплат экземпляров класса
        """
        if isinstance(other, Vacancy):
            payment_1 = self.get_payment()
            payment_2 = other.get_payment()
            return payment_1 < payment_2

    def get_payment(self) -> int:
        """
        Для получения зарплаты экземпляров класса
        """
        payment_from = int(self.payment.get("from", 0))
        payment_to = int(self.payment.get('to', 0))
        if payment_to > 0 and payment_from > 0:
            payment = (payment_to + payment_from) / 2
        elif payment_from == 0:
            payment = payment_to
        else:
            payment = payment_from
        return payment
