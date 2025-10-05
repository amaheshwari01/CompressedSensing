import numpy as np
import matplotlib.pyplot as plt
import time


# Global state for the display
_display_state = {
    'fig': None,
    'ax': None,
    'im': None
}


def display_grid(grid):
    """Display a 1080p grid (1920x1080)."""
    global _display_state
    
    dpi = 100
    height, width = grid.shape
    
    # Check if this is the first call
    if _display_state['fig'] is None:
        # Disable toolbar in matplotlib settings
        plt.rcParams['toolbar'] = 'None'
        
        # Create figure
        fig, ax = plt.subplots(figsize=(width/dpi, height/dpi), dpi=dpi)
        
        # Set background colors to black
        fig.patch.set_facecolor('black')
        ax.set_facecolor('black')
        
        # Remove all borders, axes, and padding
        ax.set_position([0, 0, 1, 1])
        ax.axis('off')
        fig.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)
        
        # Display the grid
        im = ax.imshow(grid, cmap='gray', vmin=0, vmax=1, interpolation='nearest')
        
        # Store state
        _display_state['fig'] = fig
        _display_state['ax'] = ax
        _display_state['im'] = im
        
        # Hide toolbar - try multiple methods for different backends
        manager = plt.get_current_fig_manager()
        if manager.toolbar:
            try:
                manager.toolbar.setVisible(False)  # Qt backend
            except:
                pass
            try:
                manager.toolbar.pack_forget()  # Tk backend
            except:
                pass
            try:
                manager.window.toolbarVisible = False  # macOS backend
            except:
                pass
        
        # Maximize window
        try:
            manager.window.state('zoomed')  # Windows
        except:
            try:
                manager.full_screen_toggle()  # Some backends
            except:
                pass
        
        # Turn on interactive mode
        plt.ion()
        plt.show()
        
        # Force initial display
        fig.canvas.draw()
        fig.canvas.flush_events()
    else:
        # Fast update path - just update data and flush
        _display_state['im'].set_data(grid)
        _display_state['fig'].canvas.flush_events()
    
    # Minimal pause for event processing
    plt.pause(0.1)


def close_display():
    """Close the display window."""
    global _display_state
    if _display_state['fig'] is not None:
        plt.close(_display_state['fig'])
        _display_state = {'fig': None, 'ax': None, 'im': None}


if __name__ == "__main__":
    # Example usage
    IMAGE_WIDTH = 1920
    IMAGE_HEIGHT = 1080
    
    START_X = 500
    START_Y = 500
    END_X = START_X+700
    END_Y = START_Y+700

    X_COUNT = 50
    Y_COUNT = 50


    PIXEL_WIDTH = (END_X - START_X) // X_COUNT
    PIXEL_HEIGHT = (END_Y - START_Y) // Y_COUNT

    

    grid = np.zeros((IMAGE_HEIGHT, IMAGE_WIDTH))

    for i in range(Y_COUNT):
        for j in range(X_COUNT):
            grid[START_Y+i*PIXEL_HEIGHT:START_Y+(i+1)*PIXEL_HEIGHT, START_X+j*PIXEL_WIDTH:START_X+(j+1)*PIXEL_WIDTH] = 1
            display_grid(grid)
            # time.sleep(.2)
            grid[START_Y+i*PIXEL_HEIGHT:START_Y+(i+1)*PIXEL_HEIGHT, START_X+j*PIXEL_WIDTH:START_X+(j+1)*PIXEL_WIDTH] = 0


            
            
