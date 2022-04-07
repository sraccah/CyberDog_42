from os import system
from time import sleep
# Com protocol
import grpc
# CyberDog Library
import cyberdog_app_pb2
import cyberdog_app_pb2_grpc
# Keyboard control
import keyboard

# MENU Config
MENU_MAX = 80

class Vector3:
    x: float = 0
    y: float = 0
    z: float = 0

    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z
        pass


MAX_SPEED = 16

stub = None
cyberdog_ip = '192.168.9.21'  # Write Your Cyberdog IP Here or Input while running
speed_lv = 1
linear = Vector3(0, 0, 0)
angular = Vector3(0, 0, 0)


# Send HiFive Cmd to Cyberdog
def HiFiveCMD():
    # Open GRPC channel
    global cyberdog_ip
    if (cyberdog_ip is None):
        cyberdog_ip = input('Cyberdog Ip:')
    with grpc.insecure_channel(str(cyberdog_ip) + ':50051') as channel:
        print("Wait connect")
        try:
            grpc.channel_ready_future(channel).result(timeout=10)
        except grpc.FutureTimeoutError:
            print("Connect error, Timeout")
            return
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
                        control_mode=cyberdog_app_pb2.CheckoutMode_request.MANUAL,
                        mode_type=0     # seem not need
                    )),
                timeout=10))
        succeed_state = False
        for resp in response:
            succeed_state = resp.succeed
            print('Execute Stand up, result:' + str(succeed_state))

        # Execute HI_FIVE order
        if (succeed_state == False):
            return
        response = stub.setExtmonOrder(
            cyberdog_app_pb2.ExtMonOrder_Request(
                order=cyberdog_app_pb2.MonOrder(
                    id=cyberdog_app_pb2.MonOrder.MONO_ORDER_HI_FIVE,
                    para=0      # seem not need
                ),
                timeout=50))
        for resp in response:
            succeed_state = resp.succeed
            print('Execute HI_FIVE order, result:' + str(succeed_state))

        # Get down
        if (succeed_state == False):
            return
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
                        control_mode=cyberdog_app_pb2.CheckoutMode_request.DEFAULT,
                        mode_type=0     # seem not need
                    )),
                timeout=10))
        for resp in response:
            succeed_state = resp.succeed
            print('Execute Get down, result:' + str(succeed_state))

# Send Welcome Cmd to Cyberdog
def WelcomeCMD():
    # Open grpc channel
    global cyberdog_ip
    if (cyberdog_ip is None):
        cyberdog_ip = input('Cyberdog Ip:')
    with grpc.insecure_channel(str(cyberdog_ip) + ':50051') as channel:
        print("Wait connect")
        try:
            grpc.channel_ready_future(channel).result(timeout=10)
        except grpc.FutureTimeoutError:
            print("Connect error, Timeout")
            return
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
                        control_mode=cyberdog_app_pb2.CheckoutMode_request.MANUAL,
                        mode_type=0     # seem not need
                    )),
                timeout=10))
        succeed_state = False
        for resp in response:
            succeed_state = resp.succeed
            print('Execute Stand up, result:' + str(succeed_state))

        # Execute Welcome order
        if (succeed_state == False):
            return
        response = stub.setExtmonOrder(
            cyberdog_app_pb2.ExtMonOrder_Request(
                order=cyberdog_app_pb2.MonOrder(
                    id=cyberdog_app_pb2.MonOrder.MONO_ORDER_WELCOME,
                    para=0      # seem not need
                ),
                timeout=50))
        for resp in response:
            succeed_state = resp.succeed
            print('Execute Welcome order, result:' + str(succeed_state))

        # Get down
        if (succeed_state == False):
            return
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
                        control_mode=cyberdog_app_pb2.CheckoutMode_request.DEFAULT,
                        mode_type=0     # seem not need
                    )),
                timeout=10))
        for resp in response:
            succeed_state = resp.succeed
            print('Execute Get down, result:' + str(succeed_state))

