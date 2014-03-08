# Script written by Donovan Bartish aka DRockstar
# These are global settings to assign controller cc numbers, etc
NUM_TRACKS = 8
NUM_SCENES = 1
GLOBAL_CHANNEL = 15
ENCODER_CC = [33, 34, 35, 36, 37, 38, 39, 40]
# Transport: Stop, Play, Rewind, Fast Forward, Loop, Record
TRANSPORT_CC = [116, 117, 114, 115, 113, 118, 60]
# Minus one pad to account for shift button
PAD_CC = [99, 100, 101, 102, 98, 61, 59] 
SHIFT_CC = 58
'''
ENCODER_MODES:
0: absolute
1: absolute_14_bit
2: relative_binary_offset
3: relative_signed_bit
4: relative_signed_bit2
5: relative_smooth_binary_offset
6: relative_smooth_signed_bit
7: relative_smooth_signed_bit2
8: relative_smooth_two_compliment
9: relative_two_compliment
'''
ENCODER_MODE = 5
# Drum Pad Note Numbers
DRUMPAD_NOTES = [36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51]
