import time
import pytz
from Repository.Timer import Timer
from Repository.background import keep_alive
from Repository.Bot import Bot


def main():
    keep_alive()
    timer = Timer()
    telebot = Bot()
    telebot.start()
    while True:
        now, current_int = timer.check_time()
        print(now, current_int)
        if current_int:
            telebot.send_messages(current_int)
            timer.sent_today += 1
        time.sleep(60)


if __name__ == "__main__":
    main()