# Send Roll Cmd to Cyberdog
def RollCMD():
    # Open grpc channel
    global cyberdog_ip
    if (cyberdog_ip is None):
        cyberdog_ip = input('Cyberdog Ip:')
    with grpc.insecure_channel(str(cyberdog_ip) + ':50051') as channel:
        print("Wait connect")
        try:
            grpc.channel_ready_future(channel).result(timeout=10)
        except grpc.FutureTimeoutError:
            print("Connect error, Timeout")
            return
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
                        control_mode=cyberdog_app_pb2.CheckoutMode_request.MANUAL,
                        mode_type=0     # seem not need
                    )),
                timeout=10))
        succeed_state = False
        for resp in response:
            succeed_state = resp.succeed
            print('Execute Stand up, result:' + str(succeed_state))

        # Execute PROSTRATE order
        if (succeed_state == False):
            return
        response = stub.setExtmonOrder(
            cyberdog_app_pb2.ExtMonOrder_Request(
                order=cyberdog_app_pb2.MonOrder(
                    id=cyberdog_app_pb2.MonOrder.MONO_ORDER_PROSTRATE,
                    para=0      # seem not need
                ),
                timeout=50))
        for resp in response:
            succeed_state = resp.succeed
            print('Execute Roll order, result:' + str(succeed_state))

        # Get down
        if (succeed_state == False):
            return
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
                        control_mode=cyberdog_app_pb2.CheckoutMode_request.DEFAULT,
                        mode_type=0     # seem not need
                    )),
                timeout=10))
        for resp in response:
            succeed_state = resp.succeed
            print('Execute Get down, result:' + str(succeed_state))

# Send Dance Cmd to Cyberdog
def DanceCMD():
    # Open grpc channel
    global cyberdog_ip
    if (cyberdog_ip is None):
        cyberdog_ip = input('Cyberdog Ip:')
    with grpc.insecure_channel(str(cyberdog_ip) + ':50051') as channel:
        print("Wait connect")
        try:
            grpc.channel_ready_future(channel).result(timeout=10)
        except grpc.FutureTimeoutError:
            print("Connect error, Timeout")
            return
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
                        control_mode=cyberdog_app_pb2.CheckoutMode_request.MANUAL,
                        mode_type=0     # seem not need
                    )),
                timeout=10))
        succeed_state = False
        for resp in response:
            succeed_state = resp.succeed
            print('Execute Stand up, result:' + str(succeed_state))

        # Execute Dance order
        if (succeed_state == False):
            return
        response = stub.setExtmonOrder(
            cyberdog_app_pb2.ExtMonOrder_Request(
                order=cyberdog_app_pb2.MonOrder(
                    id=cyberdog_app_pb2.MonOrder.MONO_ORDER_DANCE,
                    para=0      # seem not need
                ),
                timeout=50))
        for resp in response:
            succeed_state = resp.succeed
            print('Execute Dance order, result:' + str(succeed_state))

        # Get down
        if (succeed_state == False):
            return
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
                        control_mode=cyberdog_app_pb2.CheckoutMode_request.DEFAULT,
                        mode_type=0     # seem not need
                    )),
                timeout=10))
        for resp in response:
            succeed_state = resp.succeed
            print('Execute Get down, result:' + str(succeed_state))

def PrintState():
    print('Now speed:%.1fm/s' % float(speed_lv*0.1))
    print('W:GoFront')
    print('S:GoBack')
    print('A:GoLeft')
    print('D:GoRight')
    print('Q:TurnLeft')
    print('E:TurnRight')
    print('U:SpeedUp')
    print('I:SpeedDown')
    print('ESC:Exit Control')

def PrintPoses():
    print('Now speed:%.1fm/s' % float(speed_lv*0.1))
    print('U:UpPose')
    print('C:ConfigPose')
    print('L:LockPose')
    print('S:SemiPose')
    print('I:DownPose')
    print('ESC:Exit Control')

def SendData():
    global stub
    system('clear')
    PrintState()
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


def GoForward(Event):
    linear.x = 0.1 * speed_lv
    linear.y = 0
    angular.z = 0
    SendData()


def GoBack(Event):
    linear.x = -0.1 * speed_lv
    linear.y = 0
    angular.z = 0
    SendData()


def GoLeft(Event):
    linear.x = 0
    linear.y = 0.1 * speed_lv
    angular.z = 0
    SendData()


def GoRight(Event):
    linear.x = 0
    linear.y = -0.1 * speed_lv
    angular.z = 0
    SendData()


def TurnLeft(Event):
    linear.x = 0
    linear.y = 0
    angular.z = 0.1 * speed_lv
    SendData()


def TurnRight(Event):
    linear.x = 0
    linear.y = 0
    angular.z = -0.1 * speed_lv
    SendData()


def Stop(Event):
    linear.x = 0
    linear.y = 0
    angular.z = 0
    SendData()


def SpeedUp(Event):
    global speed_lv
    speed_lv += 1
    speed_lv = min(speed_lv, MAX_SPEED)


def SpeedDown(Event):
    global speed_lv
    speed_lv -= 1
    speed_lv = max(speed_lv, 1)

