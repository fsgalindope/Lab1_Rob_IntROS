import rospy
from geometry_msgs.msg import Twist
from turtlesim.srv import TeleportAbsolute, TeleportRelative
from turtlesim.srv import Spawn
import termios, sys, os
from numpy import pi 

TERMIOS = termios

def getkey():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] = new[3] & ~TERMIOS.ICANON & ~TERMIOS.ECHO
    new[6][TERMIOS.VMIN] = 1
    new[6][TERMIOS.VTIME] = 0
    termios.tcsetattr(fd, TERMIOS.TCSANOW, new)
    c = None
    try:
        c = os.read(fd, 1)
    finally:
        termios.tcsetattr(fd, TERMIOS.TCSAFLUSH, old)
    return c

def toCenter():
    rospy.wait_for_service('/turtle1/teleport_absolute')
    try:
        telA=rospy.ServiceProxy('/turtle1/teleport_absolute', TeleportAbsolute)
        resp=telA(5,5,1.5)

    except rospy.ServiceException:
        pass

def giro180():
    rospy.wait_for_service('/turtle1/teleport_relative')
    try:
        telR=rospy.ServiceProxy('/turtle1/teleport_relative', TeleportRelative)
        rel=telR(0,3.1416)
    except rospy.ServiceException:
        pass

def pubVel(x, z, time):
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rospy.init_node('velPub', anonymous=True)
    vel = Twist()
    vel.linear.x = x
    vel.angular.z = z
    rospy.loginfo(vel)
    fTime = rospy.Time.now() + rospy.Duration(time)
    while  rospy.Time.now() < fTime:
        pub.publish(vel)

if __name__ == "__main__":
    while 1:
        letter = getkey()
        if(letter ==b'w' or letter == b'W'):
            print('Adelante')
            # pubVel(1,0)
            pubVel(0.4,0,0.05)
        elif(letter ==b's' or letter == b'S'):
            print('Atrás')
            pubVel(-0.4,0,0.05)
        elif(letter ==b'd' or letter == b'D'):
            print('Giro derecha')
            pubVel(0,-0.2,0.05)
        elif(letter ==b'a' or letter == b'A'):
            print('Giro izquierda')
            pubVel(0,0.2,0.05)
        elif(letter ==b'r' or letter == b'R'):
            print('Al centro')
            toCenter()
        elif(letter ==b' '):
            print('Giro 180')
            giro180()
        if (letter==b'\x1b'):
            break