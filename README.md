# Lab1_Rob_IntROS
Laboratorio 1: Introducción ROS
## Integrantes:
- Fabian Steven Galindo Peña
- Christian Cuestas
## Metodologia:
Para este laboratorio se utilizo una instalacion nativa de Ubuntu version 20.04 LTS, se instalo ROS Noetic, se utilizo MATLAB
R2021b, ROS toolbox, Python y Visual Code. 
### Conexión de ROS con Matlab
Se lanzan 2 terminales. En la primera terminal se escribe el comando:
```matlab
roscore
```
en la segunda se escribe:
```matlab
rosrun turtlesim turtlesim_node
```
#### Creación de publisher
Se lanza la instancia de Matlab para Linux y se corre el siguiente script
```matlab
%%
rosinit; %Conexi ́on con nodo maestro
%%
velPub = rospublisher('/turtle1/cmd_vel','geometry_msgs/Twist'); %Creaci ́on publicador
velMsg = rosmessage(velPub); %Creaci ́on de mensaje
%%
velMsg.Linear.X = 1; %Valor del mensaje
send(velPub,velMsg); %Envio
pause(1)  
```
Donde rosinit va a inicar el nodo ROS global con un nombre predeterminado e intenta conectarse a un nodo maestro que se ejecuta en localhost. 
rospublisher() permite crear un objeto publicador el cual publica un tipo de mensaje especifico en un topic dado. En este caso:
```matlab
velPub = rospublisher('/turtle1/cmd_vel','geometry_msgs/Twist');
```
Se crea un publicador para el topico "cmd_vel" con el tipo de mensaje "geometry_msgs/Twist". geometric_msgs proporciona mensajes para primitivas geométricas comunes, como puntos, vectores y poses. Estas primitivas están diseñadas para proporcionar un tipo de datos común y facilitar la interoperabilidad en todo el sistema. 

Luego se crea el mensaje con:
```matlab
velMsg = rosmessage(velPub);
```
Donde rosmessage(pub) va a crean un objeto de tipo mensanje ROS vacio,en este caso el argumento es un publicador, entonces el mensaje va a ser del mismo tipo que el topic publicado por pub. 
Ahora se le da el valor al mensaje en :
```matlab
velMsg.Linear.X = 1;
```
Send() publica el mensaje vel Msg sobre el topico especificado en velPub.
```matlab
send(velPub,velMsg);
```


#### Creación de subscriber
Se crea un nuevo script en matlab donde se suscribe al topico de pose de la simulacion de turtle1.
```matlab
poseSub = rossubscriber('/turtle1/pose','turtlesim/Pose'); 
pause(1) 
poseCap = poseSub.LatestMessage
```
`rossubscriber()` permite crear un suscriptor ROS para recibir mensajes en la red ROS. El objeto creado recibe el nombre del topico y el tipo de mensaje.
pause(1)se pausa para recibir el mensaje. Con`poseCap = poseSub.LatestMessage` se captura el ultimo mensaje del topico pose.
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
Primero se consulta la lista de sercios disponibles con: `rosservice('list')`. Se crea un cliente que va a utilizar el servicio. Se comprueba que el servidor del servicio este disponible y se espera que el cliente se conecte al servidor.Con `poseMsg = rosmessage(poseClient)` se crea el mensaje que va a recibir el cliente. Luego se definen los valores de la pose (X,Y,theta). Y se envia el mensaje al servicio con `call(poseClient,poseMsg,"Timeout",3)`.
Para cambiar LienarVelocity y AngularVelocity se utiliza un publisher `/turtle1/cmd_vel`


