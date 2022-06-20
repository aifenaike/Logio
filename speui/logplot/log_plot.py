import matplotlib.pyplot as plt
import lasio
from pandas import DataFrame
from numpy import arange

class InvalidFormatException(Exception):
    """Format does not conform with the required format"""
    pass

class LogPlot:

    def __init__(self, data):
        """
        Visualize well logs

        Parameters
        ----------
        data: lasio.las.LASFile or pd.DataFrame object
        """

        if type(data) == lasio.las.LASFile:
            self.df = data.df()
        elif type(data) == DataFrame:
            self.df = data
        else:
            raise InvalidFormatException('data input is neither a LASFile nor DataFrame object')


    def plot_log(self, plots: list, y: str="DEPTH", y_range:tuple = (0,0,0), xscale:list = ['linear'], **kwargs):

        """
        Base function/method for visualization

        Parameters
        ----------
        plots: list; a list of required plots to make. The list can contain strings and tuples. 
                Use tuple to plot more than one log on an axes i.e ("GR", "BS") will plot the GR 
                log and the BS log on the same axes
        y: str; name of column in dataframe to be plotted on the vertical axis
        y_range: tuple, value range for the y-axis, passed to the plot as ylim()
        xscale : {"linear", "log", "symlog", "logit", ...} The scale type to apply to the x-axis, 
                default = 'linear'.
        **kwargs: These are passed to the subplots function, e.g: figsize = (4, 9), dpi = 60
        """

        # Checking the inputs
        dataframe = self.df.reset_index()
        if len(y_range) == 2:
            self.dr = y_range
        else:
            self.dr = (dataframe[y].min() - (dataframe[y].max()* 0.02), dataframe[y].max() * 1.02)
        self.plots = plots
        self.fig, self.axes = plt.subplots(ncols=len(self.plots), facecolor = '#E9E9E9', **kwargs)
        colors = ['black', 'darkred', 'green', 'darkblue', 'orange', '']

        if len(xscale) == 1:
            self.xscale = [xscale[0] for i in self.plots]
        elif len(xscale) != len(plots):
            raise InvalidFormatException('Length of xscale != length of plots')
        else:
            self.xscale = xscale

        # Plotting a single variable on an axis
        def plotter(axis, plot_var, scale):
            axis.plot(dataframe[plot_var], dataframe[y], lw=.8)
            axis.set_xscale(scale)
            axis.set_xlabel(plot_var)
            axis.legend(labels = [plot_var])
            axis.set_ylim(self.dr)
            axis.invert_yaxis()
            axis.minorticks_on()
            axis.grid(which="major", linestyle='-', linewidth=0.7, color="black")
            axis.grid(which="minor", linestyle='-.', linewidth=0.7, color="#CDC0B0")
        
        # Plotting 2 variables on an axis
        def tuple_plotter(axis, plot_var, scale):
            axis.plot(dataframe[plot_var[0]], dataframe[y], lw= .6)
            axis.set_xscale(scale)
            axis.set_xlabel(plot_var[0])
            axis.legend(labels = [plot_var[0]], loc = 'upper right', borderaxespad = .1, bbox_to_anchor=(0.95, 0.96))
            ax2 = axis.twiny()
            ax2.plot(dataframe[plot_var[1]], dataframe[y], color= 'red', lw= .6)
            ax2.set_xscale(scale)
            ax2.set_xlabel(plot_var[1])
            ax2.legend(labels = [plot_var[1]], loc = 'upper right', borderaxespad = .1, bbox_to_anchor=(0.95, 0.94))
            axis.set_ylim(self.dr)
            axis.invert_yaxis()
            axis.minorticks_on()
            axis.grid(which="major", linestyle='-', linewidth=0.7, color="black")
            axis.grid(which="minor", linestyle='-.', linewidth=0.7, color="#CDC0B0")

        
        try:
            self.axes[0].set_ylabel(y)

            for plott, x_scale, axe in zip(self.plots, self.xscale, self.axes):

                if type(plott) == tuple:
                    tuple_plotter(axe, plott, x_scale)
                else:
                    plotter(axe, plott, x_scale)

                if axe != self.axes[0]:
                    axe.set_yticklabels([])

            plt.subplots_adjust(wspace = .02, hspace=.05)

        except TypeError:
            self.axes.set_ylabel(y)

            for plott in self.plots:

                if type(plott) == tuple:
                    tuple_plotter(self.axes, plott, self.xscale[0])
                else:
                    plotter(self.axes, plott, self.xscale[0])

            plt.subplots_adjust(wspace = .05, hspace=.05)

    def show(self):
        plt.tight_layout()
        plt.show()


    def cutoff_plot(self, x, y, x_cutoff,  y_range: tuple = (0,0), xscale:str = 'linear', colors: list = ['red', 'lightblue'],labels: list = ['Cat_A', 'Cat_B'], fig_size : tuple = (4.5, 10)):
        """
        Plots a visualization for a single log with a cutoff value for the x variable
        Parameters
        ----------
        dataframe: pandas.DataFrame object containing the data to be analysed
        x: name of column to be plotted on the x-axis
        y: name of column to be plotted on the y-axis
        x_cutoff: x value for delineating the categories in the x variable
                If specified as a fraction between 0 and 1, it is calculated as:
                (max_x_value - min_x_value) * x_cutoff + min_x_value
                Otherwise, the x plot is separated into sections based on the x value passed
        y_range: tuple, value range for the y-axis, passed to th plot as ylim(),
                default  = (y.min, y.max)
        xscale : {"linear", "log", "symlog", "logit", ...} The scale type to apply to the x-axis, 
                default = 'linear'.
        colors: list containing the colors for filliung the cutoff sections
        labels: list containing the labels for the cutoff sections
        figsize: tuple (width, height) for controlling the size of the plot 
        """

        #Check
        if len(colors) == 2:
            pass
        else:
            raise InvalidFormatException('Length of colors does not match number of partitions')
        
        if len(labels) == 2:
            pass
        else:
            raise InvalidFormatException('Length of labels does not match number of partitions')
        
        # Removing null values from the data to be plotted
        dataframe = self.df[~self.df[x].isnull()]
        y1 = dataframe.reset_index()[y]
        x1 = dataframe[x]
        # Determining the cutoff
        if (x_cutoff > 0) & (x_cutoff< 1):
            x2 = (x1.max() - x1.min()) * x_cutoff + x1.min()
        else:
            x2 = x_cutoff

        plt.figure(figsize = fig_size, dpi = 100, facecolor = '#E9E9E9')
        plt.axes().set_axisbelow(True)
        
        # Plotting the cutoff
        plt.fill_betweenx(y1, x1, x2, where = x2>=x1, facecolor = colors[0], label = labels[0])
        plt.fill_betweenx(y1, x1, x2, where = x2<x1, facecolor = colors[1], label = labels[1])
        plt.vlines(x2, y1.min(), y1.max(), linestyles='dashed', color = '#000000', lw = 1, label = 'cutoff')
        plt.xscale(xscale)
        if y_range[1] != 0:
            plt.ylim(y_range)
        plt.xlabel(x, fontsize = 12)
        plt.ylabel(y, fontsize = 12)
        plt.minorticks_on()
        plt.grid(which="major", linestyle='-', linewidth=0.5, color="black")
        plt.grid(which="minor", linewidth=0.5, color="#CDC0B0")
        plt.gca().invert_yaxis()
        plt.legend();
        