import matplotlib.pyplot as plt
import numpy as np
import io


class GenerateAxis:

    def create_axis(self, ratio_value):
        x = np.linspace(0, 30, 1000)
        y = np.linspace(0, 0, 1000)

        # The colormap
        # BrBG_r, GnBu, Greens_r, OrRd, Oranges, PiYG_r, RdBu_r, RdYlBu_r
        cmap = ('RdBu_r')

        # Create figure and axes
        fig = plt.figure(figsize=[4, 2], frameon=False, dpi=250)
        fig.clf()
        ax = fig.add_subplot(1, 1, 1)
        ax.get_yaxis().set_visible(False)
        c = np.linspace(0, 30, 1000)
        ax.scatter(x, y, c=c, cmap=cmap)

        plt.plot(ratio_value, 0, 'kx', markersize=15)

        result_plt = io.BytesIO()
        plt.savefig(result_plt, format='png')
        result_plt.seek(0)

        return result_plt