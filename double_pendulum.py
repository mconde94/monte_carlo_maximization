import sys
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import imageio

class DoublePendulum():

    def __init__(self,L1,L2,m1,m2):
        self.L1 = L1
        self.L2 = L2
        self.m1 = m1
        self.m2 = m2
        self.g = 9.81
        self.tmax= 30
        self.dt = 0.01
        # Check that the calculation conserves total energy to within some tolerance.
        self.EDRIFT = 0.05
        self.r = 0.05
        self.fps = 10
        self.di = int(1 / self.fps / self.dt)
        self.fig = plt.figure(figsize=(8.3333, 6.25), dpi=72)
        self.ax = self.fig.add_subplot(111)
        self.pic_paths_list = []

    def deriv(self,y, t, L1, L2, m1, m2):
        """Return the first derivatives of y = theta1, z1, theta2, z2."""
        theta1, z1, theta2, z2 = y

        c, s = np.cos(theta1 - theta2), np.sin(theta1 - theta2)

        theta1dot = z1
        z1dot = (m2 * self.g * np.sin(theta2) * c - m2 * s * (L1 * z1 ** 2 * c + L2 * z2 ** 2) -
                 (m1 + m2) * self.g * np.sin(theta1)) / L1 / (m1 + m2 * s ** 2)
        theta2dot = z2
        z2dot = ((m1 + m2) * (L1 * z1 ** 2 * s - self.g * np.sin(theta2) + self.g * np.sin(theta1) * c) +
                 m2 * L2 * z2 ** 2 * s * c) / L2 / (m1 + m2 * s ** 2)
        return theta1dot, z1dot, theta2dot, z2dot

    def calc_E(self,y):
        """Return the total energy of the system."""

        th1, th1d, th2, th2d = y.T
        V = -(self.m1+self.m2)*self.L1*self.g*np.cos(th1) - self.m2*self.L2*self.g*np.cos(th2)
        T = 0.5*self.m1*(self.L1*th1d)**2 + 0.5*self.m2*((self.L1*th1d)**2 + (self.L2*th2d)**2 +
                2*self.L1*self.L2*th1d*th2d*np.cos(th1-th2))
        return T + V

    def iterate(self):
        # Maximum time, time point spacings and the time grid (all in s).
        self.t = np.arange(0, self.tmax+self.dt, self.dt)
        # Initial conditions: theta1, dtheta1/dt, theta2, dtheta2/dt.
        y0 = np.array([3*np.pi/7, 0, 3*np.pi/4, 0])

        # Do the numerical integration of the equations of motion
        y = odeint(self.deriv, y0, self.t, args=(self.L1, self.L2, self.m1, self.m2))

        # Total energy from the initial conditions
        E = self.calc_E(y0)
        if np.max(np.sum(np.abs(self.calc_E(y) - E))) > self.EDRIFT:
            sys.exit('Maximum energy drift of {} exceeded.'.format(self.EDRIFT))

        # Unpack z and theta as a function of time
        theta1, theta2 = y[:,0], y[:,2]

        # Convert to Cartesian coordinates of the two bob positions.
        self.x1 = self.L1 * np.sin(theta1)
        self.y1 = -self.L1 * np.cos(theta1)
        self.x2 = self.x1 + self.L2 * np.sin(theta2)
        self.y2 = self.y1 - self.L2 * np.cos(theta2)

        # Plotted bob circle radius
        # Plot a trail of the m2 bob's position for the last trail_secs seconds.
        trail_secs = 1
        # This corresponds to max_trail time points.
        self.max_trail = int(trail_secs / self.dt)

    def make_plot(self,i):
        # Plot and save an image of the double pendulum configuration for time
        # point i.
        # The pendulum rods.
        self.ax.plot([0, self.x1[i], self.x2[i]], [0, self.y1[i], self.y2[i]], lw=2, c='k')
        # Circles representing the anchor point of rod 1, and bobs 1 and 2.
        c0 = Circle((0, 0), self.r/2, fc='k', zorder=10)
        c1 = Circle((self.x1[i], self.y1[i]), self.r, fc='b', ec='b', zorder=10)
        c2 = Circle((self.x2[i], self.y2[i]), self.r, fc='r', ec='r', zorder=10)
        self.ax.add_patch(c0)
        self.ax.add_patch(c1)
        self.ax.add_patch(c2)

        # The trail will be divided into ns segments and plotted as a fading line.
        ns = 20
        s = self.max_trail // ns

        for j in range(ns):
            imin = i - (ns-j)*s
            if imin < 0:
                continue
            imax = imin + s + 1
            # The fading looks better if we square the fractional length along the
            # trail.
            alpha = (j/ns)**2
            self.ax.plot(self.x2[imin:imax], self.y2[imin:imax], c='r', solid_capstyle='butt',
                    lw=2, alpha=alpha)

        # Centre the image on the fixed anchor point, and ensure the axes are equal
        self.ax.set_xlim(-self.L1-self.L2-self.r, self.L1+self.L2+self.r)
        self.ax.set_ylim(-self.L1-self.L2-self.r, self.L1+self.L2+self.r)
        self.ax.set_aspect('equal', adjustable='box')
        plt.axis('off')
        pic_path = 'frames/_img{:04d}.png'.format(i//self.di)
        self.pic_paths_list.append(pic_path)
        plt.savefig(pic_path, dpi=72)
        plt.cla()

    def make_gif(self):
        images = []
        for filename in self.pic_paths_list:
            images.append(imageio.imread(filename))
        imageio.mimsave('double_pendulum.gif', images)

    def run_all(self):
        self.iterate()
        # Make an image every di time points, corresponding to a frame rate of fps
        # frames per second.
        # Frame rate, s-1
        for i in range(0, self.t.size, self.di):
            print(i // self.di, '/', self.t.size // self.di)
            self.make_plot(i)
        self.make_gif()


inputs = {'L1':1,
          'L2':1,
          'm1':1,
          'm2':1.3}

if __name__ == "__main__":
    obj = DoublePendulum(**inputs)
    obj.run_all()