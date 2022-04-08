%Creaci ́on subscriptor
poseSub = rossubscriber('/turtle1/pose','turtlesim/Pose'); 
%Pausa 1ms
pause(1) 
%Captura de la pose
poseCap = poseSub.LatestMessage
  