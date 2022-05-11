from os import system
from time import sleep
# Com protocol
import grpc
# CyberDog Library
import cyberdog_app_pb2
import cyberdog_app_pb2_grpc
# Keyboard control
import keyboard
# Pad Controller
import pygame
from pygame.locals import *
# Video Handling
import moviepy.editor
import cv2

# Posición actual
x_coord = 10
y_coord = 10

# MENU Config
MENU_MAX = 80
# SPEED
MAX_SPEED = 16

STANCES = {
    'DOWN': cyberdog_app_pb2.CheckoutMode_request.DEFAULT,
    'UP': cyberdog_app_pb2.CheckoutMode_request.MANUAL,
    'SEMI': cyberdog_app_pb2.CheckoutMode_request.SEMI,
    'EXPLOR': cyberdog_app_pb2.CheckoutMode_request.EXPLOR,
    'TRACK': cyberdog_app_pb2.CheckoutMode_request.TRACK,
}

GAITS = {
    'DEFAULT': cyberdog_app_pb2.Pattern.GAIT_DEFAULT,
    'FLYTROT': cyberdog_app_pb2.Pattern.GAIT_FLYTROT,
    'TROT': cyberdog_app_pb2.Pattern.GAIT_FLYTROT,
    'WALK': cyberdog_app_pb2.Pattern.GAIT_WALK,
    'BOUND': cyberdog_app_pb2.Pattern.GAIT_BOUND,
    'PRONK': cyberdog_app_pb2.Pattern.GAIT_PRONK,
    'AMBLE': cyberdog_app_pb2.Pattern.GAIT_AMBLE,
}

MODES = {
    'WELCOME': cyberdog_app_pb2.MonOrder.MONO_ORDER_WELCOME,
    'DANCE': cyberdog_app_pb2.MonOrder.MONO_ORDER_DANCE,
    'PROSTRATE': cyberdog_app_pb2.MonOrder.MONO_ORDER_PROSTRATE,
    'HIFIVE': cyberdog_app_pb2.MonOrder.MONO_ORDER_HI_FIVE,
    'TURNOVER': cyberdog_app_pb2.MonOrder.MONO_ORDER_TURN_OVER,
    'MAX': cyberdog_app_pb2.MonOrder.MONO_ORDER_MAX,
}


class Vector3:
    x: float = 0
    y: float = 0
    z: float = 0

    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z
        pass


# stub = None
cyberdog_ip = '192.168.243.21'  # Write Your Cyberdog IP Here or Input while running
speed_lv = 1
linear = Vector3(0, 0, 0)
angular = Vector3(0, 0, 0)


class CyberDog:
    def __init__(self, ip: str) -> None:
        self.stub = None
        self.cyberdog_ip = ip  # Write Your Cyberdog IP Here or Input while running
        self.speed_lv = 1
        self.linear = Vector3(0, 0, 0)
        self.angular = Vector3(0, 0, 0)


pygame.init()

# Hacemos un recuento del número de joysticks conectados al ordenador
joystick_count = pygame.joystick.get_count()
if joystick_count == 0:
    # No joysticks!
    print("Error, No he encontrado ningún joystick.")
    exit()
else:
    # Usa el joystick #0 y lo inicializa
    mi_joystick = pygame.joystick.Joystick(0)
    mi_joystick.init()
    # Get the name from the OS for the controller/joystick.
    name = mi_joystick.get_name()
    print("Joystick name: {}".format(name))

    # Usually axis run in pairs, up/down for one, and left/right for
    # the other.
    # axes = mi_joystick.get_numaxes()
    # print("Number of axes: {}".format(axes))

    # for i in range(axes):
    #     axis = mi_joystick.get_axis(i)
    #     print("Axis {} value: {:>6.3f}".format(i, axis))

    # buttons = mi_joystick.get_numbuttons()
    # print("Number of buttons: {}".format(buttons))

    # for i in range(buttons):
    #     button = mi_joystick.get_button(i)
    #     print("Button {:>2} value: {}".format(i, button))

    # hats = mi_joystick.get_numhats()
    # print("Number of hats: {}".format(hats))

    # # Hat position. All or nothing for direction, not a float like
    # # get_axis(). Position is a tuple of int values (x, y).
    # for i in range(hats):
    #     hat = mi_joystick.get_hat(i)
    #     print("Hat {} value: {}".format(i, str(hat)))


def PrintState():
    print('Now speed:%.1fm/s' % float(speed_lv*0.1))
    print('--------- KEYBOARD CONTROL ----------')
    print('W : GoFront')
    print('S : GoBack')
    print('A : GoLeft')
    print('D : GoRight')
    print('Q : TurnLeft')
    print('E : TurnRight')
    print('U : SpeedUp')
    print('I : SpeedDown')
    print('--------- GAMEPAD CONTROL ----------')
    print('Left Stick : Move')
    print('Right Stick : Straff')
    print('A : SpeedUp')
    print('B : SpeedDown')
    print('Up Arrow : Stand Up')
    print('Down Arrow : Get Down')
    print('ESC :Exit Control')


