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
#---------------------------TELEGRAM----------------------------------#
def telegram():
    base_url = "https://api.telegram.org/bot<your_bot_token>/sendMessage?chat_id=<chat_id>&text=Incendie"
    requests.get(base_url)
    print(base_url)
#------------------------------------------SMS  MESSAGE----------------------------------#
def send_sms():
    client = vonage.Client(key="********", secret="*******")
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
#--------------------ALARM SOUND--------------------------------#
def play_alarm_sound_function():
    pygame.mixer.init()
    s = pygame.mixer.Sound("C:\Users\Abdel\OneDrive\Bureau\Alter Ego - NTO.wav")
    s.play()

#----------------------FIRE DETECTION--------------------------------#
def detect_fire(frame):
    global Fire_Reported, Alarm_Status, sms, Telegram
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
        if not Alarm_Status:
            threading.Thread(target=play_alarm_sound_function).start()
            Alarm_Status = True
        if not sms:
            send_sms()
            sms = True
        if not Telegram:
            telegram()
            Telegram = True

#--------------------------------FIRE PREVISION----------------------------#


def main():
    video = cv2.VideoCapture('http://192.168.***:8080/video')
    while True:
        grabbed, frame = video.read()
        if not grabbed:
            break
        detect_fire(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            pygame.quit()
            break
    cv2.destroyAllWindows()
    video.release()

if __name__ == "__main__":
    main()

