%%finalizacion nodo maestro
rosshutdown;
rosinit; %Conexion con nodo maestro
%%
velPub = rospublisher('/turtle1/cmd_vel','geometry_msgs/Twist'); %Creacion publicador
velMsg = rosmessage(velPub); %Creacion de mensaje
%%
velMsg.Linear.Y= 1; %Valor del mensaje
send(velPub,velMsg); %Envio
%Pausa 1ms
pause(1)    