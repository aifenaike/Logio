# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.interpolate import interp1d
from .dtwPlot import *

class DtwResult():
    """
    Result of Dynamic time warping.
    
    Attributes
    ----------
        cumsum_matrix : 2d array
            Alignment matrix
        path : float
           Alignment path.  
            * First column: query path array
            * Second column: reference path array
        window : 2d array
            window constraints
        pattern: 2d array
            Alignment pattern

    Methods
    -------
        get_warping_path(target="query"):
            Get warping path.
        plot_window():
            visualize window
        plot_cumsum_matrix():
            plot heatmap of cumsum_matrix
        plot_path(with_="cum"):
            plot alignment path; warp function/curve
        plot_pattern():
            Plot alignment pattern
        dtw_plot(query=None,reference=None, type=None,**kwargs):
            Plot dynamic time warp results using specific `type` plot.
        plot_aligned_logs(query=None,reference=None):
            plot optimal aligment of both logs.

    """
    def __init__(self, cumsum_matrix, path, window, pattern):
        """
        Constructs all the necessary attributes for the DtwResult object.

        Parameters
        ----------
            cumsum_matrix : 2d array
                Alignment matrix
            path : float
                Alignment path.  
                    * First column: query path array
                    * Second column: reference path array
            window : 2d array
                window constraints
            pattern: 2d array
                Alignment pattern
        """

        self.cumsum_matrix = cumsum_matrix

        if path is None:
            self.dist_only = True
        else:
            self.dist_only = False
            self.path = path

        self._window = window
        self._pattern = pattern

    def get_warping_path(self, target="query"):
        """
        Get warping path.

        Parameters
        ----------
        target : string, "query" or "reference"
            Specify the target to be warped.

        Returns
        -------
        warping_index : 1D array
            Warping index.
        """

        if target not in ("query", "reference"):
            raise ValueError("target argument must be 'query' or 'reference'")
        if target == "reference":
            xp = self.path[:, 0]  # query path
            yp = self.path[:, 1]  # reference path
        else:
            yp = self.path[:, 0]  # query path
            xp = self.path[:, 1]  # reference path
        interp_func = interp1d(xp, yp, kind="linear")
        # get warping index as float values and then convert to int
        # note: Ideally, the warped value should be calculated as mean.
        warping_index = interp_func(np.arange(xp.min(), xp.max()+1)).astype(np.int64)
        # the most left side gives nan, so substitute first index of path
        warping_index[0] = yp.min()

        return warping_index

    def plot_window(self):
        """Visualize window constraint"""
        self._window.plot()

    def plot_cumsum_matrix(self):
        """Plot heatmap of cumsum matrix"""
        # extract max value with ignoring inf
        masked_array = np.ma.masked_array(self.cumsum_matrix,
            mask=self.cumsum_matrix == np.inf)
        _,ax = plt.subplots(1)
        sns.heatmap(self.cumsum_matrix.T, vmax=masked_array.max(), vmin=0,
            xticklabels=self.cumsum_matrix.shape[0]//10,
            yticklabels=self.cumsum_matrix.shape[1]//10,
            ax=ax
        )
        ax.invert_yaxis()
        ax.set_xlabel("query log index")
        ax.set_ylabel("reference log index")
        ax.set_title("cumsum matrix")
        plt.show()

    def plot_path(self, with_="cum"):
        """
        Plot alignment path.

        Parameters
        ----------
        with_ : string, "win" or "cum" or None
            If given, following will be plotted with alignment path:  
            * "win" : window matrix
            * "cum" : cumsum matrix
        """

        if self.dist_only:
            raise Exception("alignment path not calculated.")
        _, ax = plt.subplots(1)
        if with_ is None:
            ax.plot(self.path[:, 0], self.path[:, 1])
        elif with_ == "win":
            sns.heatmap(self._window.matrix.T, vmin=0, vmax=1,
                xticklabels=self._window.matrix.shape[0]//10,
                yticklabels=self._window.matrix.shape[1]//10,
                ax=ax)
            ax.plot(self.path[:, 0], self.path[:, 1], "b")
            ax.invert_yaxis()
        elif with_ == "cum":
            # extract max value with ignoring inf
            masked_array = np.ma.masked_array(self.cumsum_matrix,
                mask=self.cumsum_matrix == np.inf)
            sns.heatmap(self.cumsum_matrix.T, vmax=masked_array.max(), vmin=0,
                xticklabels=self.cumsum_matrix.shape[0]//10,
                yticklabels=self.cumsum_matrix.shape[1]//10,
                ax=ax)
            ax.plot(self.path[:, 0], self.path[:, 1], "y")
            ax.invert_yaxis()
        else:
            raise NotImplementedError("'with_' argument only supports: 'win','cum'")
        ax.set_title("alignment path")
        ax.set_xlabel("query log index")
        ax.set_ylabel("reference log index")
        plt.show()

    def plot_pattern(self):
        """plot step_pattern"""
        self._pattern.plot()

    def dtw_plot(self,query=None,reference=None, type=None,**kwargs):
        """
        Plot dynamic time warp results by displaying alignment contained in ``DtwResult`` object.

        **Details**
        Various plotting styles are available, passing strings to the ``type``
        argument (may be abbreviated):

        -  ``alignment`` plots the warping curve in ``alignment_vector``;
        -  ``threeway`` vis-a-vis inspection of the timeseries and their warping curve;
             see [dtwPlot.ThreeWayPlot()]

        Additional parameters are passed to the plotting functions: use with care.

        Parameters
        ----------
        query:
            log from another well, which we intend to correlate or align with the `reference` log
            
        reference:
            reference log (log of considerable interest)
        xlab : str
            label for the query axis
        ylab : str
            label for the reference axis
        type : str
            general style for the plot, see below
        ... : 
            additional arguments, passed to plotting functions
        """

        alignment_vector = self.path
        if type == "alignment":
            return AlignmentPlot(alignment_vector, **kwargs)
        elif type == "threeway":
            return ThreeWayPlot(alignment_vector,query, reference,**kwargs)

    def plot_aligned_logs(self,query=None,reference=None,):
        """
        Plot query log such that it is locally stretched and/or compressed in order to achieve the best possible match to the reference.

        Parameters
        ----------
        query: array, DataFrame or Series
            log from another well, which we intend to correlate or align with the `reference` log.
        reference: array, DataFrame or Series
            well log used as reference point for correlation.
        """

        x_path = self.path[:,0]
        y_path = self.path[:,1]
        if isinstance(query, np.ndarray) & isinstance(reference, np.ndarray):
            plt.plot(query[x_path],label="aligned query to reference log")
            plt.plot(reference[y_path],label="reference log")
            plt.legend()
            plt.show()
        else:
            plt.plot(query.values[x_path],label="aligned query to reference log")
            plt.plot(reference.values[y_path],label="reference log")
            plt.legend()
            plt.show()
  
    

    

    
