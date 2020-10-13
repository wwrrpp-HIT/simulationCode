import vrep
import time
import numpy as np
import math
import keyword


DEG = math.pi / 180
# V-REP data transmission modes:WAIT=BLOCKING mode
WAIT = vrep.simx_opmode_oneshot_wait
ONESHOT = vrep.simx_opmode_oneshot
STREAMING = vrep.simx_opmode_streaming
BUFFER = vrep.simx_opmode_buffer
BLOCKING = vrep.simx_opmode_blocking

clientID = -1
nbrOfRobot = 4
robotID=[]; fl_joint=[]; fr_joint=[]; bl_joint=[]; br_joint=[]
body = [robotID, fl_joint, fr_joint, bl_joint, br_joint]


def show_msg(message):
    """ send a message for printing in V-REP """
    vrep.simxAddStatusbarMessage(clientID, message, WAIT)
    return

def connect():
    """ Connect to the simulator"""
    ip = '127.0.0.1'
    port = 19999
    vrep.simxFinish(-1)  # just in case, close all opened connections
    global clientID
    clientID = vrep.simxStart(ip, port, True, True, 3000, 5)
    # Connect to V-REP
    if clientID == -1:
        import sys
        sys.exit('\nV-REP remote API server connection failed (' + ip + ':' +
                 str(port) + '). Is V-REP running?')
    print('Connected to Remote API Server')  # show in the terminal
    show_msg('Python: Hello')    # show in the VREP
    time.sleep(0.5)
    return

def disconnect():
    """ Disconnect from the simulator"""
    # Make sure that the last command sent has arrived
    vrep.simxGetPingTime(clientID)
    show_msg('ROBOT: Bye')
    # Now close the connection to V-REP:
    vrep.simxFinish(clientID)
    time.sleep(0.5)
    return

def start():
    """ Start the simulation (force stop and setup)"""
    # stop()
    # setup_devices()
    # vrep.simxStartSimulation(clientID, ONESHOT)
    # time.sleep(0.5)
    # Solve a rare bug in the simulator by repeating:
    setup_first_handles(clientID, body)
    vrep.simxStartSimulation(clientID, ONESHOT)
    show_msg('start')
    print('--simulation start--')
    time.sleep(0.5)
    return

def stop():
    """ Stop the simulation """
    vrep.simxStopSimulation(clientID, ONESHOT)
    time.sleep(0.5)

def setup_first_handles(clientID, body):
    """ Assign the devices from the simulator to specific IDs """
    global robotID, fl_motorID, fr_motorID, br_motorID, bl_motorID, ultraID, rewardRefID, goalID, left_collisionID, right_collisionID
    # res: result (1(OK), -1(error), 0(not called))??手册里查到0（return ok）
    # 有几个需要控制的对象就需要加几个simxGetObjectHandle函数
    # robot
    body[0].append(vrep.simxGetObjectHandle(clientID, 'RMB', WAIT)[1])
    # motors
    body[1].append(vrep.simxGetObjectHandle(clientID, 'front_left_joint', WAIT)[1])
    body[2].append(vrep.simxGetObjectHandle(clientID, 'front_right_joint', WAIT)[1])
    body[3].append(vrep.simxGetObjectHandle(clientID, 'back_left_joint', WAIT)[1])
    body[4].append(vrep.simxGetObjectHandle(clientID, 'back_right_joint', WAIT)[1])

    # # ultrasonic sensors
    # for idx, item in enumerate(config.ultra_distribution):
    #     res, ultraID[idx] = vrep.simxGetObjectHandle(clientID, item, WAIT)
    # # reward reference distance object
    # res, rewardRefID = vrep.simxGetDistanceHandle(clientID, 'Distance#', WAIT)
    # # if res == vrep.simx_return_ok:  # [debug]
    # #    print("vrep.simxGetDistanceHandle executed fine")
    #
    # # goal reference object
    # res, goalID = vrep.simxGetObjectHandle(clientID, 'Dummy#', WAIT)
    # # collision object
    # res, left_collisionID = vrep.simxGetCollisionHandle(clientID, "leftCollision#", BLOCKING)
    # res, right_collisionID = vrep.simxGetCollisionHandle(clientID, "rightCollision#", BLOCKING)

#很重要的一点就是在读取传感器的值的时候，第一次读取的参数设置与后面读取的参数设置不同，可以把第一次读取传感器理解为传感器的初始化。
#operationMode: a remote API function operation mode. Recommended operation modes for this function are simx_opmode_streaming (the first call) and simx_opmode_buffer (the following calls)
    # vrep.simxSetJointTargetVelocity(clientID, left_motorID, 0, STREAMING)
    # vrep.simxSetJointTargetVelocity(clientID, right_motorID, 0, STREAMING)
    # # pose
    # vrep.simxGetObjectPosition(clientID, robotID, -1, MODE_INI)
    # vrep.simxGetObjectOrientation(clientID, robotID, -1, MODE_INI)
    # #
    # # # reading-related function initialization according to the recommended operationMode
    # for i in ultraID:
    #     vrep.simxReadProximitySensor(clientID, i, STREAMING)
    # vrep.simxReadDistance(clientID, rewardRefID, STREAMING)
    # vrep.simxReadCollision(clientID, left_collisionID, STREAMING)
    # vrep.simxReadCollision(clientID, right_collisionID, STREAMING)
    # return
connect()
start()
for i in range(1, 5):
    vrep.simxSetJointTargetVelocity(clientID, body[i][0], 30*DEG, BLOCKING)






# vrep.simxFinish(clientId)
# print('program ended')