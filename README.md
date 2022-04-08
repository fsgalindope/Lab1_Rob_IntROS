# Lab1_Rob_IntROS
Laboratorio 1: Introducción ROS
## Integrantes:
- Fabian Steven Galindo Peña
- Christian Camilo Cuestas Ibáñez
## Metodología:
Para este laboratorio se utilizo una instalación nativa de Ubuntu versión 20.04 LTS, se instalo ROS Noetic, se utilizo MATLAB
R2021b, ROS toolbox, Python y Visual Code. 
### Conexión de ROS con Matlab
Se lanzan 2 terminales. En la primera terminal se escribe el comando:
```
roscore
```
en la segunda se escribe:
```
rosrun turtlesim turtlesim_node
```
#### Creación de publisher
Se lanza la instancia de Matlab para Linux y se corre el siguiente script
```matlab
%%
rosinit; %Conexión con nodo maestro
%%
velPub = rospublisher('/turtle1/cmd_vel','geometry_msgs/Twist'); %Creación publicador
velMsg = rosmessage(velPub); %Creación de mensaje
%%
velMsg.Linear.X = 1; %Valor del mensaje
send(velPub,velMsg); %Envio
pause(1)  
```
Donde `rosinit` va a iniciar el nodo ROS global con un nombre predeterminado e intenta conectarse a un nodo maestro que se ejecuta en localhost. 
rospublisher() permite crear un objeto publicador el cual publica un tipo de mensaje especifico en un topic dado. En este caso:
```matlab
velPub = rospublisher('/turtle1/cmd_vel','geometry_msgs/Twist');
```
Se crea un publicador para el tópico "cmd_vel" con el tipo de mensaje "geometry_msgs/Twist". geometric_msgs proporciona mensajes para primitivas geométricas comunes, como puntos, vectores y poses. Estas primitivas están diseñadas para proporcionar un tipo de datos común y facilitar la interoperabilidad en todo el sistema. 

Luego se crea el mensaje con:
```matlab
velMsg = rosmessage(velPub);
```
Donde rosmessage(pub) va a crean un objeto de tipo mensaje ROS vació,en este caso el argumento es un publicador, entonces el mensaje va a ser del mismo tipo que el tópico publicado por pub. 
Ahora se le da el valor al mensaje en :
```matlab
velMsg.Linear.X = 1;
```
Send() publica el mensaje vel Msg sobre el tópico especificado en velPub.
```matlab
send(velPub,velMsg);
```

#### Creación de subscriber
Se crea un nuevo script en matlab donde se suscribe al tópico de pose de la simulación de turtle1.
```matlab
poseSub = rossubscriber('/turtle1/pose','turtlesim/Pose'); 
pause(1) 
poseCap = poseSub.LatestMessage
```
`rossubscriber()` permite crear un suscriptor ROS para recibir mensajes en la red ROS. El objeto creado recibe el nombre del tópico y el tipo de mensaje.
pause(1)se pausa para recibir el mensaje. Con`poseCap = poseSub.LatestMessage` se captura el ultimo mensaje del tópico pose.
#### Creación de un services
Se crea un scrip que permite enviar todos los valores asociados a la pose de turtle1.
```matlab
poseSer = rosservice('list');%%Consultamos la lista de servicios
poseClient= rossvcclient("/turtle1/teleport_absolute");%%Creamos el cliente
%%Compruebe si el servidor de servicio está disponible. Si es así, espere a
% que el cliente del servicio se conecte al servidor.
if(isServerAvailable(poseClient))
    [connectionStatus,connectionStatustext] = waitForServer(poseClient)
end
%se crea el mensaje
poseMsg = rosmessage(poseClient);
%se definen los valores X,Y y theta 
poseMsg.Y=5;
poseMsg.X=5;
poseMsg.Theta=pi;
%Especifica una solicitud de mensaje de servicio poseMsg, y lo envia al
%servicio 
call(poseClient,poseMsg,"Timeout",3)
%Pausa 1ms
pause(1)
%Cambio de la velocidad lineal y angular
velPub = rospublisher('/turtle1/cmd_vel','geometry_msgs/Twist'); %Creacion publicador
velMsg = rosmessage(velPub);
velMsg.Angular.Z= 1;%Valor del mensaje
velMsg.Linear.X=4;
send(velPub,velMsg); %Envio
%Pausa 1ms
pause(1) 
%%finalizacion nodo maestro
rosshutdown;
```
Primero se consulta la lista de servicios disponibles con: `rosservice('list')`. Se crea un cliente que va a utilizar el servicio. Se comprueba que el servidor del servicio este disponible y se espera que el cliente se conecte al servidor.Con `poseMsg = rosmessage(poseClient)` se crea el mensaje que va a recibir el cliente. Luego se definen los valores de la pose (X,Y,theta). Y se enviá el mensaje al servicio con `call(poseClient,poseMsg,"Timeout",3)`.
Para cambiar LinearVelocity y AngularVelocity se utiliza un publisher `/turtle1/cmd_vel`
Por ultimo se utiliza `rosshutdown` se cierra el nodo global y, si se está ejecutando, el maestro ROS. Cuando termine de trabajar con la red ROS, se usa rosshutdown para cerrar las entidades ROS globales creadas por rosinit.
### Utilizando Python

