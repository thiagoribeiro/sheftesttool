try:
    from cv2 import cv
except Exception, e:
    import cv

class Camera(object):
    __instance = None

    def get_instance(self):
        if not Camera.__instance:
            Camera.__instance = Camera()
        return Camera.__instance
    get_instance = classmethod(get_instance)

    def __init__(self):
        self.capture = cv.CaptureFromCAM(0)
        if Camera.__instance:
            raise Camera.__instance
        Camera.__instance = self

    def get_image(self):
        frame = cv.QueryFrame(self.capture)
        if frame is None:
            return
        img_cv = frame
        image_rgb = cv.CreateImage((img_cv.width,img_cv.height), img_cv.depth, img_cv.channels)
        cv.CvtColor(img_cv,image_rgb, cv.CV_BGR2RGB)
        return image_rgb

    def save_frame(self, name):
        frame = cv.QueryFrame(self.capture)
        cv.SaveImage(name, frame)

