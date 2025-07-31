import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Buat lintasan linear dari (0,0) ke (5,2)
x_vals = np.linspace(0, 5, 50)
y_vals = np.linspace(0, 2, 50)

fig, ax = plt.subplots()
ax.set_xlim(0, 6)
ax.set_ylim(0, 3)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Pergerakan Karakter dalam Game Platform')
ax.grid(True)

# Titik karakter
point, = ax.plot([], [], 'ro', markersize=10)

def init():
    point.set_data([], [])
    return point,

def update(frame):
    x = x_vals[frame]
    y = y_vals[frame]
    point.set_data(x, y)
    return point,

ani = animation.FuncAnimation(
    fig, update, frames=len(x_vals), init_func=init,
    blit=True, interval=100, repeat=False
)

# Simpan sebagai file video
ani.save("pergerakan_karakter_xy.mp4", writer='ffmpeg', fps=10)
