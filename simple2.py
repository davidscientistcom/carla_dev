import carla 
import numpy as np
from Camera import Camera
from CameraManager import CameraManager
import cv2

# connect to the sim
client = carla.Client('localhost', 2000)
client.set_timeout(60.0)

# optional to load different towns
#client.set_timeout(15)
client.load_world('Town04')

#define environment/world and get possible places to spawn a car
world = client.get_world()
spawn_points = world.get_map().get_spawn_points()

#look for a blueprint of Mini car
vehicle_bp = world.get_blueprint_library().filter('*mini*')

#spawn a car in a random location
start_point = spawn_points[0]
vehicle = world.try_spawn_actor(vehicle_bp[0], start_point)

# move simulator view to the car
spectator = world.get_spectator()
start_point.location.x = start_point.location.x+2 #start_point was used to spawn the car but we move 1m up to avoid being on the floor
start_point.location.z = start_point.location.z+2
spectator.set_transform(start_point)

#send the car off on autopilot - this will leave the spectator
vehicle.set_autopilot(True)




c1 = Camera(world,vehicle,"sensor.camera.rgb",1.6,0.9)
c2 = Camera(world,vehicle,"sensor.camera.rgb",-5,-9)

cm = CameraManager()
cm.addCamera(c1)
cm.addCamera(c2)
cm.show()
cm.join()

len(spawn_points)

start_point = spawn_points[0]
spectator = world.get_spectator()
spectator.set_transform(start_point)

spectator.set_transform(carla.Transform(carla.Location(x=-1085.286377, y=3112.225830, z=356.060608), carla.Rotation(pitch=1.648070, yaw=20.234367, roll=0.000000)))

print(start_point)