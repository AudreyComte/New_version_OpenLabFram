from time import sleep

from picamera import PiCamera

from action import Action


class Picture(Action):

    def __init__(self, contrast, brightness, saturation, delay, width, heigth):
        super().__init__()
        # self.camera = PiCamera()
        # self.contrast = contrast
        # self.brightness = brightness
        # self.saturation = saturation
        # self.delay = delay
        # self.width = width
        # self.heigth = heigth
        
    def toDo(self):
        pass
        # self.camera.contrast = self.contrast
        # self.camera.brightness = self.brightness
        # self.camera.saturation = self.saturation
        # self.camera.resolution = (self.width, self.heigth)
        # sleep(self.delay)
        # self.camera.start_preview()
        # sleep(2)  # Permet à la caméra de s'ajuster
        # self.camera.capture('/home/audrey/image123456.jpg')
        # self.camera.stop_preview()
        # print(f"La photo a été enregistrée")
        # self.camera.close()

    def info(self, ok):
        pass


