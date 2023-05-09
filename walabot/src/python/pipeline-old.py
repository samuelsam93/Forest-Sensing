import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable


class pipeline:
    
    def __init__():
        
        self.finalVal = 0
        self.selR = 0
        self.normR2 = None

    def detect_tag(self, bscan_data, timestamps, from_, to, Tau, switchPer, plotTitle):    
        bins, numCols = bscan_data.shape
        NFFTVel = 512  # fft bin number
        modDuty = 50  # duty cycle
        modF = 1./(2*(switchPer))  # tag modulation frequency
        FrmMeasSiz = numCols  # size of the the vector
        
        expDopFinal = np.zeros((1, NFFTVel))
        sq_wav = np.squeeze(np.array([np.square(2 * np.pi * modF * timestamps[i], modDuty)
                                      for i in range(len(timestamps))]))
        expdopt = np.abs(np.fft.fft(sq_wav, NFFTVel, axis=0))  # sinc function of the modulation
        
        t = timestamps[0]
        dur = np.ceil(timestamps[-1] - timestamps[0])
        T = np.zeros((int(dur), 1))
        i = 0
        while t < timestamps[-1]:
            a = np.logical_and(t > timestamps, t <= (timestamps + 1.0))
            T[i] = np.sum(a)
            t += 1.0
            i += 1
        T = T[1:, :]
        fps = np.mean(T)
        
        tau = Tau / bins
        tof = np.arange(from_, to+1) * tau

        tagFFT = round(((1 / fps) * NFFTVel) * modF)  # the first fft bin that tag sinc harmonic shows up
        ind = np.arange(1, round(NFFTVel / (tagFFT * 2)), 2)  # finding the harmonic of the tag based on the modulation frequency
        
        # only keep the harmonics of the sync function in the template
        fInd = tagFFT * ind + 1
        fIndL = NFFTVel - tagFFT * ind + 1
        ffInd = np.unique(np.concatenate([fInd, fIndL]))
        ffInd = ffInd[(ffInd < NFFTVel) & (ffInd > 1)]
        expDopFinal[:, ffInd] = expdopt[:, ffInd]
        
        # normalize the template
        expDopFinal = (expDopFinal - np.min(expDopFinal)) / (np.max(expDopFinal) - np.min(expDopFinal))

        H = np.fft.fft(bscan_data[from_:to+1, :], NFFTVel, axis=1)
        # plt.imshow(np.abs(H), aspect='auto')
        # plt.show()

        # normalize the signal
        sig = np.abs(H)
        normA = sig - np.min(sig)
        normSig = normA / np.max(normA)

        # calculate the autocorrelation
        normR2 = np.abs(np.sum(normSig * np.tile(expDopFinal, (normSig.shape[0], 1)), axis=1))
        # the autocorrelation results
        plt.plot(tof*15, normR2)
        plt.title(plotTitle + " correlation")
        plt.xlabel("Range (cm)")
        plt.show()

        # selR hold the range bin with max correlation
        self.finalVal = np.max(normR2)
        self.selR = np.argmax(normR2)
        self.normR2 = normR2


if __name__ == "__main__":
    # p = pipeline()

    bscan_data = np.genfromtxt('43cm_tag_1s.csv', delimiter=',')
    bg_frame = np.genfromtxt('43cm_tag_1s_bg.csv')
    t = np.genfromtxt('timestamps.csv', delimiter=',')
    bscan_data = bscan_data - np.transpose(bg_frame)
    # define the necessary input arguments
    from_ = 0
    to = 1300
    Tau = 1
    switchPer = 1
    plotTitle = " 43cm tag 1 s tag"
    
    ax = plt.subplot()
    #bscan_data = np.fft(bscan_data)
    im = ax.imshow(bscan_data, extent=[0, 512, 12000, 0])
    plt.ylim(1400, 1000)
    plt.title('43cm tag from radar')
    plt.ylabel('mm (from radar)')
    plt.xlabel('radar frame')

    # ax.set_yticks([0, 2048, 4095], [0.0, 600.0, 1200.0])
    # create an Axes on the right side of ax. The width of cax will be 5%
    # of ax and the padding between cax and ax will be fixed at 0.05 inch.
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)

    plt.colorbar(im, cax=cax)

    plt.show()

    # call the detect_tag method
    # p.detect_tag(bscan_data, t, from_, to, Tau, switchPer, plotTitle)

