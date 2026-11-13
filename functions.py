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