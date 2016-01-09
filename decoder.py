"""
Source code originates from the `decoder.ipynb` notebook with very little cleanup.
"""

import numpy as np

from collections import namedtuple
from collections import Counter
from itertools import chain
from sys import argv


csv = np.genfromtxt(argv[1], delimiter=',', skip_header=2, usecols=(0, 1))
csv = np.transpose(csv)
time = csv[0] * 1000  # time in ms
voltage = csv[1]

digital_one = np.percentile(voltage, 90)
digital_stream = voltage / digital_one
digital_stream = digital_stream.round().astype(int)

number_of_data_points = len(digital_stream)
first_capture_time = time[0]
last_capture_time = time[-1]
total_capture_duration = last_capture_time - first_capture_time

single_data_point_duration = total_capture_duration / (number_of_data_points - 1) * 1000

Signal = namedtuple('Signal', ['high', 'duration'])
HIGH = 1

signals = []

first = True
previous = None
duration = None
last_index = len(digital_stream) - 1
for i, x in enumerate(digital_stream):
    if first:
        first = False
        previous = x
        duration = 1
        continue;

    if i == last_index or x != previous:
        high = previous == HIGH
        s = Signal(high=high, duration=duration)
        signals.append(s)

        previous = x
        duration = 1
    else:
        duration += 1

signal_pairs = []
first = None
for index, s in enumerate(signals):
    if index == 0 and s.high != True:
        # If the data begins with a low signal, drop it.
        continue;

    if first == None:
        first = s
    else:
        signal_pairs.append((first, s))
        first = None

pair_durations = [pair[0].duration + pair[1].duration for pair in signal_pairs]

c = Counter(pair_durations)
signal_pair_duration = c.most_common()[0][0]

separator_limit = signal_pair_duration * 2

messages = []
message = []
last_pair_index = len(signal_pairs) - 1
for i, sp in enumerate(signal_pairs):

    # Detect separating signal
    high, low = sp
    is_separating_signal = low.duration > separator_limit

    # Normalize separating signals:
    # The signal that is closes to the most common signal pair duration is the reliable one of the pair.
    distance_to_high = abs(signal_pair_duration - high.duration)
    distance_to_low = abs(signal_pair_duration - low.duration)
    if distance_to_high < distance_to_low:
        # The high signal is the reliable one
        new_low = low._replace(duration=signal_pair_duration - high.duration)
        message.append((high, new_low))
    else:
        # The low signal is the reliable one
        new_high = high._replace(duration=signal_pair_duration - low.duration)
        message.append((new_high, low))

    if i == last_pair_index or is_separating_signal:
        messages.append(message)
        message = []

bit_messages = []
for message in messages:
    bit_message = []
    for high, low in message:
        bit = high.duration > low.duration
        bit_message.append(bit)
    bit_messages.append(bit_message)

for m in bit_messages:
    msg = ''
    for b in m:
        msg += '1' if b else '0'
    print msg
