# -*- coding: utf-8 -*-

import numpy as np
from numba import jit
import matplotlib.pyplot as plt
import seaborn as sns

class BaseWindow():
    """
    Base class on which the desired window constraint is built upon.
    The warping window intuitively controls the amount of distortion allowed when comparing a pair of well logs.

    Note:
    ---------
    Generally they are two types of wapring windows:
    1. Sakoechiba's Window implemented in `SakoechibaWindow` class.
    2. Itakura's Window implemented in `ItakuraWindow` class.

    Methods
    -------
    plot():
        Visualize window (constraint)..   
    """

    def __init__(self):
        pass

    def plot(self):
        """Visualize window (constraint)."""
        _, ax = plt.subplots(1)
        sns.heatmap(self.matrix.T, vmin=0, vmax=1,
            xticklabels=self.matrix.shape[0]//10,
            yticklabels=self.matrix.shape[1]//10,
            ax=ax)
        ax.invert_yaxis()
        ax.set_title(self.label)
        ax.set_xlabel("query index")
        ax.set_ylabel("reference index")
        plt.show()


class NoWindow(BaseWindow):
    """
    No window class.
    
    Attributes
    ----------
        len_x : int
            Length of query log.
        len_y : int
            Length of reference log.

    Methods
    -------
        _gen_window(len_x, len_y):
            Generates the window constraint matrix.   
    """

    label = "no window"
    def __init__(self, len_x, len_y):
        """
        Constructs all the necessary attributes for the NoWindow object.

        Parameters
        ----------
            len_x : int
                Length of query log.
            len_y : int
                Length of reference log.
        """

        self._gen_window(len_x, len_y)

    def _gen_window(self, len_x, len_y):
        self.matrix = np.ones([len_x, len_y], dtype=bool)
        self.list = np.argwhere(self.matrix == True)

#Define warping constraints.
class SakoechibaWindow(BaseWindow):
    """
    Sakoechiba window warping constraint.
    
    Attributes
    ----------
        len_x : int
            Length of query log.
        len_y : int
            Length of reference log.
        size : int
            Size of window width.

    Methods
    -------
        _gen_window(len_x, len_y, size):
            Generates the window constraint matrix.
                
    """

    label = "sakoechiba window"
    def __init__(self, len_x, len_y, size):
        """
        Constructs all the necessary attributes for the SakoechibaWindow object.

        Parameters
        ----------
            len_x : int
                Length of query log.
            len_y : int
                Length of reference log.
            size : int
                Size of window width.
        """
        
        self._gen_window(len_x, len_y, size)

    def _gen_window(self, len_x, len_y, size):
        xx = np.arange(len_x)
        yy = np.arange(len_y)
        self.matrix = np.abs(xx[:,np.newaxis] - yy[np.newaxis, :]) <= size
        self.list = np.argwhere(self.matrix == True)


class ItakuraWindow(BaseWindow):
    """
    A class for the Itakura window warping constraint.

    Attributes
    ----------
        len_x : int
            Length of query log.
        len_y : int
            Length of reference log.
    Methods
    -------
        _gen_window(len_x, len_y):
            Generates the window constraint matrix.
    """

    label = "itakura window"
    def __init__(self, len_x, len_y):
        """
        Constructs all the necessary attributes for the ItakuraWindow object.

        Parameters
        ----------
            len_x : int
                Length of query log.
            len_y : int
                Length of reference log.
        """
       
        self._gen_window(len_x, len_y)

    def _gen_window(self, len_x, len_y):
        self.matrix = _gen_itakura_window(len_x, len_y).astype(np.bool)
        self.list = np.argwhere(self.matrix == True)

#speed up _gen_itakura_window using JIT (just-in-time) compiler .
@jit(nopython=True)
def _gen_itakura_window(len_x, len_y):
    matrix = np.zeros((len_x, len_y), dtype=np.int8)
    for xidx in range(len_x):
        for yidx in range(len_y):
            if (yidx < 2*xidx + 1) and (xidx <= 2*yidx + 1) and \
                (xidx >= len_x - 2*(len_y - yidx)) and \
                (yidx > len_y - 2*(len_x - xidx)):
                matrix[xidx, yidx] = 1
    return matrix


class UserWindow(BaseWindow):
    """
    A class for user defined window constraints.

    Note:
    --------
    Option for a user defined window is implemented in `UserWindow` class.
    The user window defined must be a function that returns a boolean.

    Attributes
    ----------
        len_x : int
            Length of query log.
        len_y : int
            Length of reference log.
        win_func : callable
            Any function which returns bool.
        *args, **kwargs : 
            Arguments for win_func
    Methods
    -------
        _gen_window(len_x, len_y, win_func, *args, **kwargs):
            Generates the window constraint matrix.
    """

    label = "user defined window"
    def __init__(self, len_x, len_y, win_func, *args, **kwargs):
        """
        Constructs all the necessary attributes for the UserWindow object.

        Parameters
        ----------
            len_x : int
                Length of query log.
            len_y : int
                Length of reference log.
            win_func : callable
                Any function which returns bool.
            *args, **kwargs : 
                Arguments for win_func
        """

        self._gen_window(len_x, len_y, win_func, *args, **kwargs)

    def _gen_window(self, len_x, len_y, win_func, *args, **kwargs):
        matrix = np.zeros((len_x, len_y), dtype=np.bool)
        for xidx in range(len_x):
            for yidx in range(len_y):
                if win_func(xidx, yidx, *args, **kwargs):
                    matrix[xidx,yidx] = True
        self.matrix = matrix
        self.list = np.argwhere(self.matrix == True)
