import carla
import numpy as np
import cv2

class Camera(object):
    def __init__(self, world, vehicle, camera_type, pos_x, pos_z, rotation_yaw=0, dim_x='640', dim_y='360'):
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
        with carla.CarlaSyncMode(self.world, self.camera) as sync_mode:
            while True:
                image = sync_mode.tick(timeout=2.0)[0]
                array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
                array = np.reshape(array, (image.height, image.width, 4))
                array = array[:, :, :3]
                array = cv2.cvtColor(array, cv2.COLOR_RGBA2BGR)
                cv2.imshow(window_name, array)
                if cv2.waitKey(1) == ord('q'):
                    break

        cv2.destroyAllWindows()
        self.camera.stop()