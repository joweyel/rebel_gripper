#!/usr/bin/env python3
"""
Visualization script for showing the Rebel Gripper as a standalone robot-model
"""

import os

from ament_index_python import get_package_share_directory
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

from launch import LaunchDescription
from launch.substitutions import Command, FindExecutable


def generate_launch_description():

    # Get relevant package and file paths
    rebel_gripper_pkg = get_package_share_directory("rebel_gripper")
    rebel_gripper_description_file = os.path.join(
        rebel_gripper_pkg, "urdf", "rebel_gripper.urdf.xacro"
    )
    rviz_config_file = os.path.join(rebel_gripper_pkg, "rviz", "view_gripper.rviz")

    # Get URDF/xacro (using visualization wrapper with world frame)
    robot_description_content = Command(
        [
            FindExecutable(name="xacro"),
            " ",
            rebel_gripper_description_file,
        ]
    )

    robot_description = {
        "robot_description": ParameterValue(robot_description_content, value_type=str)
    }

    # Publishes joint states of robot description
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[robot_description],
    )

    # Starts a gui to interact with articulated joints in the robot model
    joint_state_publisher_gui_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        output="screen",
    )

    # Rviz 2 Visualization
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        output="screen",
        arguments=["-d", rviz_config_file],
    )

    return LaunchDescription(
        [
            robot_state_publisher_node,
            joint_state_publisher_gui_node,
            rviz_node,
        ]
    )
