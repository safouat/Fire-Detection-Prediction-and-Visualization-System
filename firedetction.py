import cv2
import numpy as np
import smtplib
import pygame
import threading
import vonage
import requests

Fire_Reported = 0
Email_Status = False
Alarm_Status = False
wtsp = False
Telegram = False
sms = False

def telegram():
    base_url = "https://api.telegram.org/bot5158217023:AAFVs40nhJmdvYx@qbkE3_8vJRGYMF06D8A/sendMessage?chat_id=-630103128>&text=Incendie"
    requests.get(base_url)
    print(base_url)

def SMS():
    client = vonage.Client(key="********", secret="edhWAJ5xMcrBIUTY")
    sms = vonage.Sms(client)
    responseData = sms.send_message(
        {
            "from": "Vonage APIs",
            "to": "212767790246",
            "text": "Attention!!! Un feu",
        }
    )
    if responseData["messages"][0]["status"] == "0":
        print("Message sent successfully.")
    else:
        print("Message failed with error:", responseData["messages"][0]["error-text"])

def play_alarm_sound_function():
    while True:
        pygame.mixer.init()
        s = pygame.mixer.Sound("C:\Users\Abdel\OneDrive\Bureau\Alter Ego - NTO.wav")
        s.play()

video = cv2.VideoCapture('http://192.168.43.29:8080/video')
while True:
    grabbed, frame = video.read()
    if not grabbed:
        break
    frame = cv2.resize(frame, (960, 540))
    blur = cv2.GaussianBlur(frame, (21, 21), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    lower = [18, 90, 180]
    upper = [35, 255, 255]
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    mask = cv2.inRange(hsv, lower, upper)
    output = cv2.bitwise_and(frame, hsv, mask=mask)
    no_red = cv2.countNonZero(mask)
    if int(no_red) > 15000:
        Fire_Reported += 1
    cv2.imshow("Detection du feu", output)
    if Fire_Reported >= 1:
        if Alarm_Status == False:
            threading.Thread(target=play_alarm_sound_function).start()
            Alarm_Status = True
        if sms == True:
            SMS()
            sms = True
        if Telegram == False:
            telegram()
            Telegram = True
    if cv2.waitKey(1) & 0xFF == ord('q'):
        pygame.quit()
        break
cv2.destroyAllWindows()
video.release()

