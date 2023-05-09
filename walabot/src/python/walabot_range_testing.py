import WalabotAPI as wlbt
import pprint as pp
import matplotlib.pyplot as pyplot
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np 
import time 


def configure():
    # wlbt.SetProfile(wlbt.PROF_SENSOR)
    wlbt.SetProfile(wlbt.PROF_SENSOR_NARROW)
    # wlbt.SetProfile(wlbt.PROF_SHORT_RANGE_SINGLE_LINE)
    # wlbt.SetProfile(wlbt.PROF_SHORT_RANGE_IMAGING)

    wlbt.SetDynamicImageFilter(wlbt.FILTER_TYPE_NONE)
    # wlbt.SetDynamicImageFilter(wlbt.FILTER_TYPE_MTI)
    # wlbt.SetDynamicImageFilter(wlbt.FILTER_TYPE_DERIVATIVE)




if __name__ == "__main__":
    # wlbt.Disconnect()
    # wlbt.Clean()
    wlbt.Init()
    wlbt.Initialize()
    print('initialized')
    wlbt.ConnectAny()
    configure()
    print('configured')
    #time.sleep(5)
    radar_frames = 100

    wlbt.Start()
    pairs = wlbt.GetAntennaPairs()
    print(pairs)
    selected_pair = 6
    num_pairs = len(pairs)
    print(num_pairs)
    print("collecting the background frame.")
    wlbt.Trigger()
    signal, t = wlbt.GetSignal(pairs[selected_pair])
    bscan_data = np.zeros((num_pairs*radar_frames, len(signal)))

    for i in range(num_pairs):
        print(f'pair number: {i}')
        print("collecting the background frame.")
        wlbt.Trigger()
        signal, t = wlbt.GetSignal(pairs[selected_pair])
        bg_frame = np.array(signal)
        input("Done collecting the background frame. Press Enter to continue...")
        print("collecting data")
        timestamps = []
        sample_times = []

        for x in range(radar_frames):
            wlbt.Trigger()
            signal, t = wlbt.GetSignal(pairs[i])
            timestamps.append(time.time_ns())
            bscan_data[x,:] = signal

        name = f"static_plate_pair{i}_prof_sensor_narrow"
        # np.savetxt(name + "_bg.csv", np.transpose(bg_frame), delimiter = ",")
        np.savetxt(name + ".csv", np.transpose(bscan_data), delimiter = ",")
        np.savetxt(name + "_timestamps.csv", timestamps, delimiter = ",")



 

    ax = pyplot.subplot()

    im = ax.imshow(np.transpose(bscan_data))
    pyplot.title('static plate varying antennas')
    pyplot.ylabel('range bins')
    pyplot.xlabel('radar frame')
    # create an Axes on the right side of ax. The width of cax will be 5%
    # of ax and the padding between cax and ax will be fixed at 0.05 inch.
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)

    pyplot.colorbar(im, cax=cax)

    pyplot.show()
