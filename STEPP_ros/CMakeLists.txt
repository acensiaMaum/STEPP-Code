cmake_minimum_required(VERSION 3.5)
project(STEPP_ros)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)

find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(cv_bridge REQUIRED)
find_package(image_transport REQUIRED)
find_package(pcl_conversions REQUIRED)
find_package(pcl_ros REQUIRED)
find_package(PCL REQUIRED)
find_package(OpenCV REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(tf2_geometry_msgs REQUIRED)
find_package(message_filters REQUIRED)

# ROS 2 message generation
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/Float32Stamped.msg"
  DEPENDENCIES std_msgs
)

# C++ executable
add_executable(depth_projection_synchronized src/depth_projection_synchronized.cpp)
ament_target_dependencies(depth_projection_synchronized
  rclcpp sensor_msgs nav_msgs std_msgs cv_bridge pcl_conversions tf2 tf2_ros tf2_geometry_msgs message_filters
)
target_include_directories(depth_projection_synchronized PUBLIC ${PCL_INCLUDE_DIRS})
target_link_libraries(depth_projection_synchronized ${PCL_LIBRARIES} ${OpenCV_LIBS})

# Ensure messages are built before the node that uses them
rosidl_get_typesupport_target(cpp_typesupport_target ${PROJECT_NAME} "rosidl_typesupport_cpp")
add_dependencies(depth_projection_synchronized ${cpp_typesupport_target})

install(TARGETS depth_projection_synchronized
  DESTINATION lib/${PROJECT_NAME}
)

# Install Python script as an executable
install(PROGRAMS scripts/inference_node.py
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY launch/
  DESTINATION share/${PROJECT_NAME}/launch
)

ament_export_dependencies(rosidl_default_runtime)
ament_package()
