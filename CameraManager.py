from multiprocessing import Process
class CameraManager(object):
    def __init__(self):
        self.cameras = []
        self.processes = []
       

    def addCamera(self,camera):
        self.cameras.append(camera)

    def render(self,camera,window_name):
        camera.render(window_name)

    def show(self):
        for i in range(0,len(self.cameras)):
            p = Process(target=self.render,args=(self.cameras[i],'camara' + str(i)))
            self.processes.append(p)
            p.start()
    def join(self):
        for p in self.processes:
            p.join()

    

