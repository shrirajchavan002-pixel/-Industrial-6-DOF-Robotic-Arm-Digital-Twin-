import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import Command


def generate_launch_description():

    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    pkg_description = get_package_share_directory(
        'industrial_robot_description'
    )

    xacro_file = os.path.join(
        pkg_description,
        'urdf',
        'industrial_robot.urdf.xacro'
    )

    robot_desc = Command(['xacro ', xacro_file])

    # Robot State Publisher
    rsp_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[
            {
                'robot_description': robot_desc,
                'use_sim_time': True
            }
        ]
    )

    # Gazebo Sim
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                pkg_ros_gz_sim,
                'launch',
                'gz_sim.launch.py'
            )
        ),
        launch_arguments={
            'gz_args': '-r empty.sdf'
        }.items(),
    )

    # Spawn robot into Gazebo
    spawn_node = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-topic',
            'robot_description',
            '-name',
            'industrial_6dof'
        ],
        output='screen'
    )

    # Gazebo -> ROS 2 clock bridge
    clock_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'
        ],
        output='screen'
    )

    # Joint State Broadcaster
    jsb_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'joint_state_broadcaster'
        ],
    )

    # Arm Joint Trajectory Controller
    arm_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'arm_controller'
        ],
    )

    # Wait for Gazebo and controller_manager
    delayed_spawners = TimerAction(
        period=3.0,
        actions=[
            jsb_spawner,
            arm_spawner
        ]
    )

    return LaunchDescription([
        rsp_node,
        gazebo,
        clock_bridge,
        spawn_node,
        delayed_spawners
    ])
