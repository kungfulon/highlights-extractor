import sys
import numpy as np
from moviepy.editor import VideoFileClip, concatenate

clip = VideoFileClip(sys.argv[1])
cut = lambda i: clip.audio.subclip(i,i+1).to_soundarray(fps=22000) 
volume = lambda array: np.sqrt(((1.0*array)**2).mean())
volumes = [volume(cut(i)) for i in range(0,int(clip.audio.duration-2))]
averaged_volumes = np.array([sum(volumes[i:i+10])/10
                             for i in range(len(volumes)-10)])

increases = np.diff(averaged_volumes)[:-1]>=0
decreases = np.diff(averaged_volumes)[1:]<=0
peaks_times = (increases * decreases).nonzero()[0]
peaks_vols = averaged_volumes[peaks_times]
peaks_times = peaks_times[peaks_vols>np.percentile(peaks_vols,90)]

final_times=[peaks_times[0]]
for t in peaks_times:
    if (t - final_times[-1]) < 60:
        if averaged_volumes[t] > averaged_volumes[final_times[-1]]:
            final_times[-1] = t
    else:
        final_times.append(t)

final = concatenate([clip.subclip(max(t-20,0),min(t+20, clip.duration))
                     for t in final_times])
final.to_videofile(sys.argv[2])

