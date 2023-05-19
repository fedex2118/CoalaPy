import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np
from math import nan


def plot_data(x, y1, y2, y3, title, ylabel):
    log_x = np.log10(x)
    
    plot_y1 = False
    plot_y2 = False
    plot_y3 = False
    
    if y1:
        plot_y1 = True
    if y2:
        plot_y2 = True
    if y3:
        plot_y3 = True

    plt.figure(figsize=(10,6))
    
    color_y1 = "red"
    color_y2 = "royalblue"
    color_y3 = "forestgreen"
    
    linestyle_y1 = "--"
    linestyle_y2 = ":"
    linestyle_y3 = "-."
    
    label_y1 = 'Bio.Phylo'
    label_y2 = 'DendroPy'
    label_y3 = 'ETE3'
    
    log_y1 = []
    log_y2 = []
    log_y3 = []
    
    if plot_y1:
        log_y1 = np.log10(y1)
        plt.plot(log_x, log_y1, 'o-', linestyle=linestyle_y1, color=color_y1)
    if plot_y2:
        log_y2 = np.log10(y2)
        plt.plot(log_x, log_y2, 'o-', linestyle=linestyle_y2, color=color_y2)
    if plot_y3:
        log_y3 = np.log10(y3)
        plt.plot(log_x, log_y3, 'o-', linestyle=linestyle_y3, color=color_y3)

    # creation of ticks, y uses custom ones
    x_labels = x
    y_labels = ["10\u207b\u2070", "10\u207b\xb2", "10\u207b\xb9", "10\u2070", "10\xb9", "10\xb2", "10\xb3"]
    
    y = [10**-3, 10**-2, 10**-1, 10**0, 10**1, 10**2, 10**3]
    plt.xticks(log_x, x_labels)
    plt.yticks(np.log10(y), y_labels)


    # ticks for y
    ax = plt.gca()
    ax.yaxis.set_ticks(np.concatenate((log_y1, log_y2, log_y3)), minor=True)
    ax.set_yticklabels(y_labels, fontsize='11')
    ax.set_xticklabels(x_labels, fontsize='11')


    # x, y names
    plt.xlabel('Number of Leaves', fontsize='11')
    plt.ylabel(ylabel, fontsize='11')

    plt.title(title)

    plt.grid(False)
    
    # Lines for legend
    line1 = mlines.Line2D([], [], linestyle=linestyle_y1, color=color_y1, markersize=15, label=label_y1)
    line2 = mlines.Line2D([], [], linestyle=linestyle_y2, color=color_y2, markersize=15, label=label_y2)
    line3 = mlines.Line2D([], [], linestyle=linestyle_y3, color=color_y3, markersize=15, label=label_y3)
    
    # Legend
    legend = plt.legend(handles=[line1, line2, line3], loc='upper left')
    
    # Text color
    legend.get_texts()[0].set_color(line1.get_color())
    legend.get_texts()[1].set_color(line2.get_color())
    legend.get_texts()[2].set_color(line3.get_color())
    
    plt.show()



# Input
leaves = [10, 100, 1000, 10000, 100000] # leaves
execution_time_label = "Execution Time (seconds)"
mem_usage_label = "Memory Usage (MB)"

# Load execution time:
biopython_load_time = [0.00015731603307358454, 0.0010421274333566543, 
     0.007479889766788498, 0.18686582139986666, 1.7723854481168018]
dendroPy_load_time = [0.0004518484167419956, 0.0035951785331538606, 0.033410964433460325,
                      0.5359831678835689, 10.313732832783293]
ete3_load_time = [0.0002210363333991457, 0.0013737565835375183, 0.023994095550309187,
                  0.2059684280333992, 2.394691006383497]

plot_data(leaves, biopython_load_time, dendroPy_load_time, ete3_load_time,
                    "Load Tree (Execution Time)", execution_time_label)

# Load memory usage:
biopython_load_mem = [0.008399866666666667, 0.10222186666666667, 1.0634232,
                      10.6493332, 106.579706]
dendroPy_load_mem = [0.017098400000000003, 0.1676454666666667, 1.6674692,
                     16.475016266666668, 167.91709533333335]
ete3_load_mem = [0.008079633333333332, 0.09746110000000001, 1.0695449666666665,
                 10.798730833333334, 108.18882083333332]

plot_data(leaves, biopython_load_mem, dendroPy_load_mem, ete3_load_mem,
                    "Load Tree (Memory Usage)", mem_usage_label)

# Preorder
biopython_pre_time = [0.009095687000808539, 0.05650303100264864, 0.6262769400018442,
                      5.787008057999628, 64.35174629700123]
dendroPy_pre_time = [0.017958208001800813, 0.15122151200193912, 1.6724014660030662,
                     16.019918406000215, nan]
ete3_pre_time = [0.007133678998798132, 0.05053734899775009, 0.5300769889981893,
                 5.045954938999785, 51.50761510099983]

plot_data(leaves, biopython_pre_time, dendroPy_pre_time, ete3_pre_time,
          "Pre-order Traversal", execution_time_label)

# Inorder
biopython_in_time = []
dendroPy_in_time = [0.0214506939992134, 0.16040190100102336, 1.8950629780010786,
                    18.474239554001542, nan]
ete3_in_time = []

plot_data(leaves, biopython_in_time, dendroPy_in_time, ete3_in_time,
          "In-order Traversal", execution_time_label)

# Postorder
biopython_post_time = [0.010868665998714278, 0.05871436500092386, 0.6370462060003774,
                       6.785569609997765, 65.83900364100191]
dendroPy_post_time = [0.022444065001764102, 0.15538908500093385, 1.72158565099744, 
                      16.52253994900093, nan]
ete3_post_time = [0.008682053001393797, 0.05697300800238736, 0.6080341720007709,
                  5.726655216996733, 58.045722294998995]

plot_data(leaves, biopython_post_time, dendroPy_post_time, ete3_post_time,
          "Post-order Traversal", execution_time_label)

# Levelorder
biopython_level_time = [0.009585780000634259, 0.054719394000130706, 0.7900085569999646,
                        7.0579358549985045, 75.16901795299782]
dendroPy_level_time = [0.024767487000644905, 0.15162906699697487, 2.1616000150024774,
                       20.60662450200107, nan]
ete3_level_time = [0.010312424001313047, 0.04849434300194844, 0.6599777809969964,
                   5.964638386001752, 88.090368861]

plot_data(leaves, biopython_level_time, dendroPy_level_time, ete3_level_time,
          "Level-order Traversal", execution_time_label)
