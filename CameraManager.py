from multiprocessing import Process, Queue

class CameraManager(object):
    def __init__(self):
        self.cameras = []
        self.processes = []

    def addCamera(self, camera):
        self.cameras.append(camera)

    def execute(self):
        for i, camera in enumerate(self.cameras):
            p = Process(target=camera.render, args=('camara' + str(i),))
            self.processes.append(p)
            p.start()
            
    def join(self):
        for p in self.processes:
            p.join()