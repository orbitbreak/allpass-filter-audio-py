from pathlib import Path
import numpy as np
import soundfile as sf
from scipy import signal

def generate_white_noise( duration_secs, sample_rate ):
    duration_samples = int( duration_secs * sample_rate )
    return np.random.default_rng().uniform( -1, 1, duration_samples )

def a1_coefficient( freq_break, sample_rate ):
    tan = np.tan( np.pi * freq_break / sample_rate )
    return ( tan-1 )/( tan+1 )

def allpass_filter( signal_in, freq_break, sample_rate ):
    allpass_result = np.zeros_like( signal_in ) # output init
    buffer_singlesamplediff = 0  # buffer for single sample
    for n in range( signal_in.shape[0] ):
        a1 = a1_coefficient( freq_break[n], sample_rate ) # allpass coeff calc for each sample
        allpass_result[n] = a1 * signal_in[n] + buffer_singlesamplediff # allpass difference formula
        buffer_singlesamplediff = signal_in[n] - a1 * allpass_result[n] # save to buffer for next iter
    return allpass_result

def allpass_based_filter(signal_in, freq_cutoff, sample_rate, highpass=False, amplitude=1.0):
    allpass_output = allpass_filter( signal_in, freq_cutoff, sample_rate ) # do allpass filter
    if highpass:
        allpass_output *= -1 # for highpass, invert phase
    filter_output = signal_in + allpass_output # direct + output summing
    filter_output *= 0.5 # clipping protection
    filter_output *= amplitude # apply given amplitude
    return filter_output


sample_rate = 44100
duration_secs = 5

prefile_out='white_UNFILTERED.wav'
print("Generating white noise to filename: {}".format( prefile_out ))
white_noise = generate_white_noise(duration_secs, sample_rate) # 5 seconds of white noise
signal_in = white_noise

sf.write(prefile_out, signal_in * 0.1, sample_rate)

freq_cutoff = np.geomspace(20000, 20, signal_in.shape[0]) # cutoff freq decays with time

postfile_out='white_FILTERED.wav'
print("Generating high-pass filtered white noise to filename: {}".format( postfile_out ))
filter_output = allpass_based_filter( signal_in, freq_cutoff, sample_rate, highpass=False, amplitude=0.1)

sf.write(postfile_out, filter_output, sample_rate)


