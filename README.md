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
~~~
roscore
~~~
en la segunda se escribe:
~~~
rosrun turtlesim turtlesim_node
~~~
#### Creación de publisher
Se lanza la instancia de Matlab para Linux y se corre el siguiente script
~~~
%%
rosinit; %Conexi ́on con nodo maestro
%%
velPub = rospublisher('/turtle1/cmd_vel','geometry_msgs/Twist'); %Creaci ́on publicador
velMsg = rosmessage(velPub); %Creaci ́on de mensaje
%%
velMsg.Linear.X = 1; %Valor del mensaje
send(velPub,velMsg); %Envio
pause(1)  
~~~
Donde rosinit va a inicar el nodo ROS global con un nombre predeterminado e intenta conectarse a un nodo maestro que se ejecuta en localhost. 
rospublisher() permite crear un objeto publicador el cual publica un tipo de mensaje especifico en un topic dado. En este caso:
~~~
velPub = rospublisher('/turtle1/cmd_vel','geometry_msgs/Twist');
~~~
Se crea un publicador para el topico "cmd_vel" con el tipo de mensaje "geometry_msgs/Twist". geometric_msgs proporciona mensajes para primitivas geométricas comunes, como puntos, vectores y poses. Estas primitivas están diseñadas para proporcionar un tipo de datos común y facilitar la interoperabilidad en todo el sistema. 

Luego se crea el mensaje con:
~~~
velMsg = rosmessage(velPub);
~~~
Donde rosmessage(pub) va a crean un objeto de tipo mensanje ROS vacio,en este caso el argumento es un publicador, entonces el mensaje va a ser del mismo tipo que el topic publicado por pub. 
Ahora se le da el valor al mensaje en :
~~~
velMsg.Linear.X = 1;
~~~
Send() publica el mensaje vel Msg sobre el topico especificado en velPub.
~~~
send(velPub,velMsg);
~~~


#### Creación de subscriber
Se crea un nuevo script en matlab donde se suscribe al topico de pose de la simulacion de turtle1.
~~~
CODIGO
~~~
`rossubscriber()` permite crear un suscriptor ROS para recibir mensajes en la red ROS. El objeto creado recibe el nombre del topico y el tipo de mensaje.
pause(1)se pausa para recibir el mensaje.

