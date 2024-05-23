#!/usr/bin/env python

# Copyright (c) 2019 Computer Vision Center (CVC) at the Universitat Autonoma de
# Barcelona (UAB).
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.


import carla
import pygame
import random
from MultiScreen import MultiScreenCamera
from CarlaSync import CarlaSyncMode

def should_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                return True
    return False


def main():
    actor_list = []
    pygame.init()
    clock = pygame.time.Clock()

    client = carla.Client('localhost', 2000)
    client.set_timeout(2.0)

    world = client.get_world()
    
    try:
        m = world.get_map()
        start_pose = random.choice(m.get_spawn_points())
        waypoint = m.get_waypoint(start_pose.location)

        blueprint_library = world.get_blueprint_library()

        vehicle = world.spawn_actor( world.get_blueprint_library().filter('vehicle.dodge.charger_police_2020')[0],
            start_pose)
        actor_list.append(vehicle)
        vehicle.set_simulate_physics(False)

        ms = MultiScreenCamera(world=world,vehicle=vehicle)

        

        # Create a synchronous mode context.
        with CarlaSyncMode(world, ms.cameras, fps=30) as sync_mode:
            while True:
                if should_quit():
                    return
                clock.tick()

                # Advance the simulation and wait for the data.
                ms.data = sync_mode.tick(timeout=2.0)

                # Choose the next waypoint and update the car location.
                waypoint = random.choice(waypoint.next(1.5))
                vehicle.set_transform(waypoint.transform)

                ms.draw()

                pygame.display.flip()

    finally:

        print('destroying actors.')
        for actor in actor_list:
            actor.destroy()

        pygame.quit()
        print('done.')


if __name__ == '__main__':

    try:

        main()

    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')