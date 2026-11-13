# CFD From Scratch

Building an understanding of computational fluid dynamics by implementing numerical solvers from the governing equations. This repository starts with one-dimensional convection and diffusion, using Python, finite differences, and animated plots to connect the mathematics to the behavior of a field over time.

This is an ongoing learning project. The current examples are small, explicit solvers intended for experimentation and understanding.

## Implemented examples

| Example | Governing equation | What to look for |
| --- | --- | --- |
| Linear convection | $\partial_t u + c\,\partial_x u = 0$ | A pulse travels at the constant speed $c$. |
| Nonlinear convection | $\partial_t u + u\,\partial_x u = 0$ | Higher values travel faster, causing the pulse to deform and its leading edge to steepen. |
| Diffusion | $\partial_t u = \nu\,\partial_{xx}u$ | Gradients spread out and the pulse becomes smoother. |

Each example starts with a field of $u=1$ on $0\leq x\leq2$, raised to $u=2$ between approximately $x=0.5$ and $x=1.0$.

## Getting started

Use Python 3 with NumPy and Matplotlib. JupyterLab is needed to run the diffusion notebook.

```bash
git clone https://github.com/n1vaan/CFDFromScratch.git
cd CFDFromScratch
python3 -m venv .venv
source .venv/bin/activate
python -m pip install numpy matplotlib jupyterlab
```

On Windows, activate the environment with `.venv\Scripts\activate` instead.

Run either convection example from the repository directory:

```bash
python "Linear Convection.py"
python "NonLinear Convection.py"
```

Each script opens a Matplotlib animation. Close the plot window to finish the script.

For diffusion, launch JupyterLab, open `Diffusion.ipynb`, and run the cells in order:

```bash
jupyter lab
```

The animation helper embeds playback controls inside a notebook and opens a plot window when called from a script.

## Numerical methods

Here, $u_i^n$ denotes the field at spatial point $i$ and time step $n$. Every solver computes a new state from a copy of the previous state.

### Linear convection

Forward Euler in time and a backward difference in space give

$$
u_i^{n+1}=u_i^n-c\frac{\Delta t}{\Delta x}\left(u_i^n-u_{i-1}^n\right).
$$

The backward spatial difference is an upwind choice for positive $c$. The first grid value stays fixed; the remaining points are updated, including the right endpoint.

### Nonlinear convection

The same discretization uses the local field value as the transport speed:

$$
u_i^{n+1}=u_i^n-u_i^n\frac{\Delta t}{\Delta x}\left(u_i^n-u_{i-1}^n\right).
$$

This implementation assumes positive transport speeds and keeps the first grid value fixed. It discretizes the advective form directly; it is not a conservative shock-capturing solver.

### Diffusion

Forward Euler in time and a centered second difference in space give

$$
u_i^{n+1}=u_i^n+\nu\frac{\Delta t}{(\Delta x)^2}\left(u_{i+1}^n-2u_i^n+u_{i-1}^n\right).
$$

Only interior points are updated, so both endpoint values remain fixed at their initial value of 1.

## Experimenting with the solvers

Edit the parameters near the top of each script or in the first code cell of the notebook.

| Parameter | Convection scripts | Diffusion notebook |
| --- | --- | --- |
| Spatial resolution | `N_X` | `nx` |
| Time step | `D_T` | `dt`, calculated from `sigma`, `dx`, and `nu` |
| Number of updates | `N_T` | `nt` |
| Transport speed | `C` for linear convection; local `u` for nonlinear convection | — |
| Diffusivity | — | `nu` |

For these explicit schemes, choose parameters that satisfy:

- **Linear convection:** $0\leq c\Delta t/\Delta x\leq1$.
- **Nonlinear convection:** $\max_i|u_i|\Delta t/\Delta x\leq1$, with positive speeds for the implemented backward stencil.
- **Diffusion:** $0\leq\nu\Delta t/(\Delta x)^2\leq1/2$.

Increasing spatial resolution generally requires reducing the time step as well. The diffusion notebook handles this through `dt = sigma * dx**2 / nu`, with `sigma = 0.2` by default.

**Why does convection also look smoother?** The first-order upwind method introduces numerical diffusion. Exact linear convection preserves the pulse shape, but its numerical approximation can smear sharp edges. In the diffusion example, smoothing is part of the governing physics itself.

## Repository layout

```text
CFDFromScratch/
├── Linear Convection.py      # Constant-speed 1D transport
├── NonLinear Convection.py   # 1D transport with speed determined by u
├── Diffusion.ipynb           # Derivation, implementation, and animation
├── functions.py             # Shared Matplotlib animation helper
├── ProjectProposal.pdf      # Project proposal
└── README.md
```

`animate_evolution(xspace, tspace, states, interval=100, y_limits=(0.5, 2.5))` takes spatial coordinates, frame times, and a dictionary mapping each frame time to a field array. It returns a Matplotlib `FuncAnimation`. The `interval` argument controls playback delay in milliseconds, independently of the simulated time step.

## Current limitations

- The examples cover 1D scalar equations; multidimensional flow, pressure coupling, and Navier–Stokes solvers are not implemented yet.
- The convection scripts record states before each update and use `linspace` for frame times. The displayed timestamps therefore do not exactly match the update spacing `D_T`, and the final computed state is not included in the animation.
- The diffusion notebook's explanatory Markdown contains derivative and index typos; the update equation above reflects its implemented stencil.
- The shared animation legend currently reads “1D Advection” for all examples, including diffusion.
