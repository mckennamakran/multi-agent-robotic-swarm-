# Multi-Robot Swarm Intelligence and Autonomous Control

A multi-robot simulation project developed using **Webots R2025a and Python**. Explories swarm robotics, distributed consensus algorithms and neural-network-based decision-making. 

## Table of Contents

1. [Project Overview](#project-overview)
2. [Technologies and Libraries](#technologies-and-libraries)
3. [Project Objectives](#project-objectives)
3. [Simulation Environment](#simulation-environment)
4. [Project Architecture](#project-architecture)
5. [Experiments and Implementations](#experiments-and-implementations)
   - [B1: Swarm Robotics and Communication](#b1-swarm-robotics-and-communication)
   - [B2: Distributed Consensus](#b2-distributed-consensus)
   - [B4: Neural Network-Based Robot Control](#b4-neural-network-based-robot-control)
7. [Explanation Pictures](#explanation-pictures)


## Project Overview

This project investigates how multiple autonomous robots can operate within a shared environment using different approaches to intelligent control and coordination.

The simulation consists of four E-puck mobile robots operating in a 3 × 3 metre arena containing three physical obstacles.

Each robot is controlled independently through Python controllers integrated with the Webots robotics simulation environment.

The project explores 3 completed experiments:

| Experiment | Focus | Main Concept |
|---|---|---|
| B1 | Swarm Robotics | Autonomous movement and wireless communication |
| B2 | Distributed Consensus | Agreement between multiple agents |
| B3 | Particle Swarm Optimization |  *coming soon...*|
| B4 | Neural Network Control | Machine-learning-based movement decisions |


The experiments demonstrate different aspects of multi-agent systems, ranging from basic autonomous navigation to distributed algorithms and machine learning.

The project also incorporates data collection and performance analysis to evaluate the behaviour of the robots rather than relying exclusively on visual observations.

## Technologies and Libraries

The project uses the following technologies:

| Technology | Purpose |
|---|---|
| Python | Robot controllers and analysis scripts |
| Webots R2025a | Robotics simulation environment |
| E-puck | Simulated differential-drive robot |
| NumPy | Numerical operations and calculations |
| Pandas | CSV processing and data analysis |
| Matplotlib | Graphs and data visualization |
| JSON | Neural network model storage and robot messaging |
| CSV | Experimental data storage |
| PyCharm | Python development environment |

### Python modules

The project also uses standard Python modules:

- `controller`: Webots robot API.
- `math`: Mathematical calculations and trigonometry.
- `random`: Random values for PSO.
- `json`: Serialization and deserialization.
- `csv`: CSV file operations.
- `os`: File and directory management.


## Project Objectives

The primary objectives are to:

- Develop a multi-robot simulation using Webots.
- Implement autonomous robot movement using differential-drive motors.
- Integrate proximity sensors for obstacle detection and avoidance.
- Use GPS sensors to monitor robot positions and trajectories.
- Implement wireless communication between multiple robots.
- Explore distributed consensus algorithms.
- Apply Particle Swarm Optimization to multi-robot target searching.
- Integrate a feedforward neural network into a robot controller.
- Compare centralized and distributed approaches to numerical agreement.
- Collect experimental data and evaluate system performance.
- Visualize robot behaviour using Python data-analysis libraries.


## Simulation Environment

The project uses four **E-puck robots** within a "rectangular arena".

### Environment specifications

| Component | Configuration |
|---|---|
| Simulator | Webots R2025a |
| Programming language | Python |
| Arena dimensions | 3 × 3 metres |
| Number of robots | 4 |
| Robot model | E-puck |
| Number of obstacles | 3 |
| Proximity sensors | 8 per robot |
| Position tracking | GPS |
| Movement system | Two independently controlled wheels |
| Communication | Webots emitter and receiver |
| Robot control | Individual Python controllers |

### Robot starting positions

The robots begin in different corners of the arena.

| Robot | X-coordinate | Y-coordinate |
|---|---:|---:|
| E-puck 1 | -1.0 | -1.0 |
| E-puck 2 | 1.0 | -1.0 |
| E-puck 3 | -1.0 | 1.0 |
| E-puck 4 | 1.0 | 1.0 |

### Environment obstacles

Three physical box-shaped obstacles are positioned inside the arena.

These obstacles introduce navigation challenges and allow the controllers to demonstrate obstacle detection, avoidance, and recovery behaviour.

### Sensors and actuators

**Proximity sensors**

Each E-puck uses eight infrared proximity sensors, identified as `ps0` through `ps7`.

The sensors provide readings that help the robot identify nearby objects and determine when avoidance behaviour is necessary.

**GPS**

The GPS sensor provides the robot's simulated position coordinates, allowing the controllers to record trajectories and calculate distances.

**Differential-drive motors**

Each robot has two independently controlled wheel motors:

- Left wheel motor
- Right wheel motor

By adjusting the velocities of these motors, the robot can move forward, reverse, turn, or rotate.

**Wireless communication**

Each robot uses a Webots emitter and receiver to exchange information with the other robots.

Messages are serialized using JSON and transmitted as encoded byte data.

## Project Architecture

The project follows a three-layer architecture.

### 1. Simulation layer

Webots provides the physical simulation environment, including:

- Robot models
- Arena and obstacles
- Sensors
- Motors
- Communication devices
- Simulation time and physics

### 2. Control layer

Python controllers implement the behaviour of each robot, which include:

- Obstacle avoidance
- Swarm communication
- Consensus calculations
- Particle Swarm Optimization
- Neural network inference
- Wheel-speed control

### 3. Evaluation layer

Python analysis scripts process the recorded experimental data.

The evaluation process uses:

- CSV files for data storage
- Pandas for data processing
- NumPy for numerical calculations
- Matplotlib for visualization
- Evaluation tables for summarizing performance

The overall data flow is:

**Webots Simulation → Python Controllers → CSV Logs → Data Analysis → Performance Metrics and Graphs**

---

# Experiments and Implementations

## B1: Swarm Robotics and Communication

**Controller:** `b_swarm_controller.py`

### Objective

To investigate how multiple autonomous robots can navigate a shared environment, avoid obstacles, and exchange information through wireless communication.

### Implementation

Each robot independently executes its own controller. The controller performs the following operations:

1. Initializes the robot and retrieves its Webots simulation timestep.
2. Identifies the robot using its assigned name.
3. Initializes the left and right wheel motors.
4. Enables the eight infrared proximity sensors.
5. Initializes GPS for position tracking.
6. Initializes the emitter and receiver communication devices.
7. Reads proximity sensor values during each simulation cycle.
8. Determines whether an obstacle is present.
9. Executes obstacle avoidance behaviour when necessary.
10. Adjusts wheel velocities to control movement.
11. Broadcasts sensor and simulation information every 15 simulation steps.
12. Receives and processes messages from other robots.
13. Records movement, sensor readings, and communication information in CSV files.

### Communication

Robots broadcast JSON messages containing information such as:

- Robot identifier
- Simulation step
- Front-left proximity reading
- Front-right proximity reading

The messages are converted into JSON strings and encoded using UTF-8 before transmission.

Receiving robots decode and deserialize the messages into Python dictionaries.

The robots exchange information independently, without a central communication controller.

### Obstacle avoidance

The controller uses proximity sensor thresholds to determine when nearby objects require an avoidance manoeuvre.

The escape behaviour involves reversing and turning away from the detected obstacle.

Wheel velocities are constrained to the configured maximum motor speed.

### Evaluation

The experiment records:

- Robot trajectories
- Distance travelled
- Proximity sensor readings
- Obstacle escape behaviour
- Messages transmitted
- Messages received

### Experimental results

| Robot | Distance travelled | Messages sent | Messages received |
|---|---:|---:|---:|
| E-puck 1 | 8.7552 m | 314 | 939 |
| E-puck 2 | 8.6805 m | 314 | 939 |
| E-puck 3 | 8.5512 m | 314 | 939 |
| E-puck 4 | 8.4444 m | 314 | 939 |

### Key findings

The four robots successfully executed independent navigation and wireless information exchange.

Each robot transmitted 314 messages and received 939 messages during the recorded experiment.

The results demonstrate basic decentralized robot operation and multi-agent communication.

**Implementation note:** Although robots exchange information, their movement decisions are based on their own proximity sensor readings. Received messages are not directly incorporated into their steering decisions.

## B2: Distributed Consensus

**Controller:** `b_consensus_controller.py`

**Analysis:** `B2_consensus_analysis.py`

### Objective

To implement a distributed consensus algorithm in which multiple robots independently calculate and agree on a common numerical value.

### Initial conditions

Each robot starts with a different numerical value.

| Robot | Initial value |
|---|---:|
| E-puck 1 | 10 |
| E-puck 2 | 20 |
| E-puck 3 | 30 |
| E-puck 4 | 40 |

The expected consensus value is the arithmetic mean: In this case **25**

### Implementation

The consensus controller performs the following operations:

1. Initializes the robot and communication devices.
2. Assigns an initial numerical value based on the robot ID.
3. Stops the wheel motors because this experiment focuses on information exchange rather than navigation.
4. Broadcasts the current numerical value to the other robots.
5. Receives messages containing values from neighbouring robots.
6. Checks that the received messages belong to the current iteration.
7. Stores the latest received value from each neighbouring robot.
8. Waits until values from all three other robots have been received.
9. Calculates the average of the four values.
10. Updates its own numerical value.
11. Repeats the process for 30 iterations.
12. Records the numerical values and consensus errors in CSV files.

### Consensus calculation

Each robot independently calculates the sum of all recieved values. The three neighbouring values represent the other robots' current estimates. Because the network is fully connected, every robot receives all three neighbouring values. The robots therefore calculate the same average.

### Evaluation

The experiment measures:

- Consensus value over time
- Iteration count
- Difference from the expected average
- Convergence behaviour

### Experimental results

All four robots successfully reached the expected consensus value of 25.

| Metric | Result |
|---|---:|
| Expected average | 25 |
| Final robot 1 value | 25 |
| Final robot 2 value | 25 |
| Final robot 3 value | 25 |
| Final robot 4 value | 25 |
| Final consensus error | 0 |
| Recorded iterations | 30 |

### Key findings

The experiment demonstrates that multiple independent agents can reach numerical agreement through direct information exchange without requiring a central controller to calculate and distribute the answer.

The fully connected communication network allows the robots to reach consensus in the first recorded update.

**Implementation note:** The current implementation assumes all three neighbouring values are received during each consensus round. Communication failures and partially connected networks are not evaluated.

---

## B4: Neural Network-Based Robot Control

**Controller:** `b_neural_controller.py`

**Model:** `B4_model.json`

**Analysis:** `B4_neural_training.py`

### Objective

To integrate a feedforward neural network into an autonomous robot controller so that robots can select movement actions based on proximity sensor readings.

### Neural network architecture

The network uses a 2-8-3 architecture:

| Layer | Neurons | Function |
|---|---:|---|
| Input layer | 2 | Receives proximity sensor features |
| Hidden layer | 8 | Processes the input using ReLU |
| Output layer | 3 | Produces movement action scores |

The two input features represent normalized front-left and front-right proximity readings.

### Neural network model

The trained model parameters are stored in:

`data/B4_neural_logs/B4_model.json`

The JSON file contains:

- Weight matrices
- Bias values

The network contains 51 parameters in total --> 2 × 8 + 8 + 8 × 3 + 3 = 51

### Forward propagation

The controller uses forward propagation to process sensor readings.

Each neuron calculates a weighted sum:


# PIC


The hidden layer applies the ReLU activation function:

# PIC

The output layer generates three scores. The controller selects the index of the highest output 


### Available movement actions

| Output class | Action | Left motor | Right motor |
|---|---|---:|---:|
| 0 | Forward | 3.8 | 3.8 |
| 1 | Left | 2.8 | 4.0 |
| 2 | Right | 4.0 | 2.8 |

Motor values represent wheel angular velocities in radians per second.

### Implementation

The neural controller performs the following operations:

1. Initializes the robot and its sensors.
2. Enables GPS and proximity sensors.
3. Initializes the wheel motors.
4. Loads the saved neural network model from JSON.
5. Reads front-left and front-right proximity sensor values.
6. Normalizes the readings.
7. Passes the resulting features into the neural network.
8. Performs forward propagation through the hidden layer.
9. Applies ReLU activation.
10. Calculates the three output scores.
11. Selects the predicted movement action.
12. Converts the selected action into wheel velocities.
13. Monitors obstacle conditions.
14. Activates a rule-based recovery sequence when necessary.
15. Checks for insufficient movement to identify potentially stuck robots.
16. Records predictions, sensor readings, and GPS positions.

### Obstacle recovery

The controller combines neural-network inference with conventional rule-based control. The recovery sequence includes:

- Reversing away from an obstacle.
- Turning to find a clearer direction.
- Returning to normal forward operation.

This combination allows the neural network to make normal movement decisions while conventional logic handles specific recovery situations.


### Key findings

The neural network successfully integrated sensor-based inference into the robot control process.

However, the recorded predictions show that the forward action was never selected during this experiment.

This indicates that the model's output distribution requires further investigation and validation.

**Important implementation note:** The uploaded `B4_neural_training.py` script performs log analysis and visualization; it does not train the neural network. The model's original training procedure and dataset are not included in this repository. The JSON file contains the parameters used for inference.

The existing confusion matrix and training-loss figures are retained as experimental artifacts, but their original generation procedure is not included in the supplied scripts.

---

# Explanation Pictures 


