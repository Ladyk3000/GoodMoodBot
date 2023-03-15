from datetime import datetime, timedelta
from random import randrange


class Timer:
    def __init__(self):
        self.__reset_time = '00:00'
        self.__sending_intervals = {'Утром': ['7:00', '10:00'],
                                    'Днем': ['11:12', '11:15'],
                                    'Вечером': ['19:00', '21:00']}
        self.__send_times = self.__generate_send_times()
        self.sent_today = 0
        self.__sent_max = len(self.__send_times)

    def __generate_send_times(self):
        tmp = {}
        for interval, times in self.__sending_intervals.items():
            tmp[interval] = self.__get_random_time(times[0], times[1])
        return tmp

    def __get_random_time(self, start_time, end_time):
        start = self.__str_to_time(start_time)
        end = self.__str_to_time(end_time)
        delta = end - start
        random_second = randrange(delta.seconds)
        random_time = start + timedelta(seconds=random_second)
        return random_time

    @staticmethod
    def __str_to_time(str_time: str):
        time_obj = datetime.strptime(str_time, '%H:%M')
        time_to_eq = datetime(datetime.today().year,
                              datetime.today().month,
                              datetime.today().day,
                              time_obj.hour,
                              time_obj.minute, 0)
        return time_to_eq

    def check_time(self):
        if self.__is_new_day():
            self.__generate_send_times()
        if datetime.now() > self.__send_times['Утром'] and self.sent_today == 0:
            return 'Утром'
        elif datetime.now() > self.__send_times['Днем'] and self.sent_today <= 1:
            return 'Днем'
        elif datetime.now() > self.__send_times['Вечером'] and self.sent_today <= 2:
            return 'Вечером'
        return None

    def __is_new_day(self):
        return self.sent_today == self.__sent_max and datetime.now() > self.__str_to_time(self.__reset_time)
