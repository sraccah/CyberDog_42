# Protocolo CyberDog con GRPC y Python

## **Instalación**

En primer lugar, es necesario instalar el módulo `grpc`:

```bash
sudo pip3 install grpcio
sudo pip3 install grpcio-tools
```

Desde el [Repositorio del protocolo Xiaomi CyberDog](https://partner-gitlab.mioffice.cn/cyberdog/athena_cyberdog/-/tree/devel/athena_common/athena_grpc/protos), descarga el archivo proto `cyberdog_app.proto` y utiliza el siguiente comando para generar el módulo python:

```bash
python3 -m grpc_tools.protoc --python_out=. --grpc_python_out=. -I. *.proto
```

Asegúrese de que los archivos generados se llaman `cyberdog_app_pb2.py` y `cyberdog_app_pb2_grpc.py` y que los módulos están en el mismo directorio.

## **Opcional**

También puedes instalar el módulo python keyboard para controlar fácilmente el teclado:

```bash
sudo pip3 install keyboard
sudo pip3 install pygame
```

Hay un archivo de requisitos disponible, para simplemente hacerlo:

```bash
pip3 install -r requirements.txt
```

## **Scripting time**

A continuación, puede comenzar el script para conectarse al CyberDog y comprobar si la conexión GRPC está abierta y funciona:

```python
from os import system
# Com protocol
import grpc
# CyberDog Library
import cyberdog_app_pb2
import cyberdog_app_pb2_grpc

# Open GRPC channel
with grpc.insecure_channel(str(CYBERDOG_IP) + ':50051') as channel:
    print("Esperar a que se conecte")
    try:
        grpc.channel_ready_future(channel).result(timeout=10)
    except grpc.FutureTimeoutError:
        print("Error de conexión, tiempo de espera")
        return
    # Get stub from channel
    stub = cyberdog_app_pb2_grpc.CyberdogAppStub(channel)
```

A continuación, puede utilizar la función `setMode()` del `stub` para enviar un comando al CyberDog:

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
    print('Ejecutar el modo Stand up llamado MANUAL, resultado:' + str(succeed_state))
```

Lo mismo para volver al estado básico:

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
    print('Ejecutar el modo DEFAULT, resultado:' + str(succeed_state))
```

A partir de ahora puede añadir todo tipo de funciones e interacciones con el CyberDog, gracias a las librerías disponibles.

Por ejemplo, el módulo de teclado se puede utilizar para controlar el robot:

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

Pero primero hay que entender un poco cómo funciona el CyberDog para poder moverlo o interactuar con sus sensores.

Estamos utilizando la estructura `Vector3` para representar el movimiento.

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

Y esto nos permite preparar algunos parámetros para enviar al CyberDog:

```python
speed_lv = 1 # From 0.1 to 1.6
linear = Vector3(0, 0, 0)
angular = Vector3(0, 0, 0)
```

Para enviar los datos al CyberDog se utilizará el stub para acceder a la función `sendAppDecision()`:

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

Digamos que usted crea una función para enviar los datos llamada `SendData`, sólo tiene que crear otras funciones para actualizar los parámetros que desea enviar al CyberDog:

```python
def GoForward(Event):
    linear.x = 0.1 * speed_lv
    linear.y = 0
    angular.z = 0
    SendData()
```

Asegúrese siempre de tener una función `stop` para detener el robot:

```python
def Stop(Event):
    linear.x = 0
    linear.y = 0
    angular.z = 0
    SendData()
```

Vuelve a la parte del teclado de este documento para ver cómo podemos utilizar estas funciones y el teclado para controlar el robot.

Hemos visto la función `setMode()` pero hay muchas posibilidades, por ejemplo la función `setExtmonOrder()` para usar una acción predefinida de la lista de abajo:

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

Los modos definen la posición de pie del CyberDog y son:

```python
DEFAULT = 0; # modo por defecto visto anteriormente (Get down)
LOCK = 1;
CONFIG = 2;
MANUAL = 3; # modo manual visto anteriormente (Stand up)
SEMI = 13;
EXPLOR = 14;
TRACK = 15;
```

Los patrones de movimiento se denominan `GAIT` y definen la forma en que se moverá el CyberDog. (el estilo de andar, como podemos decir)

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

Así que podemos utilizar la función `setExtmonOrder()` para establecer el modo:

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
    print('Ejecutar orden de baile, resultado:' + str(succeed_state))
```

Y la función `setPattern()` para establecer la marcha:

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
    print('Cambiar la marcha al trot, resultado:' + str(succeed_state))
```

## **USANDO UN GAMEPAD PARA CONTROLAR EL CYBERDOG**

Para ello estamos utilizando la librairia `pygame`. Y estamos inicializando la librairy como tal:

```python
pygame.init()
```

Para comprobar si tenemos algunos controladores conectados:

```python
# Checking for joysticks
joystick_count = pygame.joystick.get_count()
if joystick_count == 0:
    # No joysticks!
    print("Error, No he encontrado ningún joystick.")
    exit()
else:
    # Initialize joystick #0
    mi_joystick = pygame.joystick.Joystick(0)
    mi_joystick.init()
    # Get the name from the OS for the controller/joystick.
    name = mi_joystick.get_name()
    print("Nombre del joystick: {}".format(name))
```

No hay que olvidarse de salir de `pygame` cuando se termina:

```python
pygame.quit()
```

Puedes utilizar el script proporcionado para obtener los datos del controlador. (controller_styled.py o controller_name.py)

## **USAR LA VOZ PARA CONTROLAR EL CYBERDOG**

Para ello estamos utilizando la librería `SpeechRecognition`. Y estamos inicializando la librería como tal:

```python
import speech_recognition as sr

LANGUAGES = {
    'FR': "fr-FR",
    'EN': "en-US",
    'ES': "es-ES",
    'UK': "uk-UA",
}
```

Para obtener el audio del micrófono:

```python
r = sr.Recognizer()
with sr.Microphone() as source:
    r.energy_threshold = 3000 # Se utiliza para las pruebas (300 por defecto)
    r.dynamic_energy_threshold = True
    r.adjust_for_ambient_noise(source, duration=0.515)
    print("¡Escuchando!")
    audio = r.listen(source)
```

## **AVISO**

Utilizar la aplicación móvil y un ordenador, o dos ordenadores, **al mismo tiempo** para controlar el robot no es aconsejable ya que está dando señales contradictorias al Cyberdog.

## **SOLUCIÓN DE PROBLEMAS**

Si el CyberDog no reacciona a nada, puede intentar revivirlo enchufándolo al cargador durante un segundo.

## **IDEAS**

WOL en el CyberDog y una skill de Alexa para poder llamar al robot desde cualquier lugar.
