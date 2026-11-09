from controller import Robot
import os
import json
import csv
import math

#initialize 
robot = Robot()
timestep = int(robot.getBasicTimeStep())
name = robot.getName()
robot_id = int(name[-1])


#file logs
BASE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

DATA = os.path.join(BASE, "data", "B4_neural_logs")
os.makedirs(DATA, exist_ok=True)


#open the model
with open(os.path.join(DATA, "B4_model.json")) as f:
    model = json.load(f)

#initilize 
weights = model["weights"] #how important value is to the output
biases = model["biases"] #constant value that can act like a boost

#wheels
left = robot.getDevice("left wheel motor")
right = robot.getDevice("right wheel motor")

left.setPosition(float("inf"))
right.setPosition(float("inf"))
left.setVelocity(0)
right.setVelocity(0)

#gps setup
gps = robot.getDevice("gps")
gps.enable(timestep)

#8 sensor readings 
sensors = []

for i in range(8):
    sensor = robot.getDevice("ps" + str(i))
    sensor.enable(timestep)
    sensors.append(sensor)

log = open(
    os.path.join(DATA, "B4_" + name + ".csv"),
    "w", newline="", encoding="utf-8"
)

writer = csv.writer(log)

writer.writerow([
    "time_s", "robot", "x", "y",
    "left_sensor", "right_sensor",
    "prediction", "obstacle_detected"
])

#begin neural network

def predict(features): #takes the sensor data that has been converted into input features
    output = features

    #goes through each layer
    for layer in range(len(weights)): #weights contains the learned connections between neuron
        result = []

        #each bias
        for j in range(len(biases[layer])):
            value = biases[layer][j]

            #for every input, * weight and add it to the neurons existing value
            for i in range(len(output)):
                value += output[i] * weights[layer][i][j]

            if layer < len(weights) - 1:
                value = max(0.0, value)

            result.append(value)

        output = result #repeats until every layer has been processed

    return output.index(max(output))

#robot variables setup
step = 0
action = 0

mode = "forward"
mode_until = 0.0
turn_direction = 1

last_position = None
last_check = 0.0
cooldown_until = 0.0

print(name, "NEURAL STARTED", flush=True)

try:
    while robot.step(timestep) != -1: #while still active

        step += 1
        now = robot.getTime() #get time

        #get gps position
        position = gps.getValues()
        x = float(position[0])
        y = float(position[1])

        #checks if gps coordinates are valid numbers
        if not (math.isfinite(x) and math.isfinite(y)):
            left.setVelocity(0) #if incorrect then both wheels stop
            right.setVelocity(0)
            continue

        #get all proximity sensor readings 
        values = [s.getValue() for s in sensors]

        #selects 4 sensor readings and takes the highest from each pair
        front_left = max(values[6], values[7])
        front_right = max(values[0], values[1])

        #values to be given to the neural network
        features = [
            min(front_left / 150.0, 1.0),
            min(front_right / 150.0, 1.0)
        ]

        #runs at steps 1, 11, 21 (wherever theres a remainder of 1)
        if step % 10 == 1:
            action = predict(features)

        obstacle = max(front_left, front_right) > 80 #check if obstacle is nearby

        #wait for robot to finish reversing or turning
        if mode == "reverse" and now >= mode_until:
            mode = "turn"
            mode_until = now + 1.0

        elif mode == "turn" and now >= mode_until:
            mode = "forward"
            cooldown_until = now + 0.8

        if mode == "forward":

            if obstacle and now >= cooldown_until:
                mode = "reverse"
                mode_until = now + 0.35
                turn_direction = -1 if front_left > front_right else 1

            #check whether obstacle is stuck (so if theyre in the same position for more than 2.5 seconds)
            elif now - last_check >= 2.5:
                
                #calculates how far the robot has travelled since the previous check
                if last_position is not None:
                    moved = math.hypot(
                        x - last_position[0],
                        y - last_position[1]
                    )
                    
                    #f the robot has travelled less than 0.05 metres (5 centimetres), the code assumes it might be stuck
                    if moved < 0.05:
                        mode = "reverse" #starts reversing
                        mode_until = now + 0.4
                        turn_direction = 1 if robot_id % 2 else -1 #choses direction based on ID

                last_position = [x, y]
                last_check = now

        #connvert decisions to actual moverment
        if mode == "reverse":
            ls, rs = -3.0, -3.0

        elif mode == "turn":
            ls = -2.5 * turn_direction
            rs = 2.5 * turn_direction

        elif action == 1:
            ls, rs = 2.8, 4.0

        elif action == 2:
            ls, rs = 4.0, 2.8

        else:
            ls, rs = 3.8, 3.8

        left.setVelocity(ls)
        right.setVelocity(rs)

        #logs
        if step % 10 == 0:
            writer.writerow([
                round(now, 3),
                name,
                round(x, 6),
                round(y, 6),
                round(front_left, 3),
                round(front_right, 3),
                action,
                int(obstacle)
            ])
            log.flush()

        if now >= 90: #seconds
            break

finally:
    left.setVelocity(0)
    right.setVelocity(0)
    log.close()

print(name, "NEURAL COMPLETE", flush=True)
