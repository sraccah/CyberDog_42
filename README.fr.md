# Protocole CyberDog utilisant GRPC et Python

## **Installation**

Tout d'abord, vous devez installer le module `grpc` :

```bash
sudo pip3 install grpcio
sudo pip3 install grpcio-tools
```

Depuis le [Dépôt du protocole Xiaomi CyberDog](https://partner-gitlab.mioffice.cn/cyberdog/athena_cyberdog/-/tree/devel/athena_common/athena_grpc/protos), téléchargez le fichier proto `cyberdog_app.proto` et utilisez la commande suivante pour générer le module python :

```bash
python3 -m grpc_tools.protoc --python_out=. --grpc_python_out=. -I. *.proto
```

Assurez-vous que les fichiers générés sont nommés `cyberdog_app_pb2.py` et `cyberdog_app_pb2_grpc.py` et que les modules sont dans le même répertoire.

## **En option**

Vous pouvez également installer le module python keyboard pour contrôler facilement le clavier :

```bash
sudo pip3 install keyboard
sudo pip3 install pygame
```

Un fichier d'exigences est disponible, à faire simplement :

```bash
pip3 install -r requirements.txt
```

## **Scripting time**

Ensuite, vous pouvez commencer le script pour vous connecter au CyberDog et vérifier si la connexion GRPC est ouverte et fonctionne :

```python
from os import system
# Com protocol
import grpc
# CyberDog Library
import cyberdog_app_pb2
import cyberdog_app_pb2_grpc

# Ouvrir GRPC channel
with grpc.insecure_channel(str(CYBERDOG_IP) + ':50051') as channel:
    print("Wait connect")
    try:
        grpc.channel_ready_future(channel).result(timeout=10)
    except grpc.FutureTimeoutError:
        print("Connexion error, Timeout")
        return
    # Avoir le stud depuis le channel
    stub = cyberdog_app_pb2_grpc.CyberdogAppStub(channel)
```

Ensuite, vous pouvez utiliser la fonction `setMode()` du `stub` pour envoyer une commande au CyberDog :

```python
# MANUAL MODE => Debout
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
    print('Exécuter le mode debout appelé MANUEL, résultat:' + str(succeed_state))
```

Même chose pour le retour à l'état de base :

```python
# DEFAULT MODE => Couché
if (succeed_state == False): # en cas d'échec d'une commande précédente
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
    print('Exécuter le mode DEFAUT, résultat:' + str(succeed_state))
```

A partir de maintenant, vous pouvez ajouter toutes sortes de fonctions et d'interactions avec le CyberDog, grâce aux bibliothèques disponibles.

Par exemple, le module clavier peut être utilisé pour contrôler le robot :

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

Mais d'abord, vous devez comprendre un peu comment fonctionne le CyberDog pour pouvoir le déplacer ou interagir avec ses capteurs.

Nous utilisons la structure `Vector3` pour représenter le mouvement.

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

Et cela nous permet de préparer quelques paramètres à envoyer au CyberDog :

```python
speed_lv = 1 # De 0.1 à 1.6
linear = Vector3(0, 0, 0)
angular = Vector3(0, 0, 0)
```

Pour envoyer les données au CyberDog, vous utiliserez le stub pour accéder à la fonction `sendAppDecision()` :

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

Disons que vous créez une fonction pour envoyer les données nommée `SendData`, il vous suffit de créer d'autres fonctions pour mettre à jour les paramètres que vous voulez envoyer au CyberDog :

```python
def GoForward(Event):
    linear.x = 0.1 * speed_lv
    linear.y = 0
    angular.z = 0
    SendData()
```

Veillez à toujours disposer d'une fonction `stop` pour arrêter le robot :

```python
def Stop(Event):
    linear.x = 0
    linear.y = 0
    angular.z = 0
    SendData()
```

Retournez à la partie clavier de ce document pour voir comment nous pouvons utiliser ces fonctions et le clavier pour contrôler le robot.

Nous avons vu la fonction `setMode()` mais il y a beaucoup de possibilités, par exemple la fonction `setExtmonOrder()` pour utiliser une action prédéfinie dans la liste ci-dessous :

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

Les modes définissent la position debout du CyberDog et sont :

```python
DEFAULT = 0; # mode par défaut vu précédemment (couché)
LOCK = 1;
CONFIG = 2;
MANUAL = 3; # mode manuel vu précédemment (debout)
SEMI = 13;
EXPLOR = 14;
TRACK = 15;
```

Les motifs de déplacement sont appelés `GAIT` et définissent la façon dont le CyberDog se déplacera. (le style de marche comme on peut dire)

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

Nous pouvons donc utiliser la fonction `setExtmonOrder()` pour définir le mode :

```python
# Code précédent pour se connecter et se lever
# ...
# Exécuter l'ordre de danse
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
    print('Exécution de l\'ordre de danse, résultat :' + str(succeed_state))
```

Et la fonction `setPattern()` pour définir la démarche :

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
    print('Changez l\'allure en trot, résultat :' + str(succeed_state))
```

## **UTILISER UN GAMEPAD POUR CONTRÔLER LE CYBERDOG**

Pour ce faire, nous utilisons la librairie `pygame`. Et nous initialisons la librairie comme telle :

```python
pygame.init()
```

Pour vérifier si nous avons des contrôleurs branchés :

```python
# Vérification des joysticks
joystick_count = pygame.joystick.get_count()
if joystick_count == 0:
    # Pas de joysticks !
    print("Erreur, je n'ai pas trouvé de joystick.")
    exit()
else:
    # Initialiser le joystick #0
    mi_joystick = pygame.joystick.Joystick(0)
    mi_joystick.init()
    # Obtenez le nom du système d'exploitation pour le contrôleur/joystick.
    name = mi_joystick.get_name()
    print("Nom du joystick: {}".format(name))
```

N'oubliez pas de quitter `pygame` quand vous avez fini :

```python
pygame.quit()
```

Vous pouvez utiliser le script fourni pour obtenir les données du contrôleur. (controller_styled.py ou controller_name.py)

## **UTILISER VOTRE VOIX POUR CONTRÔLER LE CYBERDOG**

Pour ce faire, nous utilisons la librairie `SpeechRecognition`. Et nous initialisons la librairie comme telle :

```python
import speech_recognition as sr

language_es = "es-ES"
language_us = "en-US"
```

Pour obtenir l'audio du microphone :

```python
r = sr.Recognizer()
with sr.Microphone() as source:
    r.energy_threshold = 3000 # Utilisé pour les tests (300 par défaut)
    r.dynamic_energy_threshold = True
    r.adjust_for_ambient_noise(source, duration=0.515)
    print("Listening!")
    audio = r.listen(source)
```

## **AVIS**

L'utilisation de l'application mobile et d'un ordinateur, ou de deux ordinateurs, **en même temps** pour contrôler le robot n'est pas conseillée car elle donne des signaux contradictoires au Cyberdog.

## **DÉPANNAGE**

Si le CyberDog ne réagit à rien, vous pouvez essayer de le relancer en le branchant au chargeur pendant une seconde.

## **IDEES**

WOL sur le CyberDog et une compétence Alexa pour pouvoir appeler le robot depuis n'importe où.
