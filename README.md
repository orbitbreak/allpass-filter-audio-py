Allpass filter impl in python

Script creates a white noise sample and applies a high-pass filter, outputting pre and post to wav files

NOTES:

 - Allpass impl is computationally cheap vs traditional high/low-pass filter design, since only one filter coeff needs to be recalculated on cutoff freq changes

 - Freq-dependent delay out of phase, no direct gain changes

 - Higher freq => more phase delay

 - Subtract allpass output (-phase) from input for final output
