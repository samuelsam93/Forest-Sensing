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


def collect_data():
    # wlbt.Disconnect()
    # wlbt.Clean()
    wlbt.Init()
    wlbt.Initialize()
    print('initialized')
    wlbt.ConnectAny()
    configure()
    print('configured')
    #time.sleep(5)
    radar_frames = 256

    wlbt.Start()
    pairs = wlbt.GetAntennaPairs()
    print(pairs)
    selected_pair = 6
    print("collecting the background frame.")
    wlbt.Trigger()
    signal, t = wlbt.GetSignal(pairs[selected_pair])
    bg_frame = np.array(signal)
    input("Done collecting the background frame. Press Enter to continue...")

    # print("collecting wood frame 1")
    # wlbt.Trigger()
    # signal, t = wlbt.GetSignal(pairs[selected_pair])
    # wood_frame_1 = np.array(signal)
    # input("Done collecting the wood frame 1. Press Enter to continue...")

    # print("collecting wood frame 2")
    # wlbt.Trigger()
    # signal, t = wlbt.GetSignal(pairs[selected_pair])
    # wood_frame_2 = np.array(signal)
    # input("Done collecting the wood frame 2. Press Enter to continue...")

    # print("collecting the wood frame 3.")
    # wlbt.Trigger()
    # signal, t = wlbt.GetSignal(pairs[selected_pair])
    # wood_frame_3 = np.array(signal)
    # input("Done collecting wood frame 3. Press Enter to continue...")

    # print("collecting the wood frame 4.")
    # wlbt.Trigger()
    # signal, t = wlbt.GetSignal(pairs[selected_pair])
    # wood_frame_4 = np.array(signal)
    # input("Done collecting wood frame4. Press Enter to continue...")

    print("collecting data")
    bscan_data = np.zeros((radar_frames, len(signal)))
    timestamps = []
    sample_times = []

    np.savetxt("timestamps.csv", t, delimiter=",")
    np.savetxt("amplitudes.csv", signal, delimiter=",")

    for x in range(radar_frames):
        wlbt.Trigger()
        signal, t = wlbt.GetSignal(pairs[selected_pair])
        timestamps.append(time.time())
        bscan_data[x,:] = signal

    name = input("Name to save data under: ")
    # np.savetxt(name + "_bg.csv", np.transpose(bg_frame), delimiter = ",")
    np.savetxt(name + ".csv", np.transpose(bscan_data), delimiter = ",")
    np.savetxt(name + "_timestamps.csv", timestamps, delimiter = ",")
    # np.savetxt(name + "wood_frame_30cm.csv", np.transpose(bg_frame), delimiter = ",")
    # np.savetxt(name + "wood_frame_40cm.csv", np.transpose(bg_frame), delimiter = ",")
    # np.savetxt(name + "wood_frame_50cm.csv", np.transpose(bg_frame), delimiter = ",")
    # np.savetxt(name + "wood_frame_60cm.csv", np.transpose(bg_frame), delimiter = ",")

    ax = pyplot.subplot()

    im = ax.imshow(np.transpose(bscan_data-bg_frame), extent=[0, 512, 1200, 0], aspect='auto')
    pyplot.title(name)
    pyplot.ylabel('range bins (cm)')
    pyplot.xlabel('radar frame')
    pyplot.ylim(300, 0)
    # create an Axes on the right side of ax. The width of cax will be 5%
    # of ax and the padding between cax and ax will be fixed at 0.05 inch.
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)

    pyplot.colorbar(im, cax=cax)

    pyplot.show()
    print('end')

def collect_wood_data():
    # wlbt.Disconnect()
    # wlbt.Clean()
    wlbt.Init()
    wlbt.Initialize()
    print('initialized')
    wlbt.ConnectAny()
    configure()
    print('configured')
    #time.sleep(5)
    radar_frames = 10

    wlbt.Start()
    pairs = wlbt.GetAntennaPairs()
    print(pairs)
    selected_pair = 6
    wlbt.Trigger()
    signal, t = wlbt.GetSignal(pairs[selected_pair])
    
    for x in range(1):
        name = input("Enter name of file: ")
        input("Press Enter to collect radar frames with wood.")
        
        frames = np.zeros((radar_frames, len(signal)))
        for i in range(radar_frames):
            wlbt.Trigger()
            signal, t = wlbt.GetSignal(pairs[selected_pair])
            frame = np.array(signal)    
            frames[i,:] = frame
        np.savetxt(name + ".csv", np.transpose(frames), delimiter = ",")
        input("Done collecting the radar frames. Press Enter to collect the background frames.")
        
        bg_frames = np.zeros((radar_frames, len(signal)))
        for i in range(radar_frames):
            wlbt.Trigger()
            signal, t = wlbt.GetSignal(pairs[selected_pair])
            frame = np.array(signal)
            bg_frames[i,:] = frame
        np.savetxt(name + "_bg.csv", np.transpose(bg_frames), delimiter = ",")
        input("Done collecting the background frames. Press Enter to continue.")
   


if __name__ == "__main__":
    collect_data()  
    # collect_wood_data()
