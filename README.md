#Tensorflow_in_ROS
I made a ros-node to predict numbers from camera image.  
I used Tensorflow tutorial Deep MNIST model(https://www.tensorflow.org/versions/r0.11/tutorials/mnist/pros/index.html)

Before you use this, you must install some programs.

* Install tensorflow (see https://www.tensorflow.org/versions/r0.9/get_started/os_setup.html)  
* Install ROS (see http://wiki.ros.org)  
* Install cv-bridge, and camera driver (for example, cv_camera)  

`$ sudo apt-get install ros-indigo-cv-bridge ros-indigo-cv-camera`

#tensorflow_in_ros_mnist.py
This is main file. This make the ros-node.

* publish: /result (std_msgs/Int16)
* subscribe: /image (sensor_msgs/Image)

#model.ckpt,model.ckpt.meta
This is Trained model.
Test set accuracy is approximately 99.2%.

#How to try

`$ roscore`  
`$ python tensorflow_in_ros_mnist.py image:=/cv_camera/image_raw`  
`$ rosrun cv_camera cv_camera_node`  
`$ rostopic echo /result`  

#Result
For example, you can see result1.png or result2.png.  
1 and 9 are camera image from rviz.
You can see ros-node published predicted numbers.

#Reference
* Deep MNIST for Experts (https://www.tensorflow.org/versions/r0.11/tutorials/mnist/pros/index.html)  
* Variables: Creation, Initialization, Saving, and Loading (https://www.tensorflow.org/versions/r0.11/how_tos/variables/index.html)  
* rostensorflow (https://github.com/OTL/rostensorflow)