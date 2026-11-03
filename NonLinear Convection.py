import numpy as np
from functions import animate_evolution

XSTART = 0 
XSTOP = 2
N_X = 41
D_X = (XSTOP-XSTART)/(N_X-1)


D_T = 0.025
N_T = 25

xspace = np.linspace(XSTART, XSTOP, N_X)
tspace = np.linspace(0, D_T*N_T, N_T)

u = np.ones(len(xspace))
u[(xspace >= 0.5) & (xspace <= 1.0)] = 2.0

print(u)
def nonlinear_convection(u):
    u_prev = u.copy()
    states = {}
    for t in tspace:
        states[t] = u.copy()
        u_prev = u.copy()

        for x in range(len(u)):
            if x!=0:
                u[x] = u_prev[x] - u_prev[x]*(D_T/D_X)*(u_prev[x]-u_prev[x-1])
    return u, states
            
final_u, states = nonlinear_convection(u)

animate_evolution(xspace,tspace,states)