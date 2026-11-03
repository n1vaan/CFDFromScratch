import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

XSTART = 0 
XSTOP = 2
N_X = 41
D_X = (XSTOP-XSTART)/(N_X-1)

C = 1.0

D_T = 0.025
N_T = 25

xspace = np.linspace(XSTART, XSTOP, N_X)
tspace = np.linspace(0, D_T*N_T, N_T)

u = np.ones(len(xspace))
u[(xspace >= 0.5) & (xspace <= 1.0)] = 2.0

print(u)
def advection(u):
    u_prev = u.copy()
    states = {}
    for t in tspace:
        states[t] = u.copy()
        u_prev = u.copy()

        for x in range(len(u)):
            if x!=0:
                u[x] = u_prev[x] - C*(D_T/D_X)*(u_prev[x]-u_prev[x-1])
    return u, states
            
final_u, states = advection(u)

fig, ax = plt.subplots(figsize=(8, 5))

ax.set_xlim(XSTART, XSTOP)
ax.set_ylim(0.5, 2.5)
ax.set_xlabel('x')
ax.set_ylabel('u')
ax.grid(True)

line, = ax.plot([], [], 'b-', lw=2, label='1D Advection')
time_text = ax.text(0.05, 0.90, '', transform=ax.transAxes)
ax.legend(loc='upper right')

def init():
    line.set_data([], [])
    time_text.set_text('')
    return line, time_text

def update(frame):
    t = tspace[frame]
    current_u = states[t]
    
    line.set_data(xspace, current_u)
    time_text.set_text(f'Time: {t:.3f} s (Step {frame}/{N_T-1})')
    return line, time_text

anim = FuncAnimation(
    fig, 
    update, 
    frames=len(tspace), 
    init_func=init, 
    interval=100,  
    blit=True
)

plt.show()