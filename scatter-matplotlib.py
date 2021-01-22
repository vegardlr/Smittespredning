#!/usr/bin/env python
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time

class AnimatedScatter(object):
    """An animated scatter plot using matplotlib.animations.FuncAnimation."""
    def __init__(self, numpoints=50):
        self.numpoints = numpoints
        self.stream = self.data_stream()

        # Setup the figure and axes...
        self.fig, self.ax = plt.subplots()
        # Then setup FuncAnimation.
        self.ani = animation.FuncAnimation(self.fig, self.update, interval=5, 
                                          init_func=self.setup_plot, blit=True)

    def setup_plot(self):
        """Initial drawing of the scatter plot."""
        x, y, s, c = next(self.stream).T
        self.scat = self.ax.scatter(x, y, c=c, s=s, vmin=0, vmax=1,
                                    cmap="jet", edgecolor="k")
        self.ax.axis([-10, 10, -10, 10])
        # For FuncAnimation's sake, we need to return the artist we'll be using
        # Note that it expects a sequence of artists, thus the trailing comma.
        return self.scat,

    def data_stream(self):
        """Generate a random walk (brownian motion). Data is scaled to produce
        a soft "flickering" effect."""
        red = 0.9
        blue = 0.1
        
        xy = (np.random.random((self.numpoints, 2))-0.5)*10
        s = np.ones(self.numpoints)*0.1
        c = np.ones(self.numpoints)*0.1
        age = np.zeros(self.numpoints)
        day = 0
        c[0] = red
        sick = 0
        immune = 0
        #s, c = np.random.random((self.numpoints, 2)).T
        while True:
            print(sick,immune)
            time.sleep(0.1)
            day += 1
            xy += 0.5 * (np.random.random((self.numpoints, 2)) - 0.5)
            for i in range(self.numpoints):
                one = xy[i]
                if(c[i] == red):
                    age[i] += 1
                    if(age[i]>100):
                        c[i] = blue
                        immune += 1
                        sick -= 1
                        #age[i] = 0
                for j in range(self.numpoints):
                    other=xy[j]
                    if i == j: 
                        continue
                    if((one[0]-other[0])**2 + (one[1]-other[1])**2 < 0.6):
                        if(c[i] == red and age[j]==0): 
                            c[j]=red
                            sick += 1
                        if(c[j] == red and age[i]==0): 
                            c[i]=red
                            sick += 1
                        #print(c[i],c[j])
                        #print(one,other)
                        #print("---")
            #s += 0.00 * (np.random.random(self.numpoints) - 0.5)
            #c += 0.00 * (np.random.random(self.numpoints) - 0.5)
            yield np.c_[xy[:,0], xy[:,1], s, c]

    def update(self, i):
        """Update the scatter plot."""
        data = next(self.stream)

        # Set x and y data...
        self.scat.set_offsets(data[:, :2])
        # Set sizes...
        self.scat.set_sizes(300 * abs(data[:, 2])**1.5 + 100)
        # Set colors..
        self.scat.set_array(data[:, 3])

        # We need to return the updated artist for FuncAnimation to draw..
        # Note that it expects a sequence of artists, thus the trailing comma.
        return self.scat,


if __name__ == '__main__':
    a = AnimatedScatter()
    plt.show()