# Send Move Cmd to Cyberdog
def KeyboardControl():
    global stub
    global cyberdog_ip
    if (cyberdog_ip is None):
        cyberdog_ip = input('Cyberdog Ip:')
    with grpc.insecure_channel(str(cyberdog_ip) + ':50051') as channel:
        print("Wait connect")
        try:
            grpc.channel_ready_future(channel).result(timeout=10)
        except grpc.FutureTimeoutError:
            print("Connect error, Timeout")
            return
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
                        control_mode=cyberdog_app_pb2.CheckoutMode_request.MANUAL,
                        mode_type=0     # seem not need
                    )),
                timeout=10))
        succeed_state = False
        for resp in response:
            succeed_state = resp.succeed
            print('Execute Stand up, result:' + str(succeed_state))

        # Change gait to walk
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
                        gait_pattern=cyberdog_app_pb2.Pattern.GAIT_TROT
                    )
                ),
                timeout=10
            )
        )
        for resp in response:
            succeed_state = resp.succeed
            print('Change gait to walk, result:' + str(succeed_state))

        # Send Move Cmd
        if (succeed_state == False):
            return
        PrintState()
        keyboard.on_press_key('w', GoForward)
        keyboard.on_press_key('s', GoBack)
        keyboard.on_press_key('a', GoLeft)
        keyboard.on_press_key('d', GoRight)
        # ARROWS CODES TO NAVIGUATE
        keyboard.on_press_key('up', GoForward)
        keyboard.on_press_key('down', GoBack)
        keyboard.on_press_key('left', TurnLeft)
        keyboard.on_press_key('right', TurnRight)
        # ROTATE
        keyboard.on_press_key('q', TurnLeft)
        keyboard.on_press_key('e', TurnRight)
        # VELOCIDAD
        keyboard.on_press_key('u', SpeedUp)
        keyboard.on_press_key('i', SpeedDown)
        # STOP each time we release the key
        keyboard.on_release(Stop)
        keyboard.wait('esc')
        system('clear')

        # Get down
        if (succeed_state == False):
            return
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
                        control_mode=cyberdog_app_pb2.CheckoutMode_request.DEFAULT,
                        mode_type=0     # seem not need
                    )),
                timeout=10))
        for resp in response:
            succeed_state = resp.succeed
            print('Execute Get down, result:' + str(succeed_state))

def UpPose():
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
                    control_mode=cyberdog_app_pb2.CheckoutMode_request.MANUAL,
                    mode_type=0     # seem not need
                )),
            timeout=10))
    succeed_state = False
    for resp in response:
        succeed_state = resp.succeed
        print('Execute Stand up, result:' + str(succeed_state))
    return succeed_state

def ConfigPose():
    # Get Config Pose
    if (succeed_state == False):
        return
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
                    control_mode=cyberdog_app_pb2.CheckoutMode_request.CONFIG,
                    mode_type=0     # seem not need
                )),
            timeout=10))
    for resp in response:
        succeed_state = resp.succeed
        print('Execute Config Pose, result:' + str(succeed_state))
    return succeed_state

def DownPose():
    # Get down
    if (succeed_state == False):
        return
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
                    control_mode=cyberdog_app_pb2.CheckoutMode_request.DEFAULT,
                    mode_type=0     # seem not need
                )),
            timeout=10))
    for resp in response:
        succeed_state = resp.succeed
        print('Execute Get down, result:' + str(succeed_state))
    return succeed_state

def LockPose():
    # Get down
    if (succeed_state == False):
        return
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
                    control_mode=cyberdog_app_pb2.CheckoutMode_request.LOCK,
                    mode_type=0     # seem not need
                )),
            timeout=10))
    for resp in response:
        succeed_state = resp.succeed
        print('Execute Lock pose, result:' + str(succeed_state))
    return succeed_state

def SemiPose():
    # Get down
    if (succeed_state == False):
        return
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
                    control_mode=cyberdog_app_pb2.CheckoutMode_request.SEMI,
                    mode_type=0     # seem not need
                )),
            timeout=10))
    for resp in response:
        succeed_state = resp.succeed
        print('Execute Semi pose, result:' + str(succeed_state))
    return succeed_state

def PosesControl():
    global stub
    global cyberdog_ip
    if (cyberdog_ip is None):
        cyberdog_ip = input('Cyberdog Ip:')
    with grpc.insecure_channel(str(cyberdog_ip) + ':50051') as channel:
        print("Wait connect")
        try:
            grpc.channel_ready_future(channel).result(timeout=10)
        except grpc.FutureTimeoutError:
            print("Connect error, Timeout")
            return
        stub = cyberdog_app_pb2_grpc.CyberdogAppStub(channel)
        succeed_state = UpPose()
        # Send Move Cmd
        if (succeed_state == False):
            return
        PrintPoses()
        # Poses
        keyboard.on_press_key('u', UpPose)
        keyboard.on_press_key('c', ConfigPose)
        keyboard.on_press_key('l', LockPose)
        keyboard.on_press_key('s', SemiPose)
        keyboard.on_press_key('d', DownPose)
        keyboard.wait('esc')
        system('clear')
        DownPose()

