from datetime import datetime, timedelta
from random import randrange
from pytz import timezone


class Timer:
    def __init__(self):
        self.__tz = timezone('Europe/Moscow')
        self.__reset_time = '23:58'
        self.__sending_intervals = {'Утром': ['7:00', '9:00'],
                                    'Днем': ['12:00', '14:00'],
                                    'Вечером': ['19:00', '21:00']}
        self.__send_times = self.__generate_send_times()
        self.sent_today = 0
        self.__sent_max = len(self.__send_times)

    def __generate_send_times(self):
        tmp = {}
        for interval, times in self.__sending_intervals.items():
            tmp[interval] = self.__get_random_time(times[0], times[1])
        print(f'Times to send: {tmp}')
        return tmp

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
        if self.__is_new_day():
            self.__generate_send_times()

        print(self.__send_times['Днем'].timestamp())
        print(datetime.now(self.__tz).timestamp())

        print(self.__send_times['Днем'])
        print(datetime.now(self.__tz))

        if datetime.now(self.__tz).timestamp() > self.__send_times['Утром'].timestamp() and self.sent_today == 0:
            return datetime.now(self.__tz), 'Утром'
        elif datetime.now(self.__tz).timestamp() > self.__send_times['Днем'].timestamp() and self.sent_today <= 1:
            return datetime.now(self.__tz), 'Днем'
        elif datetime.now(self.__tz).timestamp() > self.__send_times['Вечером'].timestamp() and self.sent_today <= 2:
            return datetime.now(self.__tz), 'Вечером'
        return datetime.now(self.__tz), None

    def __is_new_day(self):
        return datetime.now().timestamp() > self.__str_to_time(self.__reset_time).timestamp()
