# -*- coding: utf-8 -*-
"""DTW plotting functions"""

import numpy as np
import pandas as pd


def AlignmentPlot(alignment_vector, query_index="Query Log index", reference_index="Reference Log index", **kwargs):
    """
    Plotting of dynamic time warp results: annotated warping function

    **Details**
    Display the query and reference well logs and their warping curve, arranged for visual inspection.
    The query log is plotted in the bottom panel, with indices
    growing rightwards and values upwards. Reference log is in the left panel,
    indices growing upwards and values leftwards. 

    Parameters
    ----------
    alignment_vector : object
        an alignment result, object of class `DtwResult`
    query_index: str
        name of query_index label
    reference_index: str
        name of reference_index label
    ... : 
        additional arguments, used for the warping curve

    Returns
    -------
    axes: figure axes
    """

    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(figsize=(6, 6))

    axes.plot(alignment_vector[:,0], alignment_vector[:,1], **kwargs)
    axes.set_xlabel(query_index)
    axes.set_ylabel(reference_index)

    plt.show()
    return axes

def ThreeWayPlot(alignment_vector, query=None, reference=None,
                    match_indices=None,
                    match_col="gray",
                    query_label="Query log index",
                    reference_label="Reference log index", **kwargs):
    """
    Plotting of dynamic time warp results: annotated warping function

    **Details**
    Display the query and reference well logs and their warping curve, arranged for visual inspection.
    The query log is plotted in the bottom panel, with indices
    growing rightwards and values upwards. Reference log is in the left panel,
    indices growing upwards and values leftwards. 

    Parameters
    ----------
    alignment_vector :  object
        an alignment result, object of class `DtwResult`
    query: Series
        query log (log of considerable interest)
    reference: Series
        log from another well, which we intend to correlate or align with the `query` log.
    query_label : 
        label for the query axis
    reference_label : 
        label for the reference axis
    match_indices : 
        indices for which to draw a visual guide
    ... : 
        additional arguments, used for the warping curve

    Returns
    -------
    axes: figure axes
    """
    
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec
    from matplotlib import collections  as mc

    # Test: query and reference parameters are required as series.
    if isinstance(query, pd.Series) & isinstance(reference, pd.Series):

        len_query = len(query)
        len_ref = len(reference)
        len_query1 = np.arange(len_query)
        len_ref1 = np.arange(len_ref)

        fig = plt.figure()
        grid = gridspec.GridSpec(2, 2,
                            width_ratios=[1, 3],
                            height_ratios=[3, 1])
        axes_ref = plt.subplot(grid[0])
        axes = plt.subplot(grid[1])
        axes_query = plt.subplot(grid[3])

        axes_query.plot(len_query1, query)  # query, horizontal, bottom
        axes_query.set_xlabel(query_label)

        axes_ref.plot(reference, len_ref1)  # ref, vertical
        axes_ref.invert_xaxis()
        axes_ref.set_ylabel(reference_label)

        axes.plot(alignment_vector[:,0], alignment_vector[:,1])

        if match_indices is None:
            indices = []
        elif not hasattr(match_indices, "__len__"):
            indices = np.linspace(0, len(alignment_vector[:,0]) - 1, num=match_indices)
        else:
            indices = match_indices
        indices = np.array(indices).astype(int)

        col = []
        for index in indices:
            col.append([(alignment_vector[:,0][index], 0),
                        (alignment_vector[:,0][index], alignment_vector[:,1][index])])
            col.append([(0, alignment_vector[:,1][index]),
                        (alignment_vector[:,0][index], alignment_vector[:,1][index])])

        collection = mc.LineCollection(col, linewidths=1, linestyles=":", colors=match_col)
        axes.add_collection(collection)

        plt.show()
        return axes

    else:
        raise ValueError("Both query and reference parameters are required as pandas.core.series.Series object.")

    