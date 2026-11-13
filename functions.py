import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def animate_evolution(xspace, tspace, states, interval=100, y_limits=(0.5, 2.5)):
    """
    Animates the 1D field evolution across time.
    
    Parameters:
    -----------
    xspace   : np.ndarray -> 1D array of spatial grid coordinates
    tspace   : np.ndarray -> 1D array or list of time steps
    states   : dict       -> Dictionary mapping time t -> spatial array u
    interval : int        -> Frame delay in milliseconds
    y_limits : tuple      -> (ymin, ymax) axis limits for the plot
    
    Returns:
    --------
    anim     : FuncAnimation -> Matplotlib animation object
    """
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.set_xlim(xspace[0], xspace[-1])
    ax.set_ylim(y_limits[0], y_limits[1])
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
        time_text.set_text(f'Time: {t:.3f} s (Step {frame}/{len(tspace)-1})')
        return line, time_text

    anim = FuncAnimation(
        fig, 
        update, 
        frames=len(tspace), 
        init_func=init, 
        interval=interval,  
        blit=True
    )

    # Detect a Jupyter notebook kernel
    try:
        from IPython import get_ipython
        in_notebook = getattr(get_ipython(), "kernel", None) is not None
    except ImportError:
        in_notebook = False

    if in_notebook:
        from IPython.display import HTML, display

        plt.close(fig)
        display(HTML(anim.to_jshtml()))
    else:
        plt.show()

    return anim

def animate_evolution_2d(
    xspace, tspace, states, interval=100, y_limits=(0.5, 2.5)
):
    """
    Animate a 2D field as a 3D surface.

    xspace   : (x_coordinates, y_coordinates)
    tspace   : physical times corresponding to the stored states
    states   : dictionary of {step_index: 2D array}
    interval : frame delay in milliseconds
    y_limits : (minimum, maximum) field height
    """
    x, y = xspace

    # Matches your convention: u[x_index, y_index]
    X, Y = np.meshgrid(x, y, indexing="ij")

    keys = sorted(states)
    times = np.asarray(tspace)

    if len(times) != len(keys):
        raise ValueError("tspace must contain one time per stored state.")

    if any(np.shape(states[key]) != X.shape for key in keys):
        raise ValueError("Each state must have shape (len(x), len(y)).")

    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_subplot(111, projection="3d")

    ax.set_xlim(x[0], x[-1])
    ax.set_ylim(y[0], y[-1])
    ax.set_zlim(*y_limits)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("u")
    ax.view_init(elev=30, azim=-60)

    surface = None
    title = ax.set_title("")

    def update(frame):
        nonlocal surface

        if surface is not None:
            surface.remove()

        surface = ax.plot_surface(
            X, Y, states[keys[frame]],
            cmap="viridis",
            vmin=y_limits[0],
            vmax=y_limits[1],
            rcount=len(x),
            ccount=len(y),
            linewidth=0,
            antialiased=True,
        )

        title.set_text(
            f"Time: {times[frame]:.3f} s "
            f"(Frame {frame}/{len(keys) - 1})"
        )

        return surface, title

    anim = FuncAnimation(
        fig,
        update,
        frames=len(keys),
        interval=interval,
        blit=False,
        repeat=False,
    )

    try:
        from IPython import get_ipython
        in_notebook = getattr(get_ipython(), "kernel", None) is not None
    except ImportError:
        in_notebook = False

    if in_notebook:
        from IPython.display import HTML, display

        plt.close(fig)
        display(HTML(anim.to_jshtml()))
    else:
        plt.show()

    return anim
