import carla
import multiprocessing as mp
from CameraManager import CameraManager

def carla_server(queue):
    client = carla.Client('localhost', 2000)
    world = client.get_world()
    traffic_manager = client.get_trafficmanager()
    traffic_manager.set_synchronous_mode(True)

    # Inicializa y configura el mundo y el Traffic Manager aquí

    while True:
        request = queue.get()
        if request[0] == 'get_camera_data':
            camera = request[1]
            image = camera.shot().raw_data
            queue.put(image)
        # Maneja otras solicitudes de los clientes aquí

if __name__ == '__main__':
    queue = mp.Queue()
    server_process = mp.Process(target=carla_server, args=(queue,))
    server_process.start()

    client = carla.Client('localhost', 2000)
    world = client.get_world()
    vehicle = world.get_actors().filter('vehicle.*')[0]

    camera_manager = CameraManager(queue, world, vehicle)
    camera_manager.add_camera('sensor.camera.rgb', 2, 1, rotation_yaw=0)
    camera_manager.add_camera('sensor.camera.rgb', 2, 1, rotation_yaw=90)
    camera_manager.add_camera('sensor.camera.rgb', 2, 1, rotation_yaw=180)
    camera_manager.add_camera('sensor.camera.rgb', 2, 1, rotation_yaw=270)

    camera_manager.execute()
    camera_manager.join()