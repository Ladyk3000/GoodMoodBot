import time
from Repository.Timer import Timer
from Repository.background import keep_alive
from Repository.Bot import Bot


def main():
    keep_alive()
    timer = Timer()
    telebot = Bot()
    telebot.start()
    while True:
        current_interval = timer.check_time()
        print(current_interval)
        if current_interval:
            telebot.send_messages(current_interval)
            timer.sent_today += 1
        time.sleep(10)


if __name__ == "__main__":
    main()
