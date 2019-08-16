clear all
close all
clc
rosinit
sub150 = rossubscriber('/vicon/k150/k150');



iptsetpref('ImshowBorder','tight');
set(0,'DefaultFigureMenu','none');
format compact;
figure('units','normalized','outerposition',[0 0 1 1],'color','white')
x0 = -76.5*2.54*0.01 ;% -20 
y0 = -39.5*2.54*0.01 ;% -10;
width = 152.0*2.54*0.01 ;% 40 
height = 76.7*2.54*0.01 ; % 20 

coor = receive(sub150,10);

xi = coor.Transform.Translation.X;
yi = coor.Transform.Translation.Y; 

initial_center =[xi yi];
goal_center    =[randrange(x0,x0+width) randrange(y0,y0+height)];
radius  =  [0.07];
viscircles(initial_center,radius,'Color','g')
hold on
viscircles(goal_center,radius,'Color','r')






rectangle('Position',[x0 y0 width height],'linewidth',5)
hold on

quiver(0,0,.5,0,'linewidth',2,'color','b','MaxHeadSize',0.8)
hold on
quiver(0,0,0,.5,'linewidth',2,'color','b','MaxHeadSize',0.8)



grid on
ax = gca;
outerpos = ax.OuterPosition;
ti = ax.TightInset; 
left = outerpos(1) + ti(1);
bottom = outerpos(2) + ti(2);
ax_width = outerpos(3) - ti(1) - ti(3);
ax_height = outerpos(4) - ti(2) - ti(4);
ax.Position = [left-0.02 bottom ax_width+0.02 ax_height];
hold on
plot(0,0,'Ob','linewidth',6,'color','b')
axis equal
plot(x0,y0,'*b','linewidth',5)
plot(x0,y0+height,'*g','linewidth',5)
plot(x0+width,y0,'*r','linewidth',5)
plot(x0+width,y0+height,'*k','linewidth',5)
s1 = num2str(initial_center(1));
s2 = ' ,  ';
s3 = num2str(initial_center(2));
s4 = strcat(s1,s2,s3);

s1 = num2str(goal_center(1));
s2 = ' ,  ';
s3 = num2str(goal_center(2));
j4 = strcat(s1,s2,s3);
text(initial_center(1),initial_center(2)+0.15,s4)
text(goal_center(1),goal_center(2)+0.15,j4)

s1 = num2str(initial_center(1)*100/2.54);
s2 = ' , ';
s3 = num2str(initial_center(2)*100/2.54);
s4 = strcat(s1,s2,s3);

s1 = num2str(goal_center(1)*100/2.54);
s2 = ' , ';
s3 = num2str(goal_center(2)*100/2.54);
j4 = strcat(s1,s2,s3);
text(initial_center(1),initial_center(2)-.15,s4)
text(goal_center(1),goal_center(2)-.15,j4)



plot(initial_center(1),initial_center(2),'*g','linewidth',.1)
plot(goal_center(1),goal_center(2),'*r','linewidth',.1)

cnt = 0;
prevX = 0;
prevY = 0;


H = uicontrol('Style', 'PushButton', ...
                    'String', 'Break', ...
                    'Callback', 'delete(gcbf)','Position',[100, 100, 80 ,40]);
coor = receive(sub150,10);

xc = coor.Transform.Translation.X;
yc = coor.Transform.Translation.Y;                
 
r = 0.06;
th = 0:pi/50:2*pi;
X = r * cos(th) + xc;
Y = r * sin(th) + yc;
h = plot(X, Y, 'Color','b', 'Linewidth', 4);
while (ishandle(H))
    coor = receive(sub150,10);

    xc = coor.Transform.Translation.X;
    yc = coor.Transform.Translation.Y;
    x = coor.Transform.Translation.X;
    y = coor.Transform.Translation.Y;
    if cnt == 0
        plot(x,y,'k.', 'MarkerSize', 5);
        prevX = x;
        prevY = y;
        cnt = 1;
    else
        plot(x,y,'k.', 'MarkerSize', 30);
        plot([x prevX], [y prevY],'k', 'Linewidth', 5);
        prevX = x;
        prevY = y;
    
    end
    h.XData = r * cos(th) + xc;   %Adding a constant in the x data
    h.YData = r * sin(th) + yc;
end
rosshutdown;

function h = randrange(a,b)
 h=a + (b-a).*rand;
end 

