import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command

def generate_launch_description():
    # 1. Locate the package and URDF file
    pkg_share = get_package_share_directory('industrial_robot_description')
    xacro_file = os.path.join(pkg_share, 'urdf', 'industrial_robot.urdf.xacro')
    
    # 2. Process Xacro dynamically
    robot_description_content = Command(['xacro ', xacro_file])
    robot_description = {'robot_description': robot_description_content}

    # 3. Define Nodes
    rsp_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description]
    )

    jsp_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui'
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen'
    )

    # 4. Launch them all
    return LaunchDescription([
        rsp_node,
        jsp_gui_node,
        rviz_node
    ])
