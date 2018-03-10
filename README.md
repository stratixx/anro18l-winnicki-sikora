# anro18l-winnicki-sikora
ANRO 18L Winnicki Sikora

How to: ROS ver 1.0
Aby rozpocząć przygodę z tym repo musisz przejść tutorial ROS-a, a w szczególności: 
 - wywołać polecenia: 
 
    mkdir -p ~/catkin_ws/src        
    cd ~/catkin_ws/    
    catkin_make    
    
    source ~/catkin_ws/devel/setup.bash
    
    cd ~/catkin_ws/src    
    catkin_create_pkg beginner_tutorials std_msgs rospy roscpp    
    catkin_create_pkg lab1 std_msgs rospy roscpp    
    cd ~/catkin_ws    
    catkin_make
    
 - usunąć pliki z folderu src/
 - sklonować repo do folderu src/
 - wywołać polecenie: 
    catkin_make
