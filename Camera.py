import carla
import numpy as np
import cv2
from multiprocessing import Queue
class Camera(object):

    def __init__(self, world, vehicle, camera_type, pos_x, pos_z, image_queue,dim_x='640', dim_y='360'):
        self.world = world
        self.dim_x = dim_x
        self.dim_y = dim_y
        self.camera_type = camera_type
        self.pos_x = pos_x
        self.pos_z = pos_z
        self.image_queue = image_queue 
        self.camera_data = {'image': None}  

        
        camera_bp = self.world.get_blueprint_library().find(self.camera_type)
        camera_bp.set_attribute('image_size_x', self.dim_x)
        camera_bp.set_attribute('image_size_y', self.dim_y)

        
        camera_init_trans = carla.Transform(carla.Location(z=self.pos_z, x=self.pos_x))
        
       
        self.camera = self.world.spawn_actor(camera_bp, camera_init_trans, attach_to=vehicle)
        
        
        image_w = int(self.dim_x)
        image_h = int(self.dim_y)

        # Comienza a escuchar la cámara usando el callback proporcionado
        self.camera.listen(lambda image: self.callback(image))

    def render(self, window_name):
        while True:
            if not self.image_queue.empty():  # Verificar si hay una imagen en la cola
                self.camera_data['image'] = self.image_queue.get()  # Obtener la imagen de la cola
                cv2.imshow(window_name, self.camera_data['image'])
            else:
                #print("La imagen está vacía")  # Impresión para depuración
                pass

            # Rompe el bucle si el usuario presiona 'q'
            if cv2.waitKey(1) == ord('q'):
                break

        # Limpieza y cierre de recursos
        cv2.destroyAllWindows()
        self.camera.stop()  # Detiene la cámara

    def callback(self,image):
        array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
        array = np.reshape(array, (image.height, image.width, 4))
        array = array[:, :, :3]
        array = cv2.cvtColor(array, cv2.COLOR_RGBA2BGR)
        self.image_queue.put(array)  # Poner imagen en la cola


