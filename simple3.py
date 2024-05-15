import carla 
import numpy as np
import cv2
from threading import Thread, Lock

# Clase Camera
class Camera(object):
    def __init__(self, world, vehicle, camera_type, pos_x, pos_z, callback, dim_x='640', dim_y='360'):
        self.world = world
        self.dim_x = dim_x
        self.dim_y = dim_y
        self.camera_type = camera_type
        self.pos_x = pos_x
        self.pos_z = pos_z
        self.callback = callback

        camera_bp = self.world.get_blueprint_library().find(self.camera_type)
        camera_bp.set_attribute('image_size_x', self.dim_x)
        camera_bp.set_attribute('image_size_y', self.dim_y)

        camera_init_trans = carla.Transform(carla.Location(z=self.pos_z, x=self.pos_x))

        self.camera = self.world.spawn_actor(camera_bp, camera_init_trans, attach_to=vehicle)

        image_w = int(self.dim_x)
        image_h = int(self.dim_y)
        self.camera_data = {'image': np.zeros((image_h, image_w, 4))}
        self.lock = Lock()

        # Comienza a escuchar la cámara usando el callback proporcionado
        self.camera.listen(lambda image: self.callback(image, self.camera_data, self.lock))

    def render(self, window_name):
        while True:
            with self.lock:
                cv2.imshow(window_name, self.camera_data['image'])
            # Rompe el bucle si el usuario presiona 'q'
            if cv2.waitKey(1) == ord('q'):
                break

        # Limpieza y cierre de recursos
        cv2.destroyWindow(window_name)
        self.camera.stop()  # Detiene la cámara

# Clase CameraManager
class CameraManager(object):
    def __init__(self):
        self.cameras = []

    def addCamera(self, camera):
        self.cameras.append(camera)

    def show(self):
        for i, camera in enumerate(self.cameras):
            window_name = f'Camera {i+1}'
            t = Thread(target=camera.render, args=(window_name,))
            t.start()

# Callback de la cámara
def camera_callback(image, data_dict, lock):
    with lock:
        data_dict['image'] = np.reshape(np.copy(image.raw_data), (image.height, image.width, 4))

# Conexión al simulador
client = carla.Client('localhost', 2000)
client.set_timeout(60.0)
world = client.get_world()
spawn_points = world.get_map().get_spawn_points()

# Busca un vehículo Mini
vehicle_bp = world.get_blueprint_library().filter('*mini*')
start_point = spawn_points[0]
vehicle = world.try_spawn_actor(vehicle_bp[0], start_point)

# Activa el piloto automático
vehicle.set_autopilot(True)

# Crear cámaras y manager
cm = CameraManager()
c1 = Camera(world, vehicle, "sensor.camera.rgb", 1.6, 0.9, camera_callback)
c2 = Camera(world, vehicle, "sensor.camera.rgb", -10, 0.9, camera_callback)
cm.addCamera(c1)
cm.addCamera(c2)

# Mostrar cámaras
cm.show()
