from datetime import datetime, timedelta
from random import randrange
from pytz import timezone


class Timer:
    def __init__(self):
        self.__tz = timezone('Europe/Moscow')
        self.__reset_time = self.__str_to_time('23:48')
        self.__sent_max = 3
        self.sent_morning = False
        self.sent_day = False
        self.sent_evening = False


    def __get_random_time(self, start_time, end_time):
        start = self.__str_to_time(start_time)
        end = self.__str_to_time(end_time)
        delta = end - start
        random_second = randrange(delta.seconds)
        random_time = start + timedelta(seconds=random_second)
        return random_time

    def __str_to_time(self, str_time: str):
        time_obj = datetime.strptime(str_time, '%H:%M')
        time_to_eq = datetime(datetime.today().year,
                              datetime.today().month,
                              datetime.today().day,
                              time_obj.hour,
                              time_obj.minute, 0)
        return self.__tz.localize(time_to_eq)

    def check_time(self):
        self.__is_new_day()

        if self.__str_to_time('7:00').timestamp() <= datetime.now(self.__tz).timestamp() <= self.__str_to_time('9:00').timestamp() and not self.sent_morning:
            self.sent_morning = True
            return datetime.now(self.__tz), 'Утром'
        elif self.__str_to_time('12:00').timestamp() <= datetime.now(self.__tz).timestamp() <= self.__str_to_time('14:00').timestamp() and not self.sent_day:
            self.sent_day = True
            return datetime.now(self.__tz), 'Днем'
        elif self.__str_to_time('19:00').timestamp() <= datetime.now(self.__tz).timestamp() <= self.__str_to_time('21:00').timestamp() and not self.sent_evening:
            self.sent_evening = True
            return datetime.now(self.__tz), 'Вечером'
        return datetime.now(self.__tz), None

    def __is_new_day(self):
        if datetime.now().timestamp() > self.__reset_time.timestamp():
            self.__reset_time += timedelta(days=1)
            self.sent_morning = self.sent_day = self.sent_evening = False
            return True
        return False
