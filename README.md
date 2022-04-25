# CyberDog Protocol using GRPC and Python

## **Installation**

First of all, you need to install the `grpc` module:

```bash
sudo pip3 install grpcio
sudo pip3 install grpcio-tools
```

From the [Xiaomi CyberDog Protocol Repository](https://partner-gitlab.mioffice.cn/cyberdog/athena_cyberdog/-/tree/devel/athena_common/athena_grpc/protos), download the proto file `cyberdog_app.proto` and use the following command to generate the python module:

```bash
python3 -m grpc_tools.protoc --python_out=. --grpc_python_out=. -I. *.proto
```

Be sure that the files generated are named `cyberdog_app_pb2.py` and `cyberdog_app_pb2_grpc.py` and that the modules are in the same directory.

## **Optional**

You also can install the keyboard python module to easily control the keyboard:

```bash
sudo pip3 install keyboard
```

A requirements file is available, to just do:

```bash
pip3 install -r requirements.txt
```

## **Scripting time**

Next, you can begin to script to connect to the CyberDog and check if the GRPC connection is open and is working:

```python
from os import system
# Com protocol
import grpc
# CyberDog Library
import cyberdog_app_pb2
import cyberdog_app_pb2_grpc

# Open GRPC channel
with grpc.insecure_channel(str(CYBERDOG_IP) + ':50051') as channel:
    print("Wait connect")
    try:
        grpc.channel_ready_future(channel).result(timeout=10)
    except grpc.FutureTimeoutError:
        print("Connexion error, Timeout")
        return
    # Get stub from channel
    stub = cyberdog_app_pb2_grpc.CyberdogAppStub(channel)
```

Next, you can use the `setMode()` function from the `stub` to send a commands to the CyberDog:

```python
# MANUAL MODE => Stand up
response = stub.setMode(
    cyberdog_app_pb2.CheckoutMode_request(
        next_mode=cyberdog_app_pb2.ModeStamped(
            header=cyberdog_app_pb2.Header(
                stamp=cyberdog_app_pb2.Timestamp(
                    sec=0,
                    nanosec=0
                ),
                frame_id=""
            ),
            mode=cyberdog_app_pb2.Mode(
                control_mode=cyberdog_app_pb2.CheckoutMode_request.MANUAL,
                mode_type=0
            )),
        timeout=10))
succeed_state = False
for resp in response:
    succeed_state = resp.succeed
    print('Execute Stand up mode called MANUAL, result:' + str(succeed_state))
```

Same thing to return to the basic state:

```python
# DEFAULT MODE => Get down
if (succeed_state == False): # in case of a previous command fail
    return
response = stub.setMode(
    cyberdog_app_pb2.CheckoutMode_request(
        next_mode=cyberdog_app_pb2.ModeStamped(
            header=cyberdog_app_pb2.Header(
                stamp=cyberdog_app_pb2.Timestamp(
                    sec=0,
                    nanosec=0
                ),
                frame_id=""
            ),
            mode=cyberdog_app_pb2.Mode(
                control_mode=cyberdog_app_pb2.CheckoutMode_request.DEFAULT,
                mode_type=0
            )),
        timeout=10))
for resp in response:
    succeed_state = resp.succeed
    print('Execute DEFAULT mode, result:' + str(succeed_state))
```

From now you can add all kind of functions and interactions with the CyberDog, thanks to the libraries available.

For exemple the keyboard module can be used to control the robot:

```python
# FORWARD and BACKWARD
keyboard.on_press_key('w', GoForward)
keyboard.on_press_key('s', GoBack)
# STRAFING
keyboard.on_press_key('a', GoLeft)
keyboard.on_press_key('d', GoRight)
# ROTATE
keyboard.on_press_key('q', TurnLeft)
keyboard.on_press_key('e', TurnRight)
# ARROWS CODES TO NAVIGUATE
keyboard.on_press_key('up', GoForward)
keyboard.on_press_key('down', GoBack)
keyboard.on_press_key('left', TurnLeft)
keyboard.on_press_key('right', TurnRight)
# VELOCIDAD
keyboard.on_press_key('u', SpeedUp)
keyboard.on_press_key('i', SpeedDown)
# STOP each time we release the key
keyboard.on_release(Stop)
```

But first you need to understand a little bit how the CyberDog works to be able to move it or interract with his sensors.

We are using the `Vector3` structure to represent the movement.

```python
# Vector3 structure
class Vector3:
    x: float = 0
    y: float = 0
    z: float = 0

    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z
        pass
```

And this allow us to prepare some parameters to send to the CyberDog:

```python
speed_lv = 1 # From 0.1 to 1.6
linear = Vector3(0, 0, 0)
angular = Vector3(0, 0, 0)
```

To send the datas to the CyberDog you will use the stub to access the `sendAppDecision()` function:

```python
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
```

Let's say you create a function to send the datas named `SendData`, you just have to create other functions to update the parameters you want to send to the CyberDog:

```python
def GoForward(Event):
    linear.x = 0.1 * speed_lv
    linear.y = 0
    angular.z = 0
    SendData()
```

Always be sure to have a `stop` function to stop the robot:

```python
def Stop(Event):
    linear.x = 0
    linear.y = 0
    angular.z = 0
    SendData()
```

Go back to the keyboard part of this document to see how we can use these functions and the keyboard to control the robot.

We saw the `setMode()` function but there is a lot of posibilities, for exemple the `setExtmonOrder()` to use a predefined action from the list below:

```python
MONO_ORDER_NULL        =  0;
MONO_ORDER_WAKE_STOP   =  1;
MONO_ORDER_SHUT_STOP   =  2;
MONO_ORDER_STAND_UP    =  9;
MONO_ORDER_PROSTRATE   = 10;
MONO_ORDER_COME_HERE   = 11;
MONO_ORDER_STEP_BACK   = 12;
MONO_ORDER_TURN_AROUND = 13;
MONO_ORDER_HI_FIVE     = 14;
MONO_ORDER_DANCE       = 15;
MONO_ORDER_WELCOME     = 16;
MONO_ORDER_TURN_OVER   = 17;
MONO_ORDER_SIT         = 18;
MONO_ORDER_BOW         = 19;
MONO_ORDER_MAX         = 20;
```

The modes are defining the standing position of the CyberDog and are:

```python
DEFAULT = 0; # default mode seen earlier (Get down)
LOCK = 1;
CONFIG = 2;
MANUAL = 3; # manual mode seen earlier (Stand up)
SEMI = 13;
EXPLOR = 14;
TRACK = 15;
```

The moving patterns are called `GAIT` and are defining the way the CyberDog will move. (the walking style as we may say)

```python
GAIT_TRANS     = 0;
GAIT_PASSIVE   = 1;
GAIT_KNEEL     = 2;
GAIT_STAND_R   = 3;
GAIT_STAND_B   = 4;
GAIT_AMBLE     = 5;
GAIT_WALK      = 6;
GAIT_SLOW_TROT = 7;
GAIT_TROT      = 8;
GAIT_FLYTROT   = 9;
GAIT_BOUND     = 10;
GAIT_PRONK     = 11;
GAIT_DEFAULT   = 99;
```

So we can use the `setExtmonOrder()` function to set the mode:

```python
# Previous code to connect and stand up
# ...
# Execute Dance order
if (succeed_state == False):
    return
response = stub.setExtmonOrder(
    cyberdog_app_pb2.ExtMonOrder_Request(
        order=cyberdog_app_pb2.MonOrder(
            id=cyberdog_app_pb2.MonOrder.MONO_ORDER_DANCE,
            para=0
        ),
        timeout=50))
for resp in response:
    succeed_state = resp.succeed
    print('Execute Dance order, result:' + str(succeed_state))
```

And the `setPattern()` function to set the gait:

```python
# Change gait to trot
response = stub.setPattern(
    cyberdog_app_pb2.CheckoutPattern_request(
        patternstamped=cyberdog_app_pb2.PatternStamped(
            header=cyberdog_app_pb2.Header(
                stamp=cyberdog_app_pb2.Timestamp(
                    sec=0,
                    nanosec=0
                ),
                frame_id=""
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
    print('Change gait to trot, result:' + str(succeed_state))
```

## **NOTICE**

Using the mobile application and a computer, or two computers, AT THE SAME TIME to control the robot is not adviced as it's giving contradictory signals to the Cyberdog.