#### Creación del script

Se creó un script de python llamado `myTeleopKey.py` con el cual se puede controlar la posición y orientación de la tortuga:

- Tecla W: Hacia adelante
- Tecla S: Hacia atras
- Tecla A: Giro a la derecha
- Tecla D: Giro a la izquierda
- Tecla R: Salto al centro
- Tecla espacio: Giro de 180 grados

Se usaron los tópicos `turtle1/cmd_vel`, `turtle1/teleport_absolute`, `turtle1/teleport_relative`.

Las funciones que comprende el script son `getkey()`, `toCenter()`, `giro180()` y `pubVel()`. Estas son usadas en el main para lograr el objetivo de la siguiente manera:

```python
if __name__ == "__main__":
    while 1:
        letter = getkey()
        if(letter ==b'w' or letter == b'W'):
            print('Adelante')
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
```

Se modificó también el archivo `CMakeLists.txt` para incluir en el script de python. Posteriormente, se hizo `catkin build` al workspace para que se compilen los cambios.

## Resultados:
### Conexión de ROS con Matlab
Tras correr el primer script `conexionMatlab.m` Se obtiene lo que se ve en la imagen1 ,donde se puede ver que la tortuga realiza el movimiento en X gracias a que después de la conexion en matlab se cambia el valor de la velocidad lineal en X.
![Fig.1 image1.v](https://github.com/fsgalindope/Lab1_Rob_IntROS/blob/main/recursos/image1.png)
En la siguiente imagen se ve como se obtiene información del tópico `turtle1/pose` después de hacer la subscripcion obteniendo información de la pose (X,Y,Theta,AngularVelocity, LinearVelocity). 
![Fig.2 image2.v](https://github.com/fsgalindope/Lab1_Rob_IntROS/blob/main/recursos/image2.png)
En la siguiente imagen se puede observar la posición de la tortuga después de correr el tercer script. Donde primero se cambio la posición (X,Y,Theta) y después se cambio las velocidades(AngularVelocity, LinearVelocity). 
![Fig.3 image3.v](https://github.com/fsgalindope/Lab1_Rob_IntROS/blob/main/recursos/image3.png)
### Utilizando Python

Al hacer la prueba del script `myTeleopKey.py` se logró el resultado como lo muestra la siguiente imagen.

![Fig.4 resultPython.v](https://github.com/fsgalindope/Lab1_Rob_IntROS/blob/main/recursos/resultPython.png)

## Análisis
### Conexión de ROS con Matlab
Se pudo crear desde matlab el publisher, el subscriber, y utilizar los services a partir de la creación del cliente, ademas de la conexión entre cliente y servidor.
Para realizar algunas funciones se tuvo que usar `pause()` esto para poder capturar mensajes y para poder hacer la conexión entre cliente y servidor.

### Utilizando Python

Mediante un script en Python es posible comunicarse con los nodos de ROS y así comunicarse desde el teclado para controlar la tortuga. Se puede ecalibar bien el tiempo que la tortuga avanza o gira así como su cantidad. Fue muy importante entender cómo leer comandos desde el teclado.

## Conclusiones
- Se puede observar que se logro una conexión de matlab con ROS sin mucha complejidad, gracias a las herramientas que otorga el ROS toolbox. 
- Está fácil integración entre Matlab y ROS facilitaran proyectos más complejos con el uso de las herramientas matemáticas y de simulación que aporta matlab.
- Son bastante directos los cambios para hacer control a través de scripts de python.
- Fue muy importante entender cómo leer comandos desde el teclado.
