from multiprocessing import Process
from Camera import Camera

class CameraManager(object):
    def __init__(self, queue, world, vehicle):
        self.queue = queue
        self.world = world
        self.vehicle = vehicle
        self.cameras = []
        self.processes = []

    def add_camera(self, camera_type, pos_x, pos_z, rotation_yaw=0, dim_x='640', dim_y='360'):
        camera = Camera(self.queue, self.world, self.vehicle, camera_type, pos_x, pos_z, rotation_yaw, dim_x, dim_y)
        self.cameras.append(camera)

    def execute(self):
        for i, camera in enumerate(self.cameras):
            window_name = f'Camera Feed {i}'
            p = Process(target=camera.render, args=(window_name,))
            self.processes.append(p)
            p.start()

    def join(self):
        for p in self.processes:
            p.join()
