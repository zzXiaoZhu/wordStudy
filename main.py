"""
此信息需要保留！

作者:zzXiaoZhu
github主页:https://github.com/zzXiaoZhu
仓库地址:https://github.com/zzXiaoZhu/wordStudy/
项目开发于2022年

"""



import tkinter.messagebox
import subprocess
import pygame
import random
import tkinter
import pyttsx3
import time
import threading
import sys

pygame.init()  # 初始化pygame
Clock = pygame.time.Clock()
Fps = 60
tts = pyttsx3.init()  # 初始化语音模型
vol = tts.getProperty('volume')
tts.setProperty('vol', vol + 50)

CapsLock = False  # 大写锁定
# 按钮事件列表
ButtonEventList = (
    pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r, pygame.K_t, pygame.K_y, pygame.K_u, pygame.K_i, pygame.K_o,
    pygame.K_p, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f, pygame.K_g, pygame.K_h, pygame.K_j, pygame.K_k,
    pygame.K_l, pygame.K_z, pygame.K_x, pygame.K_c, pygame.K_v, pygame.K_b, pygame.K_n, pygame.K_m, pygame.K_1,
    pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0,
    pygame.K_MINUS, pygame.K_EQUALS, pygame.K_LEFTBRACKET, pygame.K_RIGHTBRACKET, pygame.K_BACKSLASH,
    pygame.K_SEMICOLON, pygame.K_QUOTE, pygame.K_COMMA, pygame.K_PERIOD, pygame.K_SLASH, pygame.K_SPACE
)
# 小写列表
SmallWords = (
    "q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "a", "s", "d", "f", "g", "h", "j", "k", "l", "z", "x", "c", "v",
    "b", "n", "m", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "[", "]", "\\", ";", "'", ",", ".", "/",
    " "
)
# 大写列表
BigWords = (
    "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "A", "S", "D", "F", "G", "H", "J", "K", "L", "Z", "X", "C", "V",
    "B", "N", "M", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", "{", "}", "", ":", '"', "<", ">", "?",
    " "
)

UserInput = ""  # 用户输入
Wrong = False  # 正误
WrongTimes = 0  # 错误次数
Ans = False  # 给答案

# 隐藏Tkinter窗口
tk = tkinter.Tk()
tk.iconbitmap("Files\\Logo.ico")
tk.withdraw()


# 放Alpha音乐
def play_music():
    r = pygame.mixer.Sound("Files\\Alpha.mp3")
    r.set_volume(0.3)
    r.play(-1)


MusicThreading = threading.Thread(target=play_music)
MusicThreading.start()


# 保存内容函数
def SaveWordsFile():
    try:
        WordsFile = open("Words.txt", "w", encoding="UTF-8")
        for i in WordsList:
            pygame.event.get()
            pygame.display.update()
            WordsFile.write("{}|{}|{}\n".format(i[0], i[1], i[2]))
        WordsFile.close()
    except:
        pass


# 等待函数
def Wait(Time):
    t1 = time.time()
    while True:
        try:
            pygame.event.get()
            pygame.display.update()
        except:
            pass
        if time.time() - t1 > Time:
            return "Done"


# 新单词
def NewWord():
    global WordsIndex
    global StartTime
    global ReadNoRememberWordsNum
    if ReadNoRememberWordsNum == 0:
        # 想解决方案
        Temp = tkinter.messagebox.askyesno("单词通", "目前词库单词已背完，按“是”重背一遍，“否”更换新单词")
        if Temp:
            # 将Ture改为False
            for i in range(len(WordsList)):
                WordsList[i][2] = "False"
            ReadNoRememberWordsNum = len(WordsList)
            NewWord()
        else:
            subprocess.Popen("explorer /select,.\\Words.txt")
            Exit()
    else:
        # 随机新单词
        while True:
            TempIndex = random.randint(0, len(WordsList) - 1)
            if WordsList[TempIndex][2] == "False":
                break
        WordsIndex = TempIndex
        StartTime = time.time()
        Tempth = threading.Thread(target=say)
        Tempth.start()


