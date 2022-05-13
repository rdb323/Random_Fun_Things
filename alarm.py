import os, time
from playsound import playsound


def pingtest():
    has_internet = False
    while not has_internet:
        time.sleep(2)
        response = os.system("ping www.google.com")

        if response == 0:
            has_internet = True
        
    playsound('C:/Users/Ryan/Python_codebase/Internet_Alarm/FFVII.mp3')
    print("\r\nYou now have internet, yay!")


if __name__ == '__main__':
    #pingtest()
    
    a = 512
    a = a.to_bytes(2,'big')
    print(a)
    b = 64
    b = b.to_bytes(2,'big')
    print(b)
    
    for i in range(len(a)):
        print(format(a[i], "08b"))

    for i in range(len(b)):
        print(format(b[i], "08b"))
    
