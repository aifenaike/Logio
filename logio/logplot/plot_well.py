import matplotlib.pyplot as plt
import numpy as np

class PlotWell:

    def __init__(self, dataset, depth, name_of_well=str, depth_range=tuple, logs=list):
        """
        Visualize well logs 
    
        Parameters
        ----------
        :param dataset: Well log data (DataFrame Object)
        :param depth: Information about the Depth at which log readings were taken. (DataFrame)
        :param name_of_well: Name of Well. (str)
        :param depth_range: A user specified tuple. This refers to the range of depth within which user intend to visualize. (Tuple)
        :param logs: A list of logs required to plot. The list must contain strings only. (list)
        """

        self.dr = depth_range
        self.logs = logs
        self.data = dataset
        self.depth = depth
        self.name_of_well = name_of_well

        self.plot_well()



    def plot_well(self):
        '''Base function/method for visualization'''
        self.data = self.data[self.logs]
        fig, axes = plt.subplots(1,ncols=len(self.logs),figsize = (15,10),sharey=True)
        for log, i in zip(self.logs, range(len(self.logs))):
            if log == 'CALI':
                # Plot Caliper log
                # Normalize and shift caliper self.logs to optimize display
                axes[i].plot(self.data[log],self.depth,'k-', linewidth='0.7')
                axes[i].set_title('Caliper', fontsize=14) # assign title
                axes[i].tick_params(axis='x', colors='black')
        
            elif log == 'GR':
                # Plot Gamma ray log
                left_col_value = 0
                right_col_value = 150
                gr_span = abs(left_col_value - right_col_value) #calculate the span of values
                gr_cmap = plt.get_cmap('RdYlGn') #assign a color map
                gr_color_index = np.arange(left_col_value, right_col_value, gr_span / 100) #create array of color values
                axes[i].plot(self.data[log],self.depth,'g-', linewidth='0.7')
                axes[i].set_xlabel("Gamma Ray", color='g', fontsize=14) # assign title
                axes[i].tick_params(axis='x', colors='g')
                for index in sorted(gr_color_index): #loop through each value in the color_index
                    index_value = (index - left_col_value) / gr_span
                    color = gr_cmap(index_value)
                    axes[i].fill_betweenx(self.depth, 0, self.data[log], where=(self.data[log]>=index), color = color, linewidth=0, alpha=.75)
            elif log == 'NPHI':
                # Plot Neutron Log
                axes[i].plot(self.data[log],self.depth,'m-', linewidth='0.7')
                axes[i].set_xlabel("Neutron", color='m', fontsize=14) # assign title
                axes[i].tick_params(axis='x', colors='m')
            elif log == 'RT':
            # Plot Resistivity log
                axes[i].plot(self.data[log],self.depth,'r-', linewidth='0.7')
                axes[i].set_xscale('log')
                axes[i].fill_betweenx(self.depth, 100, self.data[log], where=(self.data[log]>=100), color = 'red', linewidth=0, alpha=.75)
                axes[i].set_xlabel("Resistivity", color='r', fontsize=14) # assign title
                axes[i].tick_params(axis='x', colors='r')
            else:
                # Plot other log types  
                axes[i].plot(self.data[log],self.depth,'b-', linewidth='0.7')        
                axes[i].fill_betweenx(self.depth, 1.65, self.data[log], where=(self.data[log]<=1.65), color = 'blue', linewidth=0, alpha=.75)
                axes[i].set_xlabel(log, color='b', fontsize=14)
                axes[i].tick_params(axis='x', colors="blue")
                axes[i].spines["top"].set_edgecolor("blue")
            rf = self.data[self.depth.between(self.dr[0],self.dr[1])]
            axes[i].set_xlim(min(rf[log]), max(rf[log]))
        
    
            
        # Set other plot parameters
        fig.suptitle(f'Well: {self.name_of_well}', fontsize=15)
        fig.text(0.08, 0.5, 'DEPTH', va='center', rotation='vertical', fontsize=15)
        for i, j in zip(self.logs, range(len(axes))):
            axes[j].set_ylim(self.dr)
            axes[j].invert_yaxis()
            axes[j].minorticks_on()
            axes[j].xaxis.tick_top()
            axes[j].xaxis.set_label_position("top")
            axes[j].grid(which='major', linestyle='-', linewidth='0.5', color='green')
            axes[j].grid(which='minor', linestyle=':', linewidth='0.5', color='black')
            #ax[j].set_title(f'{i}\n', fontsize=15)
        # plt.subplots_adjust(wspace=0)

    def show(self):
        '''Display well'''
        plt.subplots_adjust(wspace=0)
        plt.show()