# 检查单词
def CheckWord():
    if UserInput == WordsList[WordsIndex][0]:
        return True
    else:
        return False


# 念单词
def say():
    tts.say(WordsList[WordsIndex][0])
    tts.runAndWait()


# 关闭函数
def Exit():
    pygame.display.set_caption("正在保存数据中……")
    SaveWordsFile()
    sys.exit()
    time.sleep(0.5)
    exit()


# 按钮
def Button(XY, Event, ButtonImage):
    sc.blit(ButtonImage, (XY[0], XY[1]))
    MousePos = pygame.mouse.get_pos()
    for event in Event:
        if XY[0] < MousePos[0] < XY[2] and XY[1] < MousePos[1] < XY[3]:
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True


# 获取事件和打字模块
def GetEvent():
    global CapsLock
    event = pygame.event.get()
    for e in event:
        # 按下按钮
        if e.type == pygame.KEYDOWN:
            # Shift 按下
            if e.key == pygame.K_LSHIFT or e.key == pygame.K_RSHIFT:
                CapsLock = True
            # 大写锁定
            if e.key == pygame.K_CAPSLOCK:
                if CapsLock:
                    CapsLock = False
                else:
                    CapsLock = True
                return event, None
            # 回车
            elif e.key == pygame.K_RETURN:
                return event, "Enter"
            # 退格
            elif e.key == pygame.K_BACKSPACE:
                return event, "BackSpace"
            # 按键
            else:
                for i in range(len(ButtonEventList)):
                    if e.key == ButtonEventList[i]:
                        if CapsLock:
                            return event, BigWords[i]
                        else:
                            return event, SmallWords[i]
        # 弹起按钮
        elif e.type == pygame.KEYUP:
            # Shift 弹起
            if e.key == pygame.K_LSHIFT or e.key == pygame.K_RSHIFT:
                CapsLock = False
        # 关闭
        elif e.type == pygame.QUIT:
            Exit()

    return event, None


# 读取Words文件
def ReadWordsFile():
    try:
        global WordsList
        global ReadNoRememberWordsNum

        WordsFile = open("Words.txt", "r", encoding="UTF-8")
        WordsList = WordsFile.readlines()
        WordsFile.close()

        ReadNoRememberWordsNum = 0
        for i in range(len(WordsList)):
            WordsList[i] = WordsList[i].strip()
            WordsList[i] = WordsList[i].split("|")
            if WordsList[i][2] == "False":
                ReadNoRememberWordsNum += 1
    except UnicodeDecodeError:
        tkinter.messagebox.showerror("单词通", "请使用UTF-8编码保存Words.txt")
        Exit()
    except:
        tkinter.messagebox.showerror("单词通", "读取错误，检查文件吧")
        Exit()


ReadWordsFile()

pygame.display.set_caption("单词通")  # 名称
pygame.display.set_icon(pygame.image.load("Files\\Logo.ico"))
sc = pygame.display.set_mode((600, 500))  # 窗口

# 字体
WordsLineFont = pygame.font.Font("Files\\Misans.ttf", 20)  # 单词释义字体
InputLineFont = pygame.font.Font("Files\\Misans.ttf", 50)  # 用户输入字体
TimeFont = pygame.font.Font("Files\\Misans.ttf", 60)  # 剩余时间字体

