# CyberDog Protocol using GRPC and Python

## **Installation**

First of all, you need to install the `grpc` module:

```bash
sudo pip install grpcio
sudo pip install grpcio-tools
```

From the repository <https://partner-gitlab.mioffice.cn/cyberdog/athena_cyberdog/-/tree/devel/athena_common/athena_grpc/protos>, download the proto file `cyberdog_app.proto` and use the following command to generate the python module:

```bash
python3 -m grpc_tools.protoc --python_out=. --grpc_python_out=. -I. *.proto
```

Be sure that the files generated are named `cyberdog_app_pb2.py` and `cyberdog_app_pb2_grpc.py` and that the modules are in the same directory.

## **Optional**

You also can install the keyboard python module to easily control the keyboard:

```bash
sudo pip install keyboard
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

Next, you can use the `stub` to send commands to the CyberDog:

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
