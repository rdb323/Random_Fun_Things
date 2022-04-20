import os, time
from playsound import playsound


def pingtest():
    has_internet = False
    while not has_internet:
        response = os.system("ping www.google.com")

        if response == 0:
            has_internet = True
        time.sleep(1)
    playsound('C:/Users/Ryan/Python_codebase/Internet_Alarm/FFVII.mp3')
    print("You now have internet, yay!")


if __name__ == '__main__':
    pingtest()