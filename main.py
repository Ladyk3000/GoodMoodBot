import time
from Repository.Timer import Timer
from Repository.background import keep_alive
from Repository.Bot import Bot


def main():
    keep_alive()
    timer = Timer()
    telegram_bot = Bot()
    telegram_bot.start()
    while True:
        now, current_interval = timer.check_time()
        print(now, current_interval)
        if current_interval:
            telegram_bot.send_messages(current_interval)
        time.sleep(600)


if __name__ == "__main__":
    main()
