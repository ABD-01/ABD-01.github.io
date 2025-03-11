# ROS2 Challenge


I have used Ubuntu:Focal docker image and source installed Ros2 Foxy for these tasks.
```
docker pull ubuntu:focal
```

```{youtube} igcttLvOtHA
:align: center
```

<!--
:::{toctree}
---
maxdepth: 2
---

Hello! ROS2 is fun <ros2/ros2_is_fun>
Launch your robot <ros2/laser_scan>
Navigate your turtlebot <ros2/navigation>
::: 
-->

## 'Hello! ROS2 is fun'

This is introduction to creating a simple publisher and subscriber in ROS2. Basically there is one node that listens on a topic on which the other node talks. 

```{image} https://abd-01.github.io/crispy-adventure/_static/gifs/talk-listen.gif
---
alt: talker-listener
align: center
width: 70%
---
```

### Creating ROS2 package:
```bash
cd <path/to/ros2_ws>/src
ros2 pkg create ros2_is_fun --build-type ament_cmake --dependencies std_msgs rclcpp
```

This will create `ros2_is_fun` package with following files and directory inside it.
```bash
ros2_is_fun/
    CMakeLists.txt
    package.xml
    include/ros2_is_fun
    src/
```
For more info on the function of these files see *[What makes up a ROS 2 package?](https://docs.ros.org/en/foxy/Tutorials/Beginner-Client-Libraries/Creating-Your-First-ROS2-Package.html#what-makes-up-a-ros-2-package)*

The source code `publisher.cpp` and `subscriber.cpp` will be added in the `src` directory. 
The `CMakeLists.txt` will be edited to add the executable to the package and install them.

```cmake
add_executable(publisher src/publisher.cpp)
ament_target_dependencies(publisher rclcpp std_msgs)

add_executable(subscriber src/subscriber.cpp)
ament_target_dependencies(subscriber rclcpp std_msgs)

install(TARGETS 
  publisher
  subscriber
  DESTINATION lib/${PROJECT_NAME})
```

### Building the package

```bash
colcon build --packages-select ros2_is_fun
```

### Using the package

To be able to run the executables, first source the setup files from `install` directory.

```bash
source install/local_setup.bash
source install/setup.bash
```

Run the executables:

```bash
ros2 run ros2_is_fun publisher
```

```bash
ros2 run ros2_is_fun subscriber
```

```{image} https://abd-01.github.io/crispy-adventure/_static/pub-sub.webp
---
width: 100%
alt: Pub-Sub
align: center
---
```

### Source Code

``````{dropdown} Source Code
`````{tab-set}
````{tab-item} Publisher

```{literalinclude} ../ros2_ws/src/ros2_is_fun/src/publisher.cpp
:language: cpp
```

````

````{tab-item} Subscriber

```{literalinclude} ../ros2_ws/src/ros2_is_fun/src/subscriber.cpp
:language: cpp
```

````
`````
``````

## Visualizing Laser Scan Data

```{image} https://abd-01.github.io/crispy-adventure/_static/gifs/Jack_Jack_Laser_Vision.webp
---
alt: Jack Jack Laser
align: center
width: 70%
---
```

This part involves using laser sensors to scan the environment and visualize the data in rviz2.

### Pre-requisites

I have used [`turtlebot3_burger`](https://github.com/ROBOTIS-GIT/turtlebot3/blob/foxy-devel/turtlebot3_description/urdf/turtlebot3_burger.urdf) as the robot model, and [`dynamic_world`](https://github.com/mlherd/Dataset-of-Gazebo-Worlds-Models-and-Maps/tree/master/worlds/dynamic_world) as a model for the world.

#### Environment Setup

My `~/.bashrc` includes these lines:
```bash
source /opt/ros/foxy/setup.bash
source /usr/share/colcon_cd/function/colcon_cd.sh
export _colcon_cd_root=/opt/ros/foxy/
source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash
export TURTLEBOT3_MODEL=burger
export GAZEBO_MODEL_PATH=/usr/share/gazebo-11/models:/opt/ros/foxy/share/turtlebot3_gazebo/models/:$GAZEBO_MODEL_PATH
```

Also, the package models if any need to be added to the path as well.

```bash
export GAZEBO_MODEL_PATH=/home/ros2_ws/src/jde_ros2_asgn/models:$GAZEBO_MODEL_PATH
```

#### Nodes

To view the Laser Scans we need atleast 4 nodes:

1. **Gazebo** - The simulation environment.
```
gazebo $(ros2 pkg prefix --share jde_ros2_asgn)/worlds/dynamic_world.world
```

2. **Robot State Publisher** - To broadcast the state of the robot to the [tf2](https://wiki.ros.org/tf2) transform library.
```
ros2 run robot_state_publisher robot_state_publisher $(ros2 pkg prefix --share turtlebot3_description)/urdf/turtlebot3_burger.urdf
```

3. **Teleop Twist Keyboard** - The title is self-explanatory.
```
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

4. **RViz2** - ROS vizualtion tool
```
rviz2
```

### Launching the nodes

I have created a launch file named `laser_scan.launch` in `launch` directory to launch all the nodes from one command.
(Except for the keyboard node, you know why.)

```bash
ros2 launch jde_ros2_asgn laser_scan.launch.py
```
and 
```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

```{raw} html
<p class="centered">
  <video width="100%" autoplay muted loop>
    <source src="https://abd-01.github.io/crispy-adventure/_static/laser_scan.mp4" type="video/mp4" />
    Your browser does not support the video tag.
  </video>
</p>
```

### Source Code

````{dropdown} laser_scan.launch.py

```{literalinclude} ../ros2_ws/src/jde_ros2_asgn/launch/laser_scan.launch.py
:language: python
```

````

## ROS2 Navigation2

In simple terms we want our robot to move from point A to point B. But first, we need to know where the robot is (i.e. localization) and where are points A and B (i.e. mapping).

```{image} https://abd-01.github.io/crispy-adventure/_static/gifs/robot_city.gif
---
alt: You Go To Robot City
align: center
width: 70%
---
```

### Background

For *mapping*, I have used `slam_toolbox` package, to help estimate the robot position and create the map of the world.

Once a map is available we need to *localize*, which is done by creating a transform chain `map -> odom -> base_link` (Oh the errors here are painful!!!). We will use [tf2](https://docs.ros.org/en/foxy/Tutorials/Intermediate/Tf2/Introduction-To-Tf2.html) transform library to do that.

Now, what left is navigation.

### Creating the Map

We will launch the slam tool box, create a gazebo simulation world, visualize the map in rviz2 and teleop the robot.

```bash
ros2 launch slam_toolbox online_async_launch.py
ros2 launch jde_ros2_asgn navingation_tb3.launch.py
rviz2 -d $(ros2 pkg prefix --share jde_ros2_asgn)/rviz/mapping.rviz
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```
Once, the mapping is done, we will save it using `nav2_map_server`.
```bash
ros2 run nav2_map_server map_saver_cli -f src/jde_ros2_asgn/maps/my_cafe --ros-args -p save_map_timeout:=10000
```

```{raw} html
<p class="centered">
  <video width="100%" autoplay muted loop>
    <source src="https://abd-01.github.io/crispy-adventure/_static/mapping(my_cafe).mp4" type="video/mp4" />
    Your browser does not support the video tag.
  </video>
</p>
```

### Waypoint Navigation

I have created a launch file to start all the required nodes, however I have been facing issue when `nav2_bringup` is lanuched using the same launch file. Hence, we will use additional terminal to launch it.

```bash
ros2 launch jde_ros2_asgn navigation_tb3.launch.py
ros2 launch nav2_bringup bringup_launch.py use_sim_time:=True autostart:=True map:=/home/ros2_ws/src/jde_ros2_asgn/maps/my_cafe.yaml
ros2 run rviz2 rviz2 -d $(ros2 pkg prefix nav2_bringup)/share/nav2_bringup/rviz/nav2_default_view.rviz
```
Rest is shown in the video.

## [If I only had more time.](https://getyarn.io/yarn-clip/da763d8d-f2bb-4f9a-8ddc-6211e6f26d68)

<!-- 
```{raw} html
<div class="centered">
  <iframe src="https://getyarn.io/yarn-clip/da763d8d-f2bb-4f9a-8ddc-6211e6f26d68/embed?autoplay=False&responsive=False">
  </iframe>
</div>
``` 
-->

I used up ~1.5 weeks of time for the following to work. Why? Because the challenge said "*(or any other robot if you wish to).*"

The issues mentioned were not the limitation, but the time was. Hence I then decided to move forward with the TurtleBot3. 

```{image} https://abd-01.github.io/crispy-adventure/_static/racecar-tunnel.webp
---
alt: Racecar and Tunnel World
align: center
width: 100%
---
```

This is racecar model and tunnel world taken from [mit-racecar](https://github.com/mit-racecar) which I guess is used for labs in [Robotics: Science and Systems (MIT Course)](https://github.com/mit-rss/intro_to_ros).

The issues I faced:
* Spawning the robot URDF in Gazebo. (I beleive version issues or my skill isssues.)
* The package was written using ROS kinetic.
* The racecar is Ackermann-steering Robot, and this was my first time working with ackermann steering.

The other candidate robot model I had in mind was [Sahayak-v3](https://www.ivlabs.in/sahayak---an-autonomous-covid-aid-bot2.html) developed at [IvLabs](https://www.ivlabs.in/).

```{raw} html
<p align="center">
  <img src="https://user-images.githubusercontent.com/64685403/132857785-d6f70385-3a5a-43d3-9c87-5cd9a9a209a8.gif" width="40%">
</p>
```

## References

* ROS & Docker: [Docker Commands](https://github.com/noshluk2/ros1_wiki/blob/main/docker/commands.md)
* ROS2 Foxy Tutorials: [Writing a simple publisher and subscriber (C++)](https://docs.ros.org/en/foxy/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Cpp-Publisher-And-Subscriber.html)
* `std::bind` function in C++: [Bind Function and Placeholders in C++](https://www.geeksforgeeks.org/bind-function-placeholders-c/)
* Gazebo not showing my models: [include a model which is not in default path](https://answers.gazebosim.org/question/24935/how-to-include-a-model-which-is-not-in-default-path/#:~:text=You%20can%20check%20the%20current%20value%20of%20GAZEBO_MODEL_PATH,them%20using%20%3A%20export%20GAZEBO_MODEL_PATH%3D%24GAZEBO_MODEL_PATH%3A%3Cpath%20to%20your%20model%3E)
* Slow Colcon Build: [`colcon build` on OSX is orders of magnitude slower than direct `make`](https://github.com/colcon/colcon-core/issues/193)
* Dynamic World Model: [Dataset-of-Gazebo-Worlds-Models-and-Maps](https://github.com/mlherd/Dataset-of-Gazebo-Worlds-Models-and-Maps/tree/master/worlds/dynamic_world)
* View URDF in Gazebo: [foxy/Tutorials/Intermediate/URDF](https://docs.ros.org/en/foxy/Tutorials/Intermediate/URDF/URDF-Main.html) & [URDF in Gazebo](https://classic.gazebosim.org/tutorials?tut=ros_urdf)
* Saving Maps [answers.ros.org/timeout error while saving map](https://answers.ros.org/question/379565/timeout-error-while-saving-map/)
* ROS2 TurtleBot3: [ros2_turtlebot3
](https://github.com/twming/ros2_turtlebot3)
* Racecar URDF: [mit-racecar/racecar_gazebo](https://github.com/mit-racecar/racecar_gazebo/blob/master/racecar_description/urdf/racecar.xacro)  
* Sahayak-V3: [IvLabs/Sahayak-v3](https://github.com/IvLabs/Sahayak-v3)
* Notes from courses done: [ROS2 (Foxy-Humble) For Beginners I](https://www.udemy.com/course/ros2-how-to) & [ros-essentials](https://www.udemy.com/course/ros-essentials/)