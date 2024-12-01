from sklearn.svm import LinearSVC
import numpy as np
import cv2 as cv
from PIL import Image

class Model:
    def __init__(self):
        self.model = LinearSVC()

    def train_model(self, counters):
        # Collect training data
        img_list = []
        class_list = []

        # Process class 1 images
        for i in range(1, counters[0]):
            img = cv.imread(f'1/frame{i}.jpg', cv.IMREAD_GRAYSCALE)  # Ensure grayscale
            if img is None:
                print(f"Warning: Unable to read image 1/frame{i}.jpg")
                continue
            img = img.flatten()  # Flatten the image
            img_list.append(img)
            class_list.append(1)

        # Process class 2 images
        for i in range(1, counters[1]):
            img = cv.imread(f'2/frame{i}.jpg', cv.IMREAD_GRAYSCALE)  # Ensure grayscale
            if img is None:
                print(f"Warning: Unable to read image 2/frame{i}.jpg")
                continue
            img = img.flatten()  # Flatten the image
            img_list.append(img)
            class_list.append(2)

        # Convert lists to numpy arrays
        img_list = np.array(img_list)
        class_list = np.array(class_list)

        # Train the model
        self.model.fit(img_list, class_list)
        print("Model successfully trained!")

    def predict(self, frame):
        # Convert frame to grayscale
        gray_frame = cv.cvtColor(frame[1], cv.COLOR_RGB2GRAY)

        # Resize to match training dimensions (e.g., thumbnail to 150x150)
        img = Image.fromarray(gray_frame)
        img.thumbnail((150, 150), Image.Resampling.LANCZOS)

        # Convert resized image to numpy array and flatten
        img = np.array(img).flatten()

        # Predict the class
        prediction = self.model.predict([img])

        return prediction[0]
