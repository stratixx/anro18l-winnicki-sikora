cmake_minimum_required(VERSION 2.8.3)
project(lab4)

find_package(catkin REQUIRED COMPONENTS
	rospy
	roscpp
	std_msgs
	message_generation
)

add_service_files(
	FILES
	InterpolationRequest.srv
)

generate_messages(
	DEPENDENCIES
	std_msgs
)


catkin_package()



if(CATKIN_ENABLE_TESTING)
  find_package(roslaunch REQUIRED)
  roslaunch_add_file_check(launch)
endif()

install(DIRECTORY launch srv urdf scripts
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})


