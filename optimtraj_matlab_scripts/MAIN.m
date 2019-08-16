clc; clear; close all

global finishPoint

xBnd = [-76.8 * 2.54/100, 75.5 * 2.54/100];
yBnd = [-39.5 * 2.54/100, 37.0 * 2.54/100];

startPoint  = [1.3599; 0.2528; 104.3 * pi / 180];        %Start here
finishPoint = [-0.4904; -0.63135; 1.7 * pi];       %Finish here
uMax        = [2;2];          %6 is for max velocity in m/s, 5 is for max angular velocity in rad/2

%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~%
%                      Set up function handles                            %
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~%

problem.func.dynamics = @(t,x,u)( dynamics(x,u) );
problem.func.pathObj  = @(t,x,u)( objective(x,u) );

%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~%
%                 Set up bounds on state and control                      %
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~%
Time = 20;

problem.bounds.initialTime.low  = 0;
problem.bounds.initialTime.upp  = 0;
problem.bounds.finalTime.low    = Time; 
problem.bounds.finalTime.upp    = Time;
problem.bounds.state.low        = [xBnd(1); yBnd(1); -2*pi];
problem.bounds.state.upp        = [xBnd(2); yBnd(2);  2*pi];
problem.bounds.initialState.low = [startPoint];
problem.bounds.initialState.upp = [startPoint];
problem.bounds.finalState.low   = [finishPoint];
problem.bounds.finalState.upp   = [finishPoint];
problem.bounds.control.low      = -uMax;
problem.bounds.control.upp      = uMax;


%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~%
%                 Initialize trajectory with guess                        %
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~%
% Car travels at a speed of one, and drives in a straight line from start
% to finish point.

problem.guess.time    = [0,60];   % time = distance/speed
problem.guess.state   = [startPoint, finishPoint];
problem.guess.control = [0,0 ; 0,0];  

%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~%
%                      Options for Transcription                          %
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~%

problem.options.nlpOpt = optimset(...
    'display','iter',...
    'MaxFunEval',1e5,...
    'tolFun',1e-6);

% problem.options.method = 'hermiteSimpson';
% problem.options.hermiteSimpson.nSegment = 40;

% problem.options.method = 'gpops';

problem.options.method = 'trapezoid';
problem.options.trapezoid.nGrid = 60;

%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~%
%                            Solve!                                       %
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~%
soln = optimTraj(problem);

%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~%
%                        Display the solution                             %
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~%

figure(1); clf; hold on;
t  = linspace(soln.grid.time(1), soln.grid.time(end), Time * 100);
z  = soln.interp.state(t);
x  = z(1,:);
y  = z(2,:);
th = z(3,:);
u  = soln.interp.control(t);

tGrid  = soln.grid.time;
xGrid  = soln.grid.state(1,:);
yGrid  = soln.grid.state(2,:);
thGrid = soln.grid.state(3,:);
uGrid  = soln.grid.control;

x_from_trajopt = xGrid; 
y_from_trajopt = yGrid;


x_check     = 0*xGrid;  x_check(1)   = xGrid(1);
y_check     = 0*yGrid;  y_check(1)   = yGrid(1);
theta_check = 0*thGrid; theta_check(1)  = thGrid(1);
z           = [x_check(1);y_check(1);theta_check(1)];

for i  = 1:length(tGrid)-1
    zdot             = dynamics(z,uGrid(:,i));
    dt               = tGrid(i+1)-tGrid(i);
    z                = z + (dt*zdot) ;
    x_check(i+1)     = z(1);
    y_check(i+1)     = z(2);
    theta_check(i+1) = z(3);
end

V = u(1,:) * 1000;
W = u(2,:);

fid1 = fopen('/home/michael/catkin_ws/src/Advance-Agent-Swarm-Platform-ROS-Package-master/khepera_communicator/scripts/V.txt','w');
fid2 = fopen('/home/michael/catkin_ws/src/Advance-Agent-Swarm-Platform-ROS-Package-master/khepera_communicator/scripts/W.txt','w');

fprintf(fid1, '%f\n',V);
fprintf(fid2, '%f\n',W);


% Plot the entire trajectory
plot(x_from_trajopt,y_from_trajopt,'b-','LineWidth',1);
hold on
plot(x_check,y_check,'k-','LineWidth',1);
plot(startPoint(1),startPoint(2),'*g');
plot(finishPoint(1),finishPoint(2),'*r');
plot(x_check(end),y_check(end),'*k','LineWidth',2);

ylabel('y coordinate');
xlabel('x coordinate');
grid on
legend('Predicted Path','Obtained Path','Start','Predicted End','Obtained End');
axis equal


% Plot the state and control:
figure(2); 
subplot(2,2,1); hold on;
plot(t,x);
plot(tGrid,xGrid,'ko','MarkerSize',5,'LineWidth',3);
ylabel('y coordinate');
grid on 

subplot(2,2,3); hold on;
plot(t,y);
plot(tGrid,yGrid,'ko','MarkerSize',5,'LineWidth',3);
ylabel('y coordinate');
grid on

subplot(2,2,2); hold on;
plot(t,th);
plot(tGrid,thGrid,'ko','MarkerSize',5,'LineWidth',3);
ylabel('theta');
grid on

subplot(2,2,4); hold on;
plot(tGrid,uGrid(1,:),'-b','linewidth',1.5);
hold on
plot(tGrid,uGrid(2,:),'-r','linewidth',1.5);
grid on
legend('v','w');
ylabel('Controls');