import math
import numpy as np
from qpsolvers import solve_qp

x = 2
y = 1 
theta  = 0 
xo1          = 0.9   ;  yo1          = 0.0   ; r1 = 0.5;
xo2          = -1.2  ;  yo2          = 0.25  ; r2 = 0.2;
xo3          = -0.3  ;  yo3          = 0.2   ; r3 = 0.4;
xo4          =  0.2  ;  yo4          = -0.7  ; r4 = 0.2;
xo5          =  -1   ;  yo5          = -0.5  ; r5 = 0.2;

xd          = -1.75  ; 
yd          = 0     ; 
d           = 0.06 ; 
xo          = np.array([xo1,xo2,xo3,xo4,xo5]); 
yo          = np.array([yo1,yo2,yo3,yo4,yo5]);
ro          = np.array([r1,r2,r3,r4,r5]);

z1 		= x + (d * np.cos(theta)) 						# x cooordinate of a point on robots xb axis at a distance d units away
z2 		= y + (d * np.sin(theta)) 						# y coordinate of a point on robots xb axis at a distnace d units away
kp 		= 1 											# Proportional gain
gamma 	= 1 											# Factor


A = np.zeros((len(ro)+4,2))
b = np.ones((len(ro)+8,1))

for m in range(len(ro)):
	A[m,:]     = np.array([-2*(z1-xo[m]), -2*(z2-yo[m])])
	hval       = ((z1-xo[m])**2 + (z2-yo[m])**2) - (ro[m]**2)
	b[m,:]     = gamma*hval



whval1       = ((z2-0.9449)**2) - (0.1)**2;
A[m+1,:]            = np.array([0, -2*(z2-0.9449)]);
b[m+1,:]             = gamma * (whval1);
	
whval2       = ((z1-1.9177)**2) - (0.1)**2;
A[m+2,:]            = np.array([-2*(z1-1.9177), 0]);
b[m+2,:]           = gamma * (whval2);
	
whval3       = ((z2+1.0033)**2) - (0.1)**2;
A[m+3,:]            = np.array([0, -2*(z2+1.0033)]);
b[m+3,:]           = gamma * (whval3);
	
whval4       = ((z1+1.9431)**2) - (0.1)**2;
A[m+4,:]            = np.array([-2*(z1+1.9431), 0]);
b[m+4,:]           = gamma * (whval4);



u1cap 	= -kp * (z1 - xd) 								# Proportional controller for z1 coordinate to make z1 stabilize to xd, should be a scalar, this is control without regarding obstacles
u2cap 	= -kp * (z2 - yd) 								# Proportional controller for z2 coordinate to make z2 stabilize to yd, should be a scalar, this is control without regarding obstacles
P 		= np.array([[2.0, 0.0],[0.0, 2.0]]) 			# Identity matrix of size 2 by 2 because we have two controls
q       = np.array([-2.0*u1cap,-2.0*u2cap])				# -2*ucap
r1      = np.array([[1.0,0.0],[0.0,1.0],[-1.0,0.0],[0.0,-1.0]])

G       = np.vstack([A,r1])								# A is for collision avoidance constraint, r1 is for explicit constraint on bounds


R  		= np.array([[np.cos(theta), -np.sin(theta)],[np.sin(theta), np.cos(theta)]]) # rotation matrix of size 2 by 2
D  		= np.array([[1.0, 0.0], [0.0, d]]) 				# Diagonal matrix of size 2 by 2
J  		= np.matmul(R,D)
M       = np.linalg.inv(J)

ustar 	= solve_qp(P,q,G,b[0:m+9,0]) 							# Quadratic programming solver
urobot 	= np.matmul(M,ustar)

V = urobot[0]
W = urobot[1]

print(urobot)