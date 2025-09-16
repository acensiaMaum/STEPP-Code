#!/usr/bin/env python3
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    rgb_topic = LaunchConfiguration('rgb_topic')
    depth_topic = LaunchConfiguration('depth_topic')
    odom_topic = LaunchConfiguration('odom_topic')
    model_path = LaunchConfiguration('model_path')
    visualize = LaunchConfiguration('visualize')
    ump = LaunchConfiguration('ump')
    cutoff = LaunchConfiguration('cutoff')
    camera_type = LaunchConfiguration('camera_type')
    decay_time = LaunchConfiguration('decay_time')

    return LaunchDescription([
        DeclareLaunchArgument('rgb_topic', default_value='desired_rgb_image_input_topic_compressed'),
        DeclareLaunchArgument('depth_topic', default_value='desired_aligned_depth_to_rgb_topic_raw'),
        DeclareLaunchArgument('odom_topic', default_value='desired_odometry_topic'),
        DeclareLaunchArgument('model_path', default_value='path_to_model_weight.pth'),
        DeclareLaunchArgument('visualize', default_value='false'),
        DeclareLaunchArgument('ump', default_value='false'),
        DeclareLaunchArgument('cutoff', default_value='0.45'),
        DeclareLaunchArgument('camera_type', default_value='zed2'),
        DeclareLaunchArgument('decay_time', default_value='8.0'),

        Node(
            package='stepp_ros',
            executable='inference_node.py',
            name='inference_node',
            output='screen',
            parameters=[{
                'model_path': model_path,
                'visualize': visualize,
                'ump': ump,
                'cutoff': cutoff,
            }],
            remappings=[
                ('/camera/color/image_raw/compressed', rgb_topic),
            ]
        ),

        Node(
            package='stepp_ros',
            executable='depth_projection_synchronized',
            name='depth_projection',
            output='screen',
            parameters=[{
                'camera_type': camera_type,
                'decayTime': decay_time,
            }],
            remappings=[
                ('/camera/aligned_depth_to_color/image_raw', depth_topic),
                ('/state_estimation', odom_topic),
            ]
        ),
    ])


