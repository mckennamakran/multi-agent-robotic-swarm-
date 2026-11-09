
from controller import Robot
import os
import csv
import json
import math
import random

robot = Robot()
timestep = int(robot.getBasicTimeStep())
name = robot.getName()
robot_id = int(name[-1])
random.seed(100 + robot_id)

left = robot.getDevice("left wheel motor")
right = robot.getDevice("right wheel motor")
left.setPosition(float("inf"))
right.setPosition(float("inf"))

gps = robot.getDevice("gps")
gps.enable(timestep)

emitter = robot.getDevice("emitter")
receiver = robot.getDevice("receiver")
receiver.enable(timestep)

sensors = []
for i in range(8):
    sensor = robot.getDevice("ps" + str(i))
    sensor.enable(timestep)
    sensors.append(sensor)

folder = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..", "..", "data", "B3_pso_logs"
    )
)
os.makedirs(folder, exist_ok=True)

file = open(
    os.path.join(folder, "B3_" + name + ".csv"),
    "w", newline="", encoding="utf-8"
)
writer = csv.writer(file)
writer.writerow([
    "time_s", "robot", "x", "y",
    "target_x", "target_y",
    "current_fitness", "personal_best_fitness",
    "swarm_best_fitness", "messages_received",
    "obstacle_detected"
])

TARGET_X = 0.0
TARGET_Y = 1.0

personal_best = None
personal_score = float("inf")
swarm_best = None
swarm_score = float("inf")

messages_received = 0
step = 0

direction = 1
turn_until = 0.0
reverse_until = 0.0

last_x = None
last_y = None
heading = 0.0

waypoint = None
velocity = [0.0, 0.0]

print(name, "PSO STARTED", flush=True)

try:
    while robot.step(timestep) != -1:
        step += 1
        now = robot.getTime()

        x, y = gps.getValues()[:2]

        if not (math.isfinite(x) and math.isfinite(y)):
            left.setVelocity(0)
            right.setVelocity(0)
            continue

        score = math.hypot(x - TARGET_X, y - TARGET_Y)

        if score < personal_score:
            personal_score = score
            personal_best = [x, y]

        if personal_score < swarm_score:
            swarm_score = personal_score
            swarm_best = personal_best.copy()

        if step % 15 == 0:
            emitter.send(json.dumps({
                "robot": name,
                "score": personal_score,
                "position": personal_best
            }).encode("utf-8"))

        while receiver.getQueueLength() > 0:
            try:
                msg = json.loads(receiver.getString())

                if msg["robot"] != name:
                    messages_received += 1

                    if msg["score"] < swarm_score:
                        swarm_score = msg["score"]
                        swarm_best = msg["position"]

            except (ValueError, KeyError, TypeError):
                pass

            receiver.nextPacket()

        if last_x is not None:
            dx = x - last_x
            dy = y - last_y

            if math.hypot(dx, dy) > 0.003:
                heading = math.atan2(dy, dx)

        last_x, last_y = x, y

        if step % max(1, int(2000 / timestep)) == 0:
            if personal_best and swarm_best:
                for axis in range(2):
                    position = x if axis == 0 else y

                    velocity[axis] = (
                        0.5 * velocity[axis]
                        + 1.2 * random.random()
                        * (personal_best[axis] - position)
                        + 1.5 * random.random()
                        * (swarm_best[axis] - position)
                    )

                    velocity[axis] = max(
                        -0.4, min(0.4, velocity[axis])
                    )

                waypoint = [
                    max(-1.1, min(1.1, x + velocity[0])),
                    max(-1.1, min(1.1, y + velocity[1]))
                ]

        if waypoint is None:
            waypoint = [TARGET_X, TARGET_Y]

        values = [sensor.getValue() for sensor in sensors]
        front_left = max(values[6], values[7])
        front_right = max(values[0], values[1])

        obstacle = max(front_left, front_right) > 85

        if obstacle and now > turn_until:
            direction = -1 if front_left > front_right else 1
            reverse_until = now + 0.35
            turn_until = now + 1.0

        if now < reverse_until:
            ls, rs = -2.0, -2.0

        elif now < turn_until:
            ls = 1.5 - 1.8 * direction
            rs = 1.5 + 1.8 * direction

        else:
            desired = math.atan2(
                waypoint[1] - y,
                waypoint[0] - x
            )
            error = math.atan2(
                math.sin(desired - heading),
                math.cos(desired - heading)
            )

            correction = max(-1.0, min(1.0, error))
            ls = 3.5 - correction
            rs = 3.5 + correction

        left.setVelocity(max(-6.28, min(6.28, ls)))
        right.setVelocity(max(-6.28, min(6.28, rs)))

        if step % 10 == 0:
            writer.writerow([
                round(now, 3), name,
                round(x, 6), round(y, 6),
                TARGET_X, TARGET_Y,
                round(score, 6),
                round(personal_score, 6),
                round(swarm_score, 6),
                messages_received,
                int(obstacle)
            ])
            file.flush()

        if now >= 90:
            break

finally:
    left.setVelocity(0)
    right.setVelocity(0)
    file.close()

print(name, "PSO COMPLETE", flush=True)
