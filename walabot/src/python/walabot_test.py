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
    print(f'num_pairs: {len(pairs)}')
    selected_pair = 0
    num_pairs = 2
    # num_pairs = len(pairs)

    wlbt.Trigger()
    signal, t = wlbt.GetSignal(pairs[0])

    bscan_data = np.zeros((num_pairs*radar_frames, len(signal)))

    for i in range(num_pairs):
        print("collecting the background frame.")
        wlbt.Trigger()
        bg_signal, t = wlbt.GetSignal(pairs[i])
        bg_frame = np.array(bg_signal)
        input("Done collecting the background frame. Press Enter to continue...")
        print("collecting data")
        timestamps = []
        sample_times = []

        for x in range(radar_frames):
            wlbt.Trigger()
            signal, t = wlbt.GetSignal(pairs[i])
            data_signal = np.array(signal) - bg_frame
            timestamps.append(time.time_ns())
            bscan_data[i*radar_frames+x,:] = data_signal
        input('done collecting. reset antenna to connect next background frame, then press ENTER')

    name = "sam_testing"
    np.savetxt(name + "_bg.csv", np.transpose(bg_frame), delimiter = ",")
    np.savetxt(name + "_bg_subtracted.csv", np.transpose(bscan_data), delimiter = ",")
    np.savetxt(name + "_timestamps.csv", timestamps, delimiter = ",")

    ax = pyplot.subplot()

    im = ax.imshow(np.transpose(bscan_data), extent=[0, radar_frames*num_pairs, 1200, 0])
    pyplot.title('horizontal walabot and rotating metal plate')
    pyplot.ylabel('range bins')
    pyplot.xlabel('radar frame')
    # create an Axes on the right side of ax. The width of cax will be 5%
    # of ax and the padding between cax and ax will be fixed at 0.05 inch.
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)

    pyplot.colorbar(im, cax=cax)

    pyplot.show()
    print('end')





# import WalabotAPI as wlbt
# import pprint as pp
# import matplotlib.pyplot as pyplot
# from mpl_toolkits.axes_grid1 import make_axes_locatable
# import numpy as np 
# import time 


# def configure():
#     # wlbt.SetProfile(wlbt.PROF_SENSOR)
#     wlbt.SetProfile(wlbt.PROF_SENSOR_NARROW)
#     # wlbt.SetProfile(wlbt.PROF_SHORT_RANGE_SINGLE_LINE)
#     # wlbt.SetProfile(wlbt.PROF_SHORT_RANGE_IMAGING)

#     wlbt.SetDynamicImageFilter(wlbt.FILTER_TYPE_NONE)
#     # wlbt.SetDynamicImageFilter(wlbt.FILTER_TYPE_MTI)
#     # wlbt.SetDynamicImageFilter(wlbt.FILTER_TYPE_DERIVATIVE)




# if __name__ == "__main__":
#     # wlbt.Disconnect()
#     # wlbt.Clean()
#     wlbt.Init()
#     wlbt.Initialize()
#     print('initialized')
#     wlbt.ConnectAny()
#     configure()
#     print('configured')
#     #time.sleep(5)
#     radar_frames = 100

#     wlbt.Start()
#     pairs = wlbt.GetAntennaPairs()
#     print(pairs)
#     selected_pair = 6
#     print("getting signal size")
#     wlbt.Trigger()
#     signal, t = wlbt.GetSignal(pairs[selected_pair])
#     bg_frame = np.zeros((len(pairs)*radar_frames, len(signal)))
#     bscan_data = np.zeros((len(pairs)*radar_frames, len(signal)))
#     timestamps = []
#     sample_times = []

#     for i in range(len(pairs)):
#         print(f"collecting the background frame {i}")
#         wlbt.Trigger()
#         signal, t = wlbt.GetSignal(pairs[i])
#         bg_frame[radar_frames*i:radar_frames*i+99, :] = signal

#     ax = pyplot.subplot()
#     im = ax.imshow(np.transpose(bg_frame))
#     pyplot.show()

#     input("Done collecting the background frame. Press Enter to continue...")
#     print("collecting data")

#     for i in range(len(pairs)):
#         print(i)
#         for x in range(radar_frames):
#             wlbt.Trigger()
#             signal, t = wlbt.GetSignal(pairs[i])
#             timestamps.append(time.time_ns())
#             bscan_data[i*radar_frames+x,:] = signal

#     name = "sam_testing"
#     np.savetxt(name + "_bg.csv", np.transpose(bg_frame), delimiter = ",")
#     np.savetxt(name + ".csv", np.transpose(bscan_data), delimiter = ",")
#     np.savetxt(name + "_timestamps.csv", timestamps, delimiter = ",")

#     ax = pyplot.subplot()

#     im = ax.imshow(np.transpose(bscan_data-bg_frame), aspect='equal', extent=[0, radar_frames*len(pairs), 1200, 0])
#     pyplot.title('horizontal walabot and rotating metal plate')
#     pyplot.ylabel('range bins')
#     pyplot.xlabel('radar frame')
#     # create an Axes on the right side of ax. The width of cax will be 5%
#     # of ax and the padding between cax and ax will be fixed at 0.05 inch.
#     divider = make_axes_locatable(ax)
#     cax = divider.append_axes("right", size="5%", pad=0.05)

#     pyplot.colorbar(im, cax=cax)

#     pyplot.show()
#     print('end')
