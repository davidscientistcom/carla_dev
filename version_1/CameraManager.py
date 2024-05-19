from multiprocessing import Process, Queue
import cv2

class CameraManager(object):
    def __init__(self):
        self.cameras = []
        self.processes = []
        self.image_queue = Queue()  # Cola para las imágenes

    def addCamera(self, camera):
        self.cameras.append(camera)

    def render(self, camera, window_name):
        while True:
            if not self.image_queue.empty():
                image = self.image_queue.get()  # Obtener imagen de la cola
                cv2.imshow(window_name, image)
                if cv2.waitKey(1) == ord('q'):
                    break
        cv2.destroyAllWindows()

    def show(self):
        for i, camera in enumerate(self.cameras):
            image_queue = Queue()  # Crear una cola para cada cámara
            camera.image_queue = image_queue  # Asignar la cola a la cámara
            p = Process(target=camera.render, args=('camara' + str(i),))
            self.processes.append(p)
            p.start()
            
    def join(self):
        for p in self.processes:
            p.join()