def SendData(channel):
    # Get stub from channel
    stub = cyberdog_app_pb2_grpc.CyberdogAppStub(channel)
    # system('clear')
    # PrintState()
    stub.sendAppDecision(
        cyberdog_app_pb2.Decissage(
            twist=cyberdog_app_pb2.Twist(
                linear=cyberdog_app_pb2.Vector3(
                    x=linear.x,
                    y=linear.y,
                    z=linear.z
                ),
                angular=cyberdog_app_pb2.Vector3(
                    x=angular.x,
                    y=angular.y,
                    z=angular.z
                )
            )
        )
    )


def GoForward(channel):
    linear.x = 0.1 * speed_lv
    linear.y = 0
    angular.z = 0
    SendData(channel)


def GoBack(channel):
    linear.x = -0.1 * speed_lv
    linear.y = 0
    angular.z = 0
    SendData(channel)


def GoLeft(channel):
    linear.x = 0
    linear.y = 0.1 * speed_lv
    angular.z = 0
    SendData(channel)


def GoRight(channel):
    linear.x = 0
    linear.y = -0.1 * speed_lv
    angular.z = 0
    SendData(channel)


def TurnLeft(channel):
    linear.x = 0
    linear.y = 0
    angular.z = 0.1 * speed_lv
    SendData(channel)


def TurnRight(channel):
    linear.x = 0
    linear.y = 0
    angular.z = -0.1 * speed_lv
    SendData(channel)


def Stop(channel):
    linear.x = 0
    linear.y = 0
    angular.z = 0
    SendData(channel)


def SpeedUp(Event):
    global speed_lv
    speed_lv += 1
    speed_lv = min(speed_lv, MAX_SPEED)


def SpeedDown(Event):
    global speed_lv
    speed_lv -= 1
    speed_lv = max(speed_lv, 1)


def SetSpeed(Event, speed):
    global speed_lv
    speed_lv = speed
    speed_lv = min(speed_lv, MAX_SPEED)


def SetStance(channel, mode):
    succeed_state = False
    # Get stub from channel
    stub = cyberdog_app_pb2_grpc.CyberdogAppStub(channel)
    # Stand up
    response = stub.setMode(
        cyberdog_app_pb2.CheckoutMode_request(
            next_mode=cyberdog_app_pb2.ModeStamped(
                header=cyberdog_app_pb2.Header(
                    stamp=cyberdog_app_pb2.Timestamp(
                        sec=0,      # seem not need
                        nanosec=0   # seem not need
                    ),
                    frame_id=""     # seem not need
                ),
                mode=cyberdog_app_pb2.Mode(
                    control_mode=mode,
                    mode_type=0     # seem not need
                )),
            timeout=10))
    for resp in response:
        succeed_state = resp.succeed
        print('Changing mode, result:' + str(succeed_state))
    return succeed_state


def SetGait(channel, mode):
    # Get stub from channel
    stub = cyberdog_app_pb2_grpc.CyberdogAppStub(channel)
    succeed_state = False
    # Change gait to mode
    response = stub.setPattern(
        cyberdog_app_pb2.CheckoutPattern_request(
            patternstamped=cyberdog_app_pb2.PatternStamped(
                header=cyberdog_app_pb2.Header(
                    stamp=cyberdog_app_pb2.Timestamp(
                        sec=0,      # seem not need
                        nanosec=0   # seem not need
                    ),
                    frame_id=""     # seem not need
                ),
                pattern=cyberdog_app_pb2.Pattern(
                    gait_pattern=mode
                )
            ),
            timeout=10
        )
    )
    for resp in response:
        succeed_state = resp.succeed
        print('Changing gait, result:' + str(succeed_state))
    return succeed_state


def SetMode(channel, mode):
    # Get stub from channel
    stub = cyberdog_app_pb2_grpc.CyberdogAppStub(channel)
    response = stub.setExtmonOrder(
        cyberdog_app_pb2.ExtMonOrder_Request(
            order=cyberdog_app_pb2.MonOrder(
                id=mode,
                para=0      # seem not need
            ),
            timeout=50))
    for resp in response:
        succeed_state = resp.succeed
        print('Execute Welcome order, result:' + str(succeed_state))


def GetStatus(channel):
    # Get stub from channel
    stub = cyberdog_app_pb2_grpc.CyberdogAppStub(channel)
    response = stub.subscribeStatus(cyberdog_app_pb2.StatusStamped())
    for resp in response:
        succeed_state = resp.succeed
        print('Get Status, result:' + str(succeed_state))


def GetTrackingStatus(channel):
    # Get stub from channel
    stub = cyberdog_app_pb2_grpc.CyberdogAppStub(channel)
    response = stub.subscribeTrackingStatus(cyberdog_app_pb2.TrackingStatus())
    for resp in response:
        succeed_state = resp.succeed
        print('Get Tracking Status, result:' + str(succeed_state))


