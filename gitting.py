
import os
import datetime
import time


def main():
    now = datetime.datetime.now()
    # now2 = datetime.datetime(year=2021, month=2, day=2, hour=24, minute=10, second=10)
    # print(now2)
    my_time = f"{now.year:04}-{now.month:02}-{now.day:02}_" \
              f"{now.hour:02}-{now.minute:02}-{now.second:02}"

    thing1 = " auto comment"
    my_commands = f"""
    git add --all
    git commit -m "{thing1} at {my_time}"
    """
    os.system(my_commands)
    last_sent = now
    while True:
        now = datetime.datetime.now()
        my_time = f"{now.year:04}-{now.month:02}-{now.day:02}_" \
                  f"{now.hour:02}-{now.minute:02}-{now.second:02}"
        if now.hour > last_sent.hour or (last_sent.hour == 23 and now.hour == 0):
            os.system(my_commands)
            last_sent = now
        time.sleep(5)
        print(my_time)


if __name__ == "__main__":
    main()
