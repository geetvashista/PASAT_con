import mne
import numpy as np
import os
import mne_connectivity
import time
import dyconnmap
start = time.time()

# Load data
base_dir = r'F:\PASAT\Cleaned'

master_epochs = []
for file in os.listdir(base_dir):
    master_epochs.append(mne.read_epochs(os.path.join(base_dir, file)))

# get events list
events_list = master_epochs[0].event_id
events_list = list(events_list.keys())

# Get data by event id
epochs_by_id = []
for event_id in events_list:
    temp = []
    for participant in master_epochs:
        epoch = participant
        data = epoch[event_id]
        temp.append(data)
    epochs_by_id.append(temp)


# org data
data_for_conn = []
for event_type in epochs_by_id:
    temp = []
    for i in event_type:
        data = i.get_data()
        temp.append(data)
    data_for_conn.append(np.concatenate(temp, axis=0))


# Connectivity
freqs = (5, 10)

# wpli calculator

def wpli_conn(array, target_fb, fs):   # Assumed shape (roi's, time_points)
    print('calculating connectivity')
    _, _, filtered_array = dyconnmap.analytic_signal(array, fb=target_fb, fs=fs)
    return dyconnmap.fc.wpli(filtered_array, fs=fs, fb=target_fb)



conn_master_data = []
for event in data_for_conn:
    event_master = []
    for epoch in event:
        event_master.append(wpli_conn(epoch, target_fb=[4, 7.], fs=250))
        conn_master_data.append(event_master)


print('\n' + "EXECUTION TIME: " + str(time.time()-start))


# conn_master_data = []
# for event in data_for_conn:
#     print('starting event')
#     conn_master_data.append(mne_connectivity.spectral_connectivity_time(event,
#                                                           freqs=freqs,
#                                                           method='wpli',
#                                                           mode='multitaper',
#                                                           fmin=(4., 8.),
#                                                           fmax=(7., 12.),
#                                                           sfreq=250,
#                                                           average=False))
#     print('event complete')
#
# print('\n' + "EXECUTION TIME: " + str(time.time()-start))




