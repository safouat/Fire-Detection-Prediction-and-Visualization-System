# Fire-detection-with-alarm-and-sms-System
Fire Detection System Implementation:
 The code uses OpenCV and other libraries to implement a fire detection system. It captures video, applies image processing techniques like Gaussian blur and color conversion, detects fire based on color thresholds, and counts the occurrences. If fire is detected, it plays an alarm sound, sends SMS notifications, and updates a Telegram channel. The code utilizes threading for parallel execution and supports video streaming.

    Video Capture:
    The system captures video input from a source, which could be a webcam or an IP camera. OpenCV's cv2.VideoCapture is used to retrieve frames from the video stream.

    Image Preprocessing:
    Before performing fire detection, the captured frames undergo preprocessing steps to enhance the quality of the image. This includes applying Gaussian blur to reduce noise and improve feature extraction.

    Color Conversion and Thresholding:
    The preprocessed frames are then converted from the RGB color space to the HSV (Hue-Saturation-Value) color space. This conversion helps to isolate the fire's color characteristics. The system applies color thresholding to identify pixels that fall within a specific color range associated with fire. This step is crucial for detecting fire regions in the image.

    Fire Detection and Counting:
    By analyzing the color thresholded image, the system counts the number of pixels that match the fire's color signature. If the count exceeds a predefined threshold, the system registers a "Fire Detected" event. The accumulation of fire detection events contributes to the tracking of fire occurrences over time.

    Alarm and Notification:
    When a fire is detected, the system responds with an alarm sound to alert the user. This is achieved using the pygame library, which plays an audio file. Additionally, the system sends SMS notifications to a designated phone number using the Vonage API. This ensures that relevant parties are informed promptly in case of a fire emergency.

    Telegram Channel Update:
    The system also utilizes the Telegram API to update a designated Telegram channel with a message indicating the occurrence of a fire. This provides an additional means of communication and allows stakeholders to stay informed.

    Parallel Execution with Threading:
    Threading is implemented to achieve parallel execution of certain tasks. For instance, the alarm sound is played in a separate thread, ensuring that it doesn't block the main program's execution. This approach enables the system to handle multiple tasks concurrently and maintain responsiveness.

    Video Streaming Support:
    The system supports video streaming by capturing frames from a specified video source, such as an IP camera. This feature extends the usability of the fire detection system to scenarios where real-time monitoring of remote locations is required.
![image](https://github.com/safouat/Fire-detection-with-alarm-and-sms-System/assets/120058233/cd471567-0678-4953-9b37-37674bd704f8)
![image](https://github.com/safouat/Fire-detection-with-alarm-and-sms-System/assets/120058233/7428ab0b-7e17-494a-abdd-a3dfe464f7b7)
![image](https://github.com/safouat/Fire-detection-with-alarm-and-sms-System/assets/120058233/aa7677dd-bc66-4443-99ef-0a9d5f4bef8e)
The code also includes a feature that empowers firefighters with predictive insights. By utilizing a machine learning technique known as k-nearest neighbors (KNN), firefighters can input geographical data about regions and receive predictions about the likelihood of fire occurrence. Here's an expanded explanation of how the prediction process works for firefighters:

Fire Prediction by Firefighters:
![image](https://github.com/safouat/Fire-Detection-Prediction-and-Visualization-System/assets/120058233/e4a2caad-9d54-4c5d-a73a-efe5e3841411)


    Dataset Collection:
    Firefighters have the ability to input data about various regions into the system. Each entry in the dataset contains two numerical values (X and Y coordinates) representing the geographical location, as well as an indicator of the region's state (burned or non-burned). The dataset serves as a training set for the prediction model.

    K-Nearest Neighbors (KNN) Algorithm:
    The prediction process relies on the KNN algorithm, a simple yet effective machine learning method. KNN considers the k-nearest data points (neighbors) to the given input when making a prediction. In this case, the algorithm will predict whether a region will experience a fire or not based on the state of its neighboring regions.

    Calculating Distances:
    For each region in the dataset, the algorithm calculates the Euclidean distance between the input region and the regions in the dataset. The Euclidean distance represents the "closeness" of two data points in a multi-dimensional space.

    Nearest Neighbors Selection:
    The KNN algorithm identifies the k-nearest regions with the smallest distances to the input region. These nearest neighbors are used to make a prediction about the input region's fire occurrence.

    Prediction Generation:
    The algorithm examines the states (burned or non-burned) of the k-nearest neighbors and determines the predominant state among them. The input region is then predicted to have the same state as the majority of its nearest neighbors.

    Visualization and Action:
    After generating predictions, the code visually presents the results on a graphical plot. Non-burned regions are typically represented in blue, while burned regions are represented in red. The user can observe the predicted states of various regions and assess the potential fire risk.
