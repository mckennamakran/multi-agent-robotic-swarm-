from controller import Robot
import os
import csv
import json

#initialize the robot 
robot = Robot()
timestep = int(robot.getBasicTimeStep())

name = robot.getName()
robot_id = int(name[-1])

#communication devices
emitter = robot.getDevice("emitter")
receiver = robot.getDevice("receiver")
receiver.enable(timestep)

#wheel data
left = robot.getDevice("left wheel motor")
right = robot.getDevice("right wheel motor")

left.setPosition(float("inf"))
right.setPosition(float("inf"))
left.setVelocity(0.0)
right.setVelocity(0.0)



#consensus experiment begins
#each robot starts with a different numerical value 

initial_values = {
    1: 10.0,
    2: 20.0,
    3: 30.0,
    4: 40.0
}

value = initial_values[robot_id] #value specific to each robot
target_average = 25.0


#data logs file
project_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

log_dir = os.path.join(
    project_dir, "data", "B2_consensus_logs"
)

os.makedirs(log_dir, exist_ok=True)

log_path = os.path.join(
    log_dir, f"B2_{name}.csv"
)

log_file = open(
    log_path, "w", newline="", encoding="utf-8"
)

writer = csv.writer(log_file)

writer.writerow([
    "iteration",
    "time_s",
    "robot",
    "consensus_value",
    "target_average",
    "absolute_error",
    "neighbours_received"
])

log_file.flush()


#display in console 
print(
    name,
    "STARTED | Initial value:",
    value,
    flush=True
)


iteration = 0 #tracks consensus rounds
cycle_steps = 20 #each round lasts 20 simulation steps 
step_count = 0 #counts simulation steps 
neighbour_values = {} #stores values recieved from other robots 

try:
    while robot.step(timestep) != -1:

        step_count += 1

        if step_count % cycle_steps == 1:

            neighbour_values = {}

            message = {
                "robot": name,
                "iteration": iteration,
                "value": value
            }

            emitter.send(
                json.dumps(message).encode("utf-8")
            )

        while receiver.getQueueLength() > 0:

            try:
                message = json.loads(
                    receiver.getString()
                )

                sender = message.get("robot")
                message_iteration = message.get("iteration")

                if (
                    sender != name
                    and message_iteration == iteration
                ):
                    neighbour_values[sender] = float(
                        message["value"]
                    )

            except (ValueError, TypeError, KeyError):
                pass

            receiver.nextPacket()

        #calculate the consensus value 
        if step_count % cycle_steps == 0:

            count = len(neighbour_values)

            if count == 3: #only calculates a new value if all 3 other robots have been heard 

                total = value + sum(
                    neighbour_values.values()
                ) #adds all values to its own 

                value = total / 4.0 #gets average 

            
            error = abs(value - target_average)

            writer.writerow([
                iteration,
                round(robot.getTime(), 3),
                name,
                round(value, 8),
                target_average,
                round(error, 8),
                count
            ])

            log_file.flush()

            print(
                name,
                "| Iteration:", iteration,
                "| Value:", round(value, 6),
                "| Error:", round(error, 6),
                "| Neighbours:", count,
                flush=True
            )

            iteration += 1

            if iteration >= 30:
                left.setVelocity(0.0)
                right.setVelocity(0.0)
                break

finally:
    log_file.close()

print(name, "CONSENSUS COMPLETE", flush=True)
