from controller import Robot
import json
import csv
import os

#create the robot
robot = Robot()

timestep = int(robot.getBasicTimeStep()) #get time simulation interval
name = robot.getName()
robot_id = int(name[-1]) 

MAX_SPEED = 6.28

#cretate the log file 
project_folder = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

log_folder = os.path.join(
    project_folder, "data", "B1_swarm_logs"
)

os.makedirs(log_folder, exist_ok=True)

log_path = os.path.join(log_folder, "B1_" + name + ".csv")

log_file = open(log_path, "w", newline="", encoding="utf-8")
writer = csv.writer(log_file)

#column headings in the csv
writer.writerow([
    "time_s", "robot", "x", "y",
    "messages_sent", "messages_received",
    "front_left", "front_right", "escape_remaining"
])


#connects communication devices 
emitter = robot.getDevice("emitter")
receiver = robot.getDevice("receiver")
receiver.enable(timestep)

#connects 2 wheels
left_motor = robot.getDevice("left wheel motor")
right_motor = robot.getDevice("right wheel motor")

#set wheels to infinite rotation
left_motor.setPosition(float("inf"))
right_motor.setPosition(float("inf"))

left_motor.setVelocity(0)
right_motor.setVelocity(0)

#connect the 8 proximity sensors
sensors = []

for i in range(8):
    sensor = robot.getDevice("ps" + str(i)) #p0 - p7 are the sensors
    sensor.enable(timestep)
    sensors.append(sensor)

#connect GPS
gps = robot.getDevice("gps")

if gps is not None:
    gps.enable(timestep)


#robot variables
step_count = 0 #track simulation steps
messages_sent = 0 #track outgoing messages
messages_received = 0 #track incoming messages

#each robot starts with a different turning duration
turn_steps = [0, 30, 60, 90]
turn_remaining = turn_steps[robot_id - 1]

#tracks how many steps remain in an obstacle-avoidance routine
escape_remaining = 0

# Robots turn in opposite directions when needed
escape_turn = 1 if robot_id % 2 else -1

#obstacle detection settings
OBSTACLE_THRESHOLD = 80
SIDE_THRESHOLD = 120

FORWARD_SPEED = 3.0
TURN_SPEED = 3.0
REVERSE_SPEED = -3.0

#control motor speed
def set_speed(left_speed, right_speed):

    left_speed = max(-MAX_SPEED, min(MAX_SPEED, left_speed))
    right_speed = max(-MAX_SPEED, min(MAX_SPEED, right_speed))

    left_motor.setVelocity(left_speed)
    right_motor.setVelocity(right_speed)



#main robot loop
try:

    while robot.step(timestep) != -1:

        step_count += 1

        #read all 8 sensors
        values = []

        for sensor in sensors:
            values.append(sensor.getValue())

        #get front and side sensor readings
        front_right = max(values[0], values[1])
        front_left = max(values[6], values[7])

        right_side = values[2]
        left_side = values[5]

        #send messages
        if step_count % 15 == 0:

            message = {
                "robot": name,
                "step": step_count,
                "front_left": front_left,
                "front_right": front_right
            }

            if gps is not None:
                position = gps.getValues()
                message["position"] = [position[0], position[1]]

            emitter.send(json.dumps(message).encode("utf-8"))

            messages_sent += 1

        #recieve messages
        while receiver.getQueueLength() > 0:

            try:

                message = json.loads(receiver.getString())

                if message.get("robot") != name:
                    messages_received += 1

            except (ValueError, TypeError):

                print(name, "Invalid message received")

            receiver.nextPacket()
        
        #initial turning
        if turn_remaining > 0:

            left_speed = -2.0
            right_speed = 2.0

            turn_remaining -= 1

        #escape obstacles 
        elif escape_remaining > 0:

            if escape_remaining > 30:

                left_speed = REVERSE_SPEED
                right_speed = REVERSE_SPEED

            else:

                left_speed = -TURN_SPEED * escape_turn
                right_speed = TURN_SPEED * escape_turn

            escape_remaining -= 1

        #normal movement 
        else:

            obstacle = (
                front_left > OBSTACLE_THRESHOLD
                or front_right > OBSTACLE_THRESHOLD
                or right_side > SIDE_THRESHOLD
                or left_side > SIDE_THRESHOLD
            )

            if obstacle:

                left_obstacle = front_left + left_side
                right_obstacle = front_right + right_side

                if left_obstacle > right_obstacle:
                    escape_turn = -1

                elif right_obstacle > left_obstacle:
                    escape_turn = 1

                else:
                    escape_turn = 1 if robot_id % 2 else -1

                escape_remaining = 55

                left_speed = REVERSE_SPEED
                right_speed = REVERSE_SPEED

                print(name, "Avoiding obstacle")

            else:

                left_speed = FORWARD_SPEED
                right_speed = FORWARD_SPEED

        #move the robot
        set_speed(left_speed, right_speed)

        #save data to csv
        if step_count % 10 == 0: #save data every 10 steps

            if gps is not None:
                position = gps.getValues()
                x = position[0]
                y = position[1] #get robot coordinates
            else:
                x = ""
                y = ""

            writer.writerow([
                round(robot.getTime(), 3),
                name,
                x,
                y,
                messages_sent,
                messages_received,
                front_left,
                front_right,
                escape_remaining
            ])

            log_file.flush() #save

        #display in console every 100 steps
        if step_count % 100 == 0:

            print(
                name,
                "Steps:", step_count,
                "Sent:", messages_sent,
                "Received:", messages_received,
                "Escape:", escape_remaining
            )

finally:

    #stop both motors
    set_speed(0, 0)

    log_file.flush()
    log_file.close()

    print(name, "Controller stopped")