# Send Bow Cmd to Cyberdog
def TestCMD():
    # Open grpc channel
    global cyberdog_ip
    if (cyberdog_ip is None):
        cyberdog_ip = input('Cyberdog Ip:')
    with grpc.insecure_channel(str(cyberdog_ip) + ':50051') as channel:
        print("Wait connect")
        try:
            grpc.channel_ready_future(channel).result(timeout=10)
        except grpc.FutureTimeoutError:
            print("Connect error, Timeout")
            return
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
                        control_mode=cyberdog_app_pb2.CheckoutMode_request.MANUAL,
                        mode_type=0     # seem not need
                    )),
                timeout=10))
        succeed_state = False
        for resp in response:
            succeed_state = resp.succeed
            print('Execute Stand up, result:' + str(succeed_state))
        # Execute order
        if (succeed_state == False):
            return
        response = stub.setExtmonOrder(
            cyberdog_app_pb2.ExtMonOrder_Request(
                order=cyberdog_app_pb2.MonOrder(
                    id=cyberdog_app_pb2.MonOrder.MONO_ORDER_BOW,
                    para=0      # seem not need
                ),
                timeout=50))
        for resp in response:
            succeed_state = resp.succeed
            print('Execute Bow order, result:' + str(succeed_state))
        sleep(2)
        # Execute order
        # if (succeed_state == False):
        #     return
        # response = stub.setExtmonOrder(
        #     cyberdog_app_pb2.ExtMonOrder_Request(
        #         order=cyberdog_app_pb2.MonOrder(
        #             id=cyberdog_app_pb2.MonOrder.MONO_ORDER_WELCOME,
        #             para=0      # seem not need
        #         ),
        #         timeout=50))
        # for resp in response:
        #     succeed_state = resp.succeed
        #     print('Execute Welcome order, result:' + str(succeed_state))
        # sleep(2)
        # Execute order
        if (succeed_state == False):
            return
        response = stub.setExtmonOrder(
            cyberdog_app_pb2.ExtMonOrder_Request(
                order=cyberdog_app_pb2.MonOrder(
                    id=cyberdog_app_pb2.MonOrder.MONO_ORDER_SIT,
                    para=0      # seem not need
                ),
                timeout=50))
        for resp in response:
            succeed_state = resp.succeed
            print('Execute Sit order, result:' + str(succeed_state))
        # Get down
        if (succeed_state == False):
            return
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
                        control_mode=cyberdog_app_pb2.CheckoutMode_request.DEFAULT,
                        mode_type=0     # seem not need
                    )),
                timeout=10))
        for resp in response:
            succeed_state = resp.succeed
            print('Execute Get down, result:' + str(succeed_state))

def print_menu():
    menuTab = [' MENU ', '-', 'Else. Exit']
    cmdTab = ['1. HiFiveCMD', '2. WelcomeCMD', '3. RollCMD', '4. DanceCMD', '5. TestCMD']
    controlTab = ['6. KeyboardControl', '7. PosesControl']
    tabs = [cmdTab, controlTab]
    print(int((MENU_MAX - len(menuTab[0])) / 2) * "-" , menuTab[0].strip(' '), int((MENU_MAX - len(menuTab[0])) / 2) * "-")
    for elem in tabs:
        for cmd in elem:
            print(cmd)
    print("Else. Exit")
    print(MENU_MAX * "-")

if __name__ == '__main__':
    while True:
        print_menu()
        choice = input("Enter your choice [1-5]: ")
        if choice == '1':     
            print("Menu 1 has been selected")
            HiFiveCMD()
        elif choice == '2':
            print("Menu 2 has been selected")
            WelcomeCMD()
        elif choice == '3':
            print("Menu 3 has been selected")
            RollCMD()
        elif choice == '4':
            print("Menu 4 has been selected")
            DanceCMD()
        elif choice == '5':
            print("Menu 4 has been selected")
            # TestCMD()
        elif choice == '6':
            print("Menu 4 has been selected")
            KeyboardControl()
        elif choice == '7':
            print("Menu 4 has been selected")
            PosesControl()
        else:
            print("Thanks for using the program. Bye bye!")
            break
