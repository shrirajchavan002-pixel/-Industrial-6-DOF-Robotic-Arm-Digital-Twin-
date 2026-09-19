# Industrial 6-DOF Robotic Arm Digital Twin & Autonomous Manipulation Platform

A simulation-based industrial 6-DOF robotic arm platform developed using **ROS 2 Jazzy, Gazebo Sim, RViz2, MoveIt 2, and ros2_control**.

The project focuses on building a modular robotic digital twin capable of robot description, visualization, motion planning, trajectory generation, and simulated joint execution.

> **Project Scope:** Simulation-only. No physical robot hardware testing has been performed.

---

## Project Overview

This project implements an industrial-style **6-DOF robotic arm digital twin** using a modular ROS 2 architecture.

### Core capabilities

- URDF/Xacro-based robot modeling
- TF2 robot frame hierarchy
- Gazebo Sim simulation
- ros2_control integration
- Joint trajectory control
- MoveIt 2 motion planning
- OMPL-based planning
- RRTConnect motion planner
- RViz2 visualization
- Joint velocity and acceleration limits
- Time-optimal trajectory parameterization
- Simulated trajectory execution

The architecture is structured with future migration to physical hardware in mind.

---

## System Architecture

```text
                    ┌─────────────────────┐
                    │       RViz2         │
                    │   MotionPlanning    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      MoveIt 2       │
                    │                     │
                    │  Motion Planning    │
                    │  IK / Validation    │
                    │  OMPL / RRTConnect  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Trajectory          │
                    │ Generation &        │
                    │ Time Parameterization│
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    ros2_control     │
                    │                     │
                    │ JointTrajectory     │
                    │ Controller          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Gazebo Sim      │
                    │                     │
                    │   6-DOF Robot       │
                    └─────────────────────┘

```
Robot Description

The robot model is implemented using modular URDF/Xacro files.

Implemented
6 revolute joints
Modular Xacro structure
Inertial properties
Joint definitions
ros2_control integration
Tool/end-effector frame
TF2 frame hierarchy

TF2 Frame Tree
```text
         
world
└── base_link
    └── link_1
        └── link_2
            └── link_3
                └── link_4
                    └── link_5
                        └── link_6
                            └── tool0

```
Gazebo Simulation

The robotic arm is simulated using Gazebo Sim.

The simulation includes:

6-DOF robot model
ROS-Gazebo communication through ros_gz
Simulation clock bridge
Joint state publishing
ros2_control integration
Simulated joint motion

ros2_control

The project uses ros2_control for controller-based robot motion.

Controllers

joint_state_broadcaster
JointTrajectoryController

Interfaces

Command interface:
position

State interfaces:
position
velocity

The six joints can receive and execute trajectory commands in simulation.

MoveIt 2

MoveIt 2 provides the motion planning layer for the robotic arm.

Implemented and verified
MoveIt 2 configuration
move_group
arm planning group
OMPL planning pipeline
RRTConnect planner
Joint velocity limits
Joint acceleration limits
State validation
Time-optimal trajectory parameterization
RViz2 MotionPlanning interface
Successful motion planning

Verified Motion Pipeline

The following pipeline has been successfully tested in simulation:
Joint Goal
    ↓
RViz2 MotionPlanning
    ↓
MoveIt 2
    ↓
OMPL / RRTConnect
    ↓
Trajectory Generation
    ↓
ros2_control
    ↓
JointTrajectoryController
    ↓
Gazebo Sim
    ↓
6-DOF Robot Motion

Repository Structure:

industrial_6dof_robot/
│
├── src/
│   │
│   ├── industrial_robot_description/
│   │   ├── launch/
│   │   ├── urdf/
│   │   ├── CMakeLists.txt
│   │   └── package.xml
│   │
│   ├── industrial_robot_moveit_config/
│   │   ├── config/
│   │   ├── launch/
│   │   ├── CMakeLists.txt
│   │   └── package.xml
│   │
│   └── industrial_robot_simulation/
│       ├── config/
│       ├── launch/
│       ├── CMakeLists.txt
│       └── package.xml
│
├── .gitignore
└── README.md

Software Environment:

| Component         | Version / Platform |
| ----------------- | ------------------ |
| Operating System  | Ubuntu 24.04       |
| ROS               | ROS 2 Jazzy        |
| Simulation        | Gazebo Sim         |
| Visualization     | RViz2              |
| Motion Planning   | MoveIt 2           |
| Control           | ros2_control       |
| Planning Pipeline | OMPL               |
| Motion Planner    | RRTConnect         |
| Robot Description | URDF / Xacro       |