def CyberdogControl():
    global stub
    global cyberdog_ip
    stopper = False
    if (cyberdog_ip is None):
        cyberdog_ip = input('Cyberdog Ip:')
    with grpc.insecure_channel(str(cyberdog_ip) + ':50051') as channel:
        print("Waiting for connection...")
        try:
            grpc.channel_ready_future(channel).result(timeout=10)
        except grpc.FutureTimeoutError:
            print("Connection error, Timeout")
            return

        print("Connected!!!")
        PrintState()
        #
        # EVENT PROCESSING STEP
        #
        # Possible joystick actions: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
        # JOYBUTTONUP, JOYHATMOTION
        while stopper is False:
            for event in pygame.event.get():  # User did something.
                # print(event)
                if event.type == pygame.QUIT:  # If user clicked close.
                    Stop(channel)
                    stopper = True
                elif event.type == pygame.JOYAXISMOTION:
                    # print(event.dict, event.joy, event.axis, event.value)
                    if event.axis == 0:
                        if event.value == -1.0 and event.value < 0.0:
                            # print("¡¡¡ TURN LEFT !!!")
                            TurnLeft(channel)
                        if event.value > 0.0 and event.value <= 1.0:
                            # print("¡¡¡ TURN RIGHT !!!")
                            TurnRight(channel)
                        if event.value == 0.0:
                            # print("¡¡¡ STOP !!!")
                            Stop(channel)
                    if event.axis == 1:
                        if event.value == -1.0 and event.value < 0.0:
                            # print("¡¡¡ R2 | FORWARD !!!")
                            if event.value < -0.5:
                                SetSpeed(event, 1)
                            if event.value > -0.5:
                                SetSpeed(event, 8)
                            if event.value > -0.3:
                                SetSpeed(event, 10)
                            if event.value > -0.1:
                                SetSpeed(event, 16)
                            GoForward(channel)
                        if event.value > 0.0 and event.value <= 1.0:
                            # print("¡¡¡ L2 | BACK !!!")
                            if event.value < 0.3:
                                SetSpeed(event, 1)
                            if event.value > 0.3:
                                SetSpeed(event, 8)
                            if event.value > 0.5:
                                SetSpeed(event, 10)
                            if event.value > 0.9:
                                SetSpeed(event, 16)
                            GoBack(channel)
                        if event.value == 0.0:
                            # print("¡¡¡ STOP !!!")
                            Stop(channel)
                    if event.axis == 4:
                        if event.value == 1.0:
                            # print("¡¡¡ L2 | BACK !!!")
                            GoBack(channel)
                        if event.value != 1.0:
                            # print("¡¡¡ STOP !!!")
                            Stop(channel)
                    if event.axis == 5:
                        if event.value == 1.0:
                            # print("¡¡¡ R2 | FORWARD !!!")
                            GoForward(channel)
                        if event.value != 1.0:
                            # print("¡¡¡ STOP !!!")
                            Stop(channel)
                elif event.type == pygame.JOYBUTTONDOWN:
                    # print(event.dict, event.joy, event.button)
                    if event.button == 0:
                        print("¡¡¡ SPEED UP !!!")
                        SpeedUp(None)
                    if event.button == 1:
                        print("¡¡¡ SPEED DOWN !!!")
                        SpeedDown(None)
                    # if event.button == 2:
                    #     print("to assign")
                    # if event.button == 3:
                    #     print("to assign")
                    # if event.button == 4:
                    #     print("to assign")
                    # if event.button == 5:
                    #     print("to assign")
                    # if event.button == 6:
                    #     print("to assign")
                    # if event.button == 7:
                    #     print("to assign")
                    # if event.button == 8:
                    #     print("to assign")
                    if event.button == 9:
                        # print("¡¡¡ L1 | STRAF LEFT !!!")
                        GoLeft(channel)
                    if event.button == 10:
                        # print("¡¡¡ R1 | STRAF RIGHT !!!")
                        GoRight(channel)
                    if event.button == 11:
                        # print("¡¡¡ STAND UP !!!")
                        succeed_state = SetStance(channel, STANCES['UP'])
                        # Check execution result
                        if (succeed_state == False):
                            return
                        SetGait(channel, GAITS['DEFAULT'])
                    if event.button == 12:
                        # print("¡¡¡ GET DOWN !!!")
                        succeed_state = SetStance(channel, STANCES['DOWN'])
                        # Check execution result
                        if (succeed_state == False):
                            return
                elif event.type == pygame.JOYBUTTONUP:
                    print("Joystick button released. Stopping now.")
                    Stop(channel)
                    # return False
                keyboard.wait('esc')
                stopper = True
        #
        # END_EVENT_PROCESSING_STEP
        #
        succeed_state = SetStance(channel, STANCES['DOWN'])
        # Check execution result
        if (succeed_state == False):
            return


# -------- Main Program Loop -----------
if __name__ == '__main__':
    while True:
        CyberdogControl()
        pygame.quit()
        exit()
