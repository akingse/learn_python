# 状态机
from time import sleep
import win32con
import win32api

record = 0
while True:
    # getKey1 = win32api.GetAsyncKeyState(win32con.VK_ESCAPE)
    getKey1 = win32api.GetAsyncKeyState(win32con.VK_F1)
    getKey1 = win32api.GetAsyncKeyState(win32con.VK_DOWN)
    # getKey1 = win32api.GetAsyncKeyState(win32con.VK_SHIFT)
    if record != getKey1:
        print(getKey1)
        record = getKey1


# stateEnum = str()
stateEnum = ['close', 'smart', 'speed_1', 'speed_2', 'speed_3']
# state = 'close'
'''
smart
speed_1
speed_2
speed_3
close
'''


def is_botton_down():
    # if pin==1:
    # sleep()
    # if pin == 1:
    # return True
    # else:
    # return False
    return True


def event_close():
    print('close')


def event_smart():
    print('smart')


def event_speed_1():
    print('speed_1')


def event_speed_2():
    print('speed_2')


def event_speed_3():
    print('speed_3')


funList = [event_close, event_smart,
           event_speed_1, event_speed_2, event_speed_3]

# input = 11
i = 0
while True:
    sleep(1)
    # tip = input("请输入文字：")
    if is_botton_down():  # 事件
        # if tip:
        i += 1
        i = i % 5
        print(i)
        state = stateEnum[i]
        # funList[i]()

        # print(state)
        if state == "smart":
            event_smart()
        elif state == "speed_1":
            event_speed_1()
        elif state == "speed_2":
            event_speed_2()
        elif state == "speed_3":
            event_speed_3()
        else:
            event_close()
