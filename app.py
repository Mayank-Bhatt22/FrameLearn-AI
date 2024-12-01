import tkinter as tk
from tkinter import simpledialog
import cv2 as cv
import os
import PIL.Image, PIL.ImageTk
import camera
import model


class App:
    def __init__(self, window=tk.Tk(), window_title='Camera Classifier'):
        self.window = window
        self.window.title(window_title)

        # Initialize counters for saved images
        self.counters = [1, 1]

        # Initialize the model and camera
        self.model = model.Model()
        self.camera = camera.Camera()

        # Toggle for auto prediction
        self.auto_predict = False

        # Set up GUI components
        self.init_gui()

        # Delay for update loop
        self.delay = 15
        self.update()

        # Ensure the app window stays on top
        self.window.attributes('-topmost', True)
        self.window.mainloop()

    def init_gui(self):
        """Set up the graphical user interface."""
        # Canvas to display camera feed
        self.canvas = tk.Canvas(self.window, width=self.camera.width, height=self.camera.height)
        self.canvas.pack()

        # Buttons and labels
        self.btn_toggleauto = tk.Button(self.window, text="Auto Prediction", width=50, command=self.auto_predict_toggle)
        self.btn_toggleauto.pack(anchor=tk.CENTER, expand=True)

        self.classname_one = simpledialog.askstring("Classname One", "Enter the name of the first class:", parent=self.window)
        self.classname_two = simpledialog.askstring("Classname Two", "Enter the name of the second class:", parent=self.window)

        self.btn_class_one = tk.Button(self.window, text=self.classname_one, width=50, command=lambda: self.save_for_class(1))
        self.btn_class_one.pack(anchor=tk.CENTER, expand=True)

        self.btn_class_two = tk.Button(self.window, text=self.classname_two, width=50, command=lambda: self.save_for_class(2))
        self.btn_class_two.pack(anchor=tk.CENTER, expand=True)

        self.btn_train = tk.Button(self.window, text="Train Model", width=50, command=lambda: self.model.train_model(self.counters))
        self.btn_train.pack(anchor=tk.CENTER, expand=True)

        self.btn_predict = tk.Button(self.window, text="Predict", width=50, command=self.predict)
        self.btn_predict.pack(anchor=tk.CENTER, expand=True)

        self.btn_reset = tk.Button(self.window, text="Reset", width=50, command=self.reset)
        self.btn_reset.pack(anchor=tk.CENTER, expand=True)

        self.class_label = tk.Label(self.window, text="CLASS")
        self.class_label.config(font=("Arial", 20))
        self.class_label.pack(anchor=tk.CENTER, expand=True)

    def auto_predict_toggle(self):
        """Toggle automatic prediction."""
        self.auto_predict = not self.auto_predict

    def save_for_class(self, class_num):
        """Save images for the specified class."""
        ret, frame = self.camera.get_frame()
        if ret and frame is not None:
            directory = str(class_num)
            if not os.path.exists(directory):
                os.mkdir(directory)

            file_path = f'{directory}/frame{self.counters[class_num - 1]}.jpg'
            cv.imwrite(file_path, cv.cvtColor(frame, cv.COLOR_RGB2GRAY))

            # Resize and save thumbnail
            img = PIL.Image.open(file_path)
            img.thumbnail((150, 150), PIL.Image.Resampling.LANCZOS)
            img.save(file_path)

            self.counters[class_num - 1] += 1
        else:
            print("Failed to save the frame.")

    def reset(self):
        """Reset the saved data and counters."""
        for directory in ['1', '2']:
            if os.path.exists(directory):
                for file in os.listdir(directory):
                    file_path = os.path.join(directory, file)
                    if os.path.isfile(file_path):
                        os.unlink(file_path)

        self.counters = [1, 1]
        self.model = model.Model()
        self.class_label.config(text="CLASS")

    def update(self):
        """Update the GUI and process frames."""
        if self.auto_predict:
            self.predict()

        ret, frame = self.camera.get_frame()
        if ret and frame is not None:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(self.delay, self.update)

    def predict(self):
        """Predict the class of the current frame."""
        ret, frame = self.camera.get_frame()
        if ret and frame is not None:
            prediction = self.model.predict(frame)
            if prediction == 1:
                self.class_label.config(text=self.classname_one)
            elif prediction == 2:
                self.class_label.config(text=self.classname_two)
            else:
                self.class_label.config(text="Unknown")
        else:
            print("No frame available for prediction.")


# Ensure camera and model modules exist and are properly implemented
# If running this script, make sure the camera.py and model.py are in the same directory.
