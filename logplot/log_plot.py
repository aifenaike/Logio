import matplotlib.pyplot as plt


class LogPlot:

    def __init__(self, las_file, depth_range=tuple, plots=list):
        """

        :param las_file:
        :param depth_range:
        :param plots: A list of required plots to make. The list can contain strings and tuples. Use tuple to plot more
        than one log on an axes i.e ("GR", "BS") will plot the GR log and the BS log on the same axes
        """

        self.dr = depth_range
        self.plots = plots
        self.df = las_file.df()
        self.depth = self.df.index

        self.fig, self.axes = plt.subplots(ncols=len(self.plots))

        self.plot_log()
        self.legend()




    def plot_log(self):

        # self.fig.
        self.axes[0].set_ylabel("Depth")

        for plot, axe in zip(self.plots, self.axes):

            if type(plot) == tuple:
                for plot in plot:
                    axe.plot(self.df[plot], self.depth, lw=1.3, label=plot)
                    axe.set_xlabel(plot)
            else:
                axe.plot(self.df[plot], self.depth, lw=1.3, label=plot)
                axe.set_xlabel(plot)

            if axe != self.axes[0]:
                axe.get_yaxis().set_visible(False)

            axe.set_ylim(self.dr)
            axe.invert_yaxis()
            axe.grid(linestyle='--', linewidth=0.4)

    def legend(self):
        for axe in self.axes:
            axe.legend()

    def show(self):
        plt.tight_layout()
        plt.show()
