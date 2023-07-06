import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def next_state(grid):
   
    new_grid = np.zeros(grid.shape, dtype=bool)

    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
           
            live_neighbors = np.sum(grid[max(0, i-1):min(grid.shape[0], i+2), max(0, j-1):min(grid.shape[1], j+2)]) - grid[i, j]

            if grid[i, j] and (live_neighbors < 2 or live_neighbors > 3):
                new_grid[i, j] = False
            elif not grid[i, j] and live_neighbors == 3:
                new_grid[i, j] = True
            elif grid[i, j] and (live_neighbors == 2 or live_neighbors == 3):
                new_grid[i, j] = True

    return new_grid


grid = np.random.choice([False, True], size=(50, 50))


fig, ax = plt.subplots()

def update(i):
    global grid
    ax.clear()
    ax.imshow(grid, cmap='binary')
    ax.set_xticks([])
    ax.set_yticks([])
    grid = next_state(grid)

ani = animation.FuncAnimation(fig, update, frames=100)

plt.show()
