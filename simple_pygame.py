import pygame
import multiprocessing

class Window(object):
    def __init__(self, caption,size_x=800,size_y=600):
        self.size_x = size_x
        self.size_y = size_y
        self.caption = caption
             

    def show(self):
        running = True
        pygame.init()
        self.display = pygame.display.set_mode((self.size_x, self.size_y))
        pygame.display.set_caption(self.caption)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        pygame.quit()



if __name__ == "__main__":
    window1 = Window("Front Camera")
    window2 = Window("Back Camera")

    process1 = multiprocessing.Process(target=window1.show)
    process2 = multiprocessing.Process(target=window2.show)
    process1.start()
    process2.start()
    process1.join()
    process2.join()
