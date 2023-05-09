import matplotlib.pyplot as pyplot
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np 
from scipy.signal import hilbert, chirp

def plot_column(bscan_data, column=0):
    bscan_data = bscan_data[:,column]
    analytical_bscan_data = hilbert(bscan_data)
    pyplot.plot(bscan_data)
    pyplot.plot(np.absolute(analytical_bscan_data))
    pyplot.show()

def do_later():

    # do background subtraction
    # convert x axis to distance
    ax = pyplot.subplot()
    #bscan_data = np.fft(bscan_data)
    im = ax.imshow(bscan_data, extent=[0, 512, 1200, 0], aspect='auto')
    # pyplot.ylim(1400, 1000)
    pyplot.title('43cm tag from radar')
    pyplot.ylabel('mm (from radar)')
    pyplot.xlabel('radar frame')

    # ax.set_yticks([0, 2048, 4095], [0.0, 600.0, 1200.0])
    # create an Axes on the right side of ax. The width of cax will be 5%
    # of ax and the padding between cax and ax will be fixed at 0.05 inch.
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)

    pyplot.colorbar(im, cax=cax)
    
    pyplot.show()
    print('end')


if __name__ == "__main__":
    bscan_data = np.genfromtxt('46cm_walabot_100ms_tag.csv', delimiter=',')
    # bg_frame = np.genfromtxt('43cm_tag_1s_bg.csv')
    t = np.genfromtxt('46cm_walabot_100ms_tag_timestamps.csv', delimiter=',')
    bscan_data = np.transpose(bscan_data)

    #bscan_data = bscan_data - bg_frame

    bscan_data = np.transpose(bscan_data)
    #bscan_data = np.absolute(bscan_data)
    
    # plot_column(bscan_data)
    do_later()
