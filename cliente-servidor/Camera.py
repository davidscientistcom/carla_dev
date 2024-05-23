import cv2
import numpy as np

class Camera(object):
    def __init__(self, queue, world, vehicle, camera_type, pos_x, pos_z, rotation_yaw=0, dim_x='640', dim_y='360'):
        self.queue = queue
        self.world = world
        self.dim_x = dim_x
        self.dim_y = dim_y
        self.camera_type = camera_type
        self.pos_x = pos_x
        self.pos_z = pos_z
        self.rotation_yaw = rotation_yaw

        image_w = int(self.dim_x)
        image_h = int(self.dim_y)

        camera_bp = self.world.get_blueprint_library().find(self.camera_type)
        camera_bp.set_attribute('image_size_x', self.dim_x)
        camera_bp.set_attribute('image_size_y', self.dim_y)

        camera_init_trans = carla.Transform(carla.Location(z=self.pos_z, x=self.pos_x), carla.Rotation(yaw=self.rotation_yaw))
        self.camera = self.world.spawn_actor(camera_bp, camera_init_trans, attach_to=vehicle)

    def render(self, window_name):
        while True:
            # Solicita los datos de la cámara al proceso servidor
            self.queue.put(('get_camera_data', self.camera))
            
            # Espera a recibir los datos de la cámara desde el proceso servidor
            camera_data = self.queue.get()
            
            # Procesa y muestra los datos de la cámara
            array = np.frombuffer(camera_data, dtype=np.dtype("uint8"))
            array = np.reshape(array, (int(self.dim_y), int(self.dim_x), 4))
            array = array[:, :, :3]
            array = cv2.cvtColor(array, cv2.COLOR_RGBA2BGR)
            cv2.imshow(window_name, array)
            
            # Rompe el bucle si el usuario presiona 'q'
            if cv2.waitKey(1) == ord('q'):
                break

        # Limpieza y cierre de recursos
        cv2.destroyWindow(window_name)
        self.camera.stop()