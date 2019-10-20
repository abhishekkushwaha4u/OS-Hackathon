from operator import itemgetter
import json
import os

# global slot
# global distance
# global parking_slot
# global car_list


current_directory = os.getcwd()


def car_list_updater_add(car, distance, parking_slot):
    if car not in car_list:
        car_list[car] = [distance, parking_slot]
    else:
        car_list[car].append([distance, parking_slot])

def car_list_updater_remove():
    pass

def car_list_initializer():
    with open('D:\Miscellaneous\Study and Interest\Python Projects\OS-Hackathon\car_parking\parking.txt', 'r') as e:
        name = e.readline()[6:].rstrip('\n')
        distance = list(map(int, e.readline()[11:].rstrip('\n').split(' ')))
        parking_slots = list(
            map(int, e.readline()[14:].rstrip('\n').split(' ')))
        car_list = {}
        car_list[name] = []
        for i in range(len(distance)):
            car_list[name].append([distance[i], parking_slots[i]])
        print(car_list)
        print(distance)
        print(parking_slots)

    
def parking_optimizer(mode, car_type):
    
               
    if mode == 'E':
        print(car_list[car_type])
        sorted(car_list[car_type], key = itemgetter(0))
        selected_position = car_list[car_type][0]
        print(selected_position)
        distance, token = selected_position
        car_list[car_type]= car_list[car_type][1:]
        print(3)
        print(car_list[car_type])
        return [distance, token]

    elif mode == 'L':
        pass`
    else:
        return None

print(parking_optimizer('E', 'SUV'))


