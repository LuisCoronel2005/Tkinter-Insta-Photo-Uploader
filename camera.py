import cv2
import os

class Camera:


    def __init__(self, drive):
        self.list = []
        self.drive = str(drive)
        if not os.path.exists(self.drive):
            os.makedirs(self.drive)
        self.vid = cv2.VideoCapture(0)
        self.current_frame = None

    def update_frame(self):
        ret, frame = self.vid.read()
        if ret:
            self.current_frame = frame
        return ret, frame

    def take_picture(self):
        
        if self.current_frame is not None:
            filename = os.path.join(self.drive, f"image_{len(os.listdir(self.drive)) + 1}.png")
            cv2.imwrite(filename, self.current_frame)
            self.list.append(filename)
            print(f"Saved {filename}")

    def release(self):
        self.vid.release()
        cv2.destroyAllWindows()
