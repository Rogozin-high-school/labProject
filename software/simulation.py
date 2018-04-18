import cv2
import numpy as np

class Display(object):

    def __init__(self, _name):
        self.screen = np.zeros((600, 800, 3), np.uint8)
        self.display = cv2.namedWindow(_name)
        self.name = _name
        self.renderers = []

    def add_render(self, renderer):
        self.renderers.append(renderer)

    def render(self):
        self.screen.fill(255)
        for r in self.renderers:
            self.screen = r(self.screen) or self.screen
        cv2.imshow(self.name, self.screen)

    def __del__(self):
        cv2.destroyWindow(self.name)
