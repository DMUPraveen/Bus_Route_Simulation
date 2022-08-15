import cv2
import pygame


class Recorder:
    def __init__(self, width, height, fps, out_file='output.avi'):

        four_cc = cv2.VideoWriter_fourcc(*'XVID')
        self.video = cv2.VideoWriter(out_file, four_cc, float(fps), (width, height))

    def record_frame(self, surf):
        # transform the pixels to the format used by open-cv
        pixels = cv2.rotate(pygame.surfarray.pixels3d(surf), cv2.ROTATE_90_CLOCKWISE)
        pixels = cv2.flip(pixels, 1)
        pixels = cv2.cvtColor(pixels, cv2.COLOR_RGB2BGR)

        # write the frame
        self.video.write(pixels)

    def end_recording(self):
        # stop recording
        self.video.release()