Installation
1. Clone the repository
git clone https://github.com/shrirajchavan002-pixel/-Industrial-6-DOF-Robotic-Arm-Digital-Twin-

cd industrial_6dof_robot

2. Source ROS 2 Jazzy
source /opt/ros/jazzy/setup.bash

3. Build the workspace
colcon build --symlink-install

4. Source the workspace
source install/setup.bash

Launch Robot Visualization

To visualize the robot model in RViz2:

ros2 launch industrial_robot_description display.launch.py

Launch Gazebo Simulation:
ros2 launch industrial_robot_simulation sim.launch.py

This starts the simulation environment and robot control stack.

Verify Controllers:
ros2 control list_controllers

Expected:
arm_controller
joint_state_broadcaster

Both controllers should be:
active

Direct Joint Trajectory Test

A trajectory can be sent directly to the joint trajectory controller:

ros2 topic pub --once \
/arm_controller/joint_trajectory \
trajectory_msgs/msg/JointTrajectory "{
  joint_names: [joint_1, joint_2, joint_3, joint_4, joint_5, joint_6],
  points: [
    {
      positions: [0.3, -0.4, 0.5, -0.3, 0.4, 0.2],
      time_from_start: {sec: 3, nanosec: 0}
    }
  ]
}"

This command was verified to produce simulated robot motion.

Launch MoveIt 2

Start the MoveIt planning node:

ros2 launch industrial_robot_moveit_config move_group.launch.py

Then launch the MoveIt RViz interface:

ros2 launch industrial_robot_moveit_config moveit_rviz.launch.py

A configured demo launch is also available:

ros2 launch industrial_robot_moveit_config demo.launch.py

MoveIt Planning Workflow:
1) Start Gazebo simulation.
2) Start the MoveIt move_group node.
3) Open RViz2 with the MotionPlanning interface.
4) Select planning group arm.
5) Define a joint-space goal.
6) Generate a motion plan.
7) Inspect the generated trajectory.
8) Execute through the configured control pipeline.

Engineering Concepts Demonstrated : 

This project demonstrates practical implementation of:

ROS 2 package architecture
URDF/Xacro modeling
TF2 transformations
Robot joint configuration
Joint limits
Motion planning
OMPL
RRTConnect
State validation
Trajectory generation
Time parameterization
ros2_control
JointTrajectoryController
Gazebo simulation
RViz2 visualization
ROS-Gazebo clock synchronization
Modular robotic simulation architecture
 
Hardware Migration Architecture

The current implementation is simulation-only.

The architecture is structured so that the simulation control layer can later be adapted for physical hardware.

                 SIMULATION
                     │
             ┌───────▼────────┐
             │  ros2_control  │
             └───────┬────────┘
                     │
             Gazebo Control
                     │
                 Gazebo Sim


              FUTURE HARDWARE
                     │
             ┌───────▼────────┐
             │  ros2_control  │
             └───────┬────────┘
                     │
             Hardware Interface
                     │
              Motor Drivers
                     │
                Real Robot 

Current Status : 

| Module                    | Status          |
| ------------------------- | --------------- |
| 6-DOF Robot Model         | Implemented     |
| URDF/Xacro                | Implemented     |
| TF2                       | Implemented     |
| RViz2 Visualization       | Implemented     |
| Gazebo Simulation         | Implemented     |
| ros2_control              | Implemented     |
| JointTrajectoryController | Implemented     |
| MoveIt 2                  | Implemented     |
| OMPL Planning             | Implemented     |
| RRTConnect                | Implemented     |
| Joint Velocity Limits     | Implemented     |
| Joint Acceleration Limits | Implemented     |
| Simulated Joint Motion    | Verified        |
| MoveIt Motion Planning    | Verified        |
| Physical Robot Testing    | Not implemented |

Future Development

Potential extensions:

1) Cartesian path planning
2) Collision-object based manipulation
3) End-effector / gripper integration
4) Autonomous pick-and-place
5) Camera integration
6) Object detection
7) Perception pipeline
8) Workspace collision monitoring
9) Diagnostics and fault handling
10) Automated ROS 2 tests
11) Hardware interface implementation
12) Real robot deployment

Project Scope :

This project is a simulation-based robotics engineering project.

All current motion and planning results are obtained in simulation. No claims of physical robot testing or real-world industrial deployment are made.

Author

Shriraj Chavan

B.Tech — Robotics & Automation
Walchand College of Engineering, Sangli

Areas of Interest
Robotics
ROS 2
Motion Planning
Robot Simulation
Computer Vision
Autonomous Systems
