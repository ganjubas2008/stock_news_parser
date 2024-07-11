import datetime


class NewsItem:
    def __init__(
        self,
        headline: str = '',
        text: str = '',
        date: datetime.datetime = datetime.date.fromisoformat('1970-01-01')
    ):
        self.headline = headline
        self.text = text
        self.date = date

    def __str__(self):
        return f'{self.headline} \n {self.text} \n {self.date}'
