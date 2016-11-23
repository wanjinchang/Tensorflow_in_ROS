import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import Int16
from cv_bridge import CvBridge
import cv2
import numpy as np
import tensorflow as tf


def weight_variable(shape):
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)

def bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)

def conv2d(x, W):
  return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], 
                      padding='SAME')

def max_pool_2x2(x):
  return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                        strides=[1, 2, 2, 1], padding='SAME')


def makeCNN(x):
    # --- define CNN model
    W_conv1 = weight_variable([5, 5, 1, 32])
    b_conv1 = bias_variable([32])
    h_conv1 = tf.nn.relu(conv2d(x, W_conv1) + b_conv1)

    h_pool1 = max_pool_2x2(h_conv1)

    W_conv2 = weight_variable([3, 3, 32, 64])
    b_conv2 = bias_variable([64])
    h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)

    h_pool2 = max_pool_2x2(h_conv2)

    W_fc1 = weight_variable([7 * 7 * 64, 1024])
    b_fc1 = bias_variable([1024])
    h_pool2_flat = tf.reshape(h_pool2, [-1, 7 * 7 * 64])
    h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

    W_fc2 = weight_variable([1024, 10])
    b_fc2 = bias_variable([10])

    y_conv = tf.nn.softmax(tf.matmul(h_fc1, W_fc2) + b_fc2)
 
    return y_conv



class RosTensorFlow():
    def __init__(self):
        self._cv_bridge = CvBridge()
        self._sub = rospy.Subscriber('image', Image, self.callback, queue_size=1)
        self._pub = rospy.Publisher('result', Int16, queue_size=1)

        self.x = tf.placeholder(tf.float32, [None,28,28,1], name="x")
        self.y_conv = makeCNN(self.x)

        self._saver = tf.train.Saver()
        self._session = tf.InteractiveSession()
        
        init_op = tf.initialize_all_variables()
        self._session.run(init_op)

        self._saver.restore(self._session, "model.ckpt")


    def callback(self, image_msg):
        cv_image = self._cv_bridge.imgmsg_to_cv2(image_msg, "bgr8")
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2GRAY)
        ret,cv_image = cv2.threshold(cv_image,128,255,cv2.THRESH_BINARY_INV)
        cv_image = cv2.resize(cv_image,(28,28))
        cv_image = np.reshape(cv_image,(1,28,28,1))
        y_conv1 = self._session.run(self.y_conv, feed_dict={self.x:cv_image})
        y = np.argmax(y_conv1,1)
        rospy.loginfo('%d' % y)
        self._pub.publish(y)

    def main(self):
        rospy.spin()

if __name__ == '__main__':
    rospy.init_node('rostensorflow')
    tensor = RosTensorFlow()
    tensor.main()