# 图像
WordsLineImage = pygame.transform.scale(pygame.image.load("Files\\WordsLine.png"), (590, 70))  # 释义栏图像
InputLineImage = pygame.transform.scale(pygame.image.load("Files\\InputLine.png"), (560, 130))  # 输入栏图像
PointerImage = pygame.transform.scale(pygame.image.load("Files\\Pointer.png"), (30, 110))  # 光标图像
CapsLockTrueImage = pygame.transform.scale(pygame.image.load("Files\\CapsLockTrue.png"), (280, 85))  # CapsLock按下图像
CapsLockFalseImage = pygame.transform.scale(pygame.image.load("Files\\CapsLockFalse.png"), (300, 100))  # CapsLock未按下图像
EnterButtonImage = pygame.transform.scale(pygame.image.load("Files\\Enter.png"), (160, 160))  # Enter图像
ClockImage = pygame.transform.scale(pygame.image.load("Files\\Time.png"), (160, 160))  # 钟表图像

# 给个假像
sc.blit(pygame.image.load("Files\\FakeImage.png"), (0, 0))
pygame.display.update()

NewWord()
while True:
    event, TempInput = GetEvent()  # 获取事件

    sc.fill((242, 242, 242))  # 背景颜色

    sc.blit(WordsLineImage, (-1, 0))  # 释义显示屏幕图像
    sc.blit(WordsLineFont.render("{}".format(WordsList[WordsIndex][1]), True, (0, 200, 0)), (30, 29))  # 释义内容

    sc.blit(InputLineImage, (20, 80))  # 用户输入栏图像
    # 显示用户输入内容
    if not Wrong:
        UserInputText = InputLineFont.render("{}".format(UserInput), True, (0, 0, 0))
    else:
        UserInputText = InputLineFont.render("错误".format(UserInput), True, (255, 0, 0))
        if time.time() - WrongTime > 1:
            Wrong = False
    sc.blit(UserInputText, (30, 110))

    # 闪动输入光标
    if time.time() % 2 // 1 == 0:
        sc.blit(PointerImage, (UserInputText.get_size()[0] + 30, 88))

    TempEnter = Button((60, 220, 220, 380), event, EnterButtonImage)  # 显示回车按钮

    sc.blit(ClockImage, (370, 220))  # 钟表图像
    # 剩余秒数
    if 30 - int((time.time() - StartTime) // 1) < 0:
        Times = TimeFont.render(str(0), True, (0, 200, 0))
    else:
        Times = TimeFont.render(str(30 - int((time.time() - StartTime) // 1)), True, (0, 200, 0))
    TimesX = 450 - (Times.get_size()[0] / 2)  # 时间的X
    TimesY = 300 - (Times.get_size()[1] / 2)  # 时间的Y
    sc.blit(Times, (TimesX, TimesY))  # 显示剩余秒数

    # CapsLock按钮
    if CapsLock:
        sc.blit(CapsLockTrueImage, (162, 390))
    else:
        sc.blit(CapsLockFalseImage, (150, 380))

    pygame.display.update()

    # 给答案
    if 30 - int((time.time() - StartTime) // 1) <= 0 or WrongTimes >= 5:
        if not Ans:
            Wait(1)
            UserInput = WordsList[WordsIndex][0]
            Ans = 1
        elif Ans == 1:
            Ans = 2
        elif Ans == 2:
            Wait(3)
            Ans = 0
            NewWord()
            UserInput = ""
            WrongTimes = 0
            StartTime = time.time()

    if TempInput is not None and not TempInput == "Enter" and not TempInput == "BackSpace":
        UserInput += TempInput
    elif TempInput == "BackSpace":
        UserInput = UserInput[0:len(UserInput) - 1]
    elif TempInput == "Enter":
        TempEnter = True

    if TempEnter:
        Temp = CheckWord()
        UserInput = ""
        if Temp:
            if not WrongTimes >= 5 and not 30 - int((time.time() - StartTime) // 1) <= 0:
                WordsList[WordsIndex][2] = "True"
                ReadNoRememberWordsNum -= 1
                WrongTimes = 0
            NewWord()
        else:
            Wrong = True
            WrongTimes += 1
            WrongTime = time.time()
            StartTime = time.time()
            Tempth = threading.Thread(target=say)
            Tempth.start()

    Clock.tick(Fps)
