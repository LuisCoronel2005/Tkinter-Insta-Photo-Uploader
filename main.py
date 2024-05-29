import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from camera import Camera
from instagrapi import Client
import cv2

class Insta_Media:
    def __init__(self, username, password):
        self.cl = Client()
        self.username = username
        self.password = password

    def login(self):
        self.cl.login(self.username, self.password)
        print("Logged in successfully")

    def logout(self):
        self.cl.logout()
        print("Logged out successfully")

    def upload_post(self, photo_path, caption=""):
        try:
            self.cl.photo_upload(photo_path, caption)
            print("Post uploaded successfully")
        except Exception as e:
            print(f"An error occurred while uploading the post: {e}")

class CameraGUI:
    def __init__(self, camera, insta_media):
        self.camera = camera
        self.insta_media = insta_media
        self.root = tk.Tk()
        self.root.title("Camera GUI")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 12), background='white', foreground='black', padding=10)
        style.configure('TFrame', background='white')
        style.configure('TLabel', background='white')

        if not self.camera.vid.isOpened():
            error_label = ttk.Label(self.root, text="ERROR, NO CAM FOUND", style='TLabel')
            error_label.pack()
            return

        # Create a frame to hold the camera display
        camera_frame = ttk.Frame(self.root, style='TFrame')
        camera_frame.pack()
        self.camera_label = ttk.Label(camera_frame, style='TLabel')
        self.camera_label.pack()

        # Create a button to take a picture
        take_picture_button = ttk.Button(self.root, text="Take Picture", command=self.take_picture, style='TButton')
        take_picture_button.pack(pady=20)

        # Create a button to upload the last taken picture to Instagram
        upload_button = ttk.Button(self.root, text="Upload to Instagram", command=self.upload_to_instagram, style='TButton')
        upload_button.pack(pady=20)

        # Start updating frames
        self.update_frame()

        # Handle window close event to release camera resource
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Start the GUI loop
        self.root.mainloop()

    def update_frame(self):
        ret, frame = self.camera.update_frame()
        if ret:
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Convert the frame to a format Tkinter can handle
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            self.camera_label.imgtk = imgtk
            self.camera_label.configure(image=imgtk)
        self.root.after(10, self.update_frame)

    def take_picture(self):
        self.camera.take_picture()

    def upload_to_instagram(self):
        if self.camera.list:
            last_picture_path = self.camera.list[-1]
            self.insta_media.upload_post(last_picture_path, caption="Uploaded from my Camera GUI")
        else:
            print("No picture to upload")

    def on_closing(self):
        self.camera.release()
        self.insta_media.logout()
        self.root.destroy()

if __name__ == "__main__":
    filesave = "HERE GOES THE FOLDER YOU WANT TO SAVE IT TO"
    camera = Camera(filesave)
    insta_media = Insta_Media('your_username', 'your_password')
    insta_media.login()
    app = CameraGUI(camera, insta_media)
