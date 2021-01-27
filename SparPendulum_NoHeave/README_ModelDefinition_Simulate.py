# 
# Sliding-Pin uniform rigid body floater (acting as a pendulum under gravity)
# 
# Equation of motions:
#  
#  M               xdot   M L/2 \cos\theta theta_ddot =  M    *L/2 sin\theta \theta_dot**2
#  M L/2 cos\theta xdot   JO               theta_ddot = -M *g *L/2 sin\theta 
#  
#
import numpy as np
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from numpy.linalg import inv
from scipy.integrate import  solve_ivp #odeint

# --- Parameters
Mtot = 5.4e6 # [kg]     floater mass
L    = 150   # [m]      floater length
rho  = 7850  # [kg/m^3] material density 
g    = 10    # [m/s-2] acceleration of gravity

# --- Derevied parameters
D  = np.sqrt(4*Mtot/(rho*np.pi*L))
A  = np.pi*D**2
JO = Mtot * L**2/3                 # moment of inertia wrt to O (around x or y axis) [kg m^2]
JG = Mtot * L**2/12                # moment of inertia wrt to G (around x or y axis) [kg m^2]
Jz = Mtot * (D/2)**2/2             # moment of inertia           around z-axis [kg m^2]

zG = -L/2

omega = np.sqrt(Mtot * g * L/2 / JO)


print('theta= ' ,10*np.pi/180)
print('D    = ' ,D)
print('t    = ' ,D/2)
print('A    = ' ,A)
print('m(z) = ' ,rho*A)
print('JOy=JOx = ' ,JO)
print('JGy=JGx = ' ,JG)
print('Jz      = ' ,Jz)
print('m z_G = ',Mtot*zG)
print('omega = ',omega )
print('f     = ',omega/(2*np.pi) )
print('T     = ',2*np.pi/omega )







def rhs(t, q):
    q=q.flatten()
    x        = q[0]
    theta    = q[1]
    xdot     = q[2]
    thetadot = q[3]

    M=np.array([[ Mtot,    Mtot*L/2*np.cos(theta) ], [  Mtot*L/2*np.cos(theta), JO]])

    Forcing=np.zeros([2,1])
    Forcing[0] = +Mtot  *L/2*np.sin(theta) * thetadot**2
    Forcing[1] = -Mtot*g*L/2*np.sin(theta)

    Acc = inv(M).dot(Forcing)

    dq = q*0
    dq[0]=q[2]
    dq[1]=q[3]
    dq[2]=Acc[0,0]
    dq[3]=Acc[1,0]

    return dq


fps=5

time=np.linspace(0,40,600)
q0=[0,10*np.pi/180,0,0]


res = solve_ivp(fun=rhs, t_span=[time[0], time[-1]], y0=q0, t_eval=time, vectorized=True)   

x_cart=- res.y[0,:] # NOTE: sign inversion
theta = res.y[1,:]
x_end =-L*np.sin(theta)  + x_cart
y_end =-L*np.cos(theta) 

# --- Export
df= pd.DataFrame(data=np.column_stack((time,x_cart,theta)), columns=['Time_[s]','PtfmSurge_[m]','PtfmPitch_[deg]'])
df.to_csv('SparPendulum_NoHeave_NumericalSolution2DOF.csv', index=False, sep=',')

# 
# --- Plot
fig,axes = plt.subplots(2, 1, sharey=False, figsize=(6.4,5.8)) # (6.4,4.8)
fig.subplots_adjust(left=0.12, right=0.95, top=0.95, bottom=0.11, hspace=0.20, wspace=0.20)
axes[0].set_xlabel('x [m]')
axes[0].set_ylabel('y [m]')
axes[0].tick_params(direction='in')
axes[1].plot(res.t,x_end,        label='x tip')
axes[1].plot(res.t,x_cart, 'k-', label='x cart')
axes[1].plot(res.t,theta*180/np.pi       , label='theta')
axes[1].set_xlabel('time [s]')
axes[1].set_ylabel('')
axes[1].legend()
axes[1].tick_params(direction='in')
lnc1, = axes[0].plot([], [], 'ks',lw=2,ms=9)
lnc2, = axes[1].plot([], [], 'ks',lw=2)
lnt1, = axes[0].plot([], [], 'o',lw=2)
lnt2, = axes[1].plot([], [], 'bo',lw=2)
lnp,  = axes[0].plot([], [], 'k-',lw=2)

def init():
    axes[0].set_xlim(-L*1.1, L*1.1)
    axes[0].set_ylim(-L*1.1, L*0.2)
    axes[0].set_aspect('equal')
    return lnp,lnc1,lnc2,lnt1,lnt2,

def update(i):
    i=fps*int(i)
    lnp.set_data([x_cart[i],x_end[i]],[0,y_end[i]])
    lnt1.set_data([x_end[i]],[y_end[i]])
    lnc1.set_data([x_cart[i]],[0])
    lnt2.set_data([time[i]],[x_end[i] ])
    lnc2.set_data([time[i]],[x_cart[i]])
    return lnp,lnc1,lnc2,lnt1,lnt2

ani = FuncAnimation(fig, update, frames=np.arange(0,len(time)/fps), init_func=init, blit=True)
# 
# 
# 
# 
# 
# 
plt.show()
