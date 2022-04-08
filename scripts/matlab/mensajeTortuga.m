%%
rosinit % Conexión con nodo maestro
%%
% Se crea el publisher
rosPubVel =  rospublisher('/turtle1/cmd_vel','geometry_msgs/Twist');
% Se crea el mensaje
rosMsgVel = rosmessage(rosPubVel);
%%
% Valor del mensaje
rosMsgVel.Linear.X = 5;
%rosMsgVel.Angular.Z = 1;
% Se envía el mensaje
send(rosPubVel,rosMsgVel)
pause(1)
%%
%rosshutdown