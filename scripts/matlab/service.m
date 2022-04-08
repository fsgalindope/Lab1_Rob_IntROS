
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



