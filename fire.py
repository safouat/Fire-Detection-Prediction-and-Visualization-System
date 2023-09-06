import cv2
import numpy as np
import smtplib
import pygame
import threading
import vonage
import requests
from math import sqrt

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

#--------------------------------FIRE PREVISION MODELISATION ----------------------------#


NON_brulee = 1
brulee = 0

def euclidean_distance(V1, V2):
    distance = 0.0
    for i in range(len(V1) - 1):
        distance += (V1[i] - V2[i]) ** 2
    return sqrt(distance)

def localisation_voisins(DATA, test_vecteur, num_neighbors):
    distances = []
    for DATA_vecteur in DATA:
        dist = euclidean_distance(test_vecteur, DATA_vecteur)
        distances.append((DATA_vecteur, dist))
    distances.sort(key=lambda tup: tup[1])
    
    voisins = []
    for i in range(num_neighbors):
        voisins.append(distances[i][0])
    return voisins

def predict_classification(train, test_row, num_voisin):
    voisins = localisation_voisins(train, test_row, num_voisin)
    classification = [row[-1] for row in voisins]
    prediction = max(set(classification), key=classification.count)
    return prediction

# Fonction pour saisir les données du dataset
def input_dataset():
    dataset = []
    while True:
        try:
            x = float(input("Entrez la valeur de x (ou un caractère pour quitter) : "))
            y = float(input("Entrez la valeur de y : "))
            etat = int(input("Entrez l'état (0 pour Non Brûlée, 1 pour Brûlée) : "))
            data_point = [x, y, etat]
            dataset.append(data_point)
        except ValueError:
            break
    return dataset

# Fonction pour tracer une courbe de points
def plot_points(x_values, y_values, color, marker, label):
    plt.scatter(x_values, y_values, color=color, marker=marker, label=label)

# Tracer la courbe avant la prédiction
def plot_before_prediction(dataset):
    x_non_brulee = []
    y_non_brulee = []
    x_brulee = []
    y_brulee = []
    for data_point in dataset:
        x, y, etat = data_point
        if etat == 0:
            x_non_brulee.append(x)
            y_non_brulee.append(y)
        else:
            x_brulee.append(x)
            y_brulee.append(y)

    plt.subplot(1, 2, 1)
    plot_points(x_non_brulee, y_non_brulee, color='blue', marker='o', label='Non Brûlée')
    plot_points(x_brulee, y_brulee, color='red', marker='x', label='Brûlée')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Avant la Prédiction')
    plt.legend()

# Tracer la courbe après la prédiction
def plot_after_prediction(dataset, num_neighbors):
    x_non_brulee_pred = []
    y_non_brulee_pred = []
    x_brulee_pred = []
    y_brulee_pred = []
    for data_point in dataset:
        x, y, etat = data_point
        prediction = predict_classification(dataset, data_point, num_neighbors)
        if prediction == 0:
            x_non_brulee_pred.append(x)
            y_non_brulee_pred.append(y)
        else:
            x_brulee_pred.append(x)
            y_brulee_pred.append(y)

    plt.subplot(1, 2, 2)
    plot_points(x_non_brulee_pred, y_non_brulee_pred, color='blue', marker='o', label='Non Brûlée (Prédiction)')
    plot_points(x_brulee_pred, y_brulee_pred, color='red', marker='x', label='Brûlée (Prédiction)')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Après la Prédiction')
    plt.legend()

def main():
    CHOICE==(who are you?firfighter or No)
    if (choice=="no")
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
    else:
    print("ENTER DATASET OF YOUR LOCALISATION:")
    dataset = input_dataset()


     num_neighbors = int(input("Enter K: "))


     plt.figure(figsize=(12, 6))
     plot_before_prediction(dataset)
     plot_after_prediction(dataset, num_neighbors)


    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()

