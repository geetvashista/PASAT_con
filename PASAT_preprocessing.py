import mne_bids
import numpy as np
import matplotlib.pyplot as plt
import mne

# Setting some backend perameters
plt.matplotlib.use('Qt5Agg')

# Set variables
# Bids directory for all subjects and epoch start - stop times

BIDS_data_path = r'C:\Users\em17531\Desktop\BIDS'
Task = 'PASAT'

tmin, tmax = (0, 1)

subject_ids = []  # Fill in all participant numbers to complete here

# Functions we need done:

Preprocessing = True

# define the pre_processor function
def pre_processor(subject_ids, BIDS_data_path):
    # Load data

    bids_path = mne_bids.BIDSPath(subject=str(subject_ids),
                                  task=Task,
                                  root=BIDS_data_path)

    raw_BIDS = mne_bids.read_raw_bids(bids_path)
    raw_BIDS.load_data()

    # Mark bad channels and annotate here
    raw_BIDS.plot(block=True, title=str(subject_ids))

    # Notch filter (50 Hz)
    raw_notch = raw_BIDS.copy().notch_filter(np.arange(50, 500, 50))

    # high pass filter set to 1 Hz (to 100 Hz)
    raw_filtered = raw_notch.copy().filter(l_freq=1, h_freq=100)

    # Virtual reference (average referencing here)
    raw_avg_ref = raw_filtered.copy().set_eeg_reference(projection=True)
    raw_avg_ref.apply_proj()

    # downsample data from to 250 Hz
    raw_downsampled = raw_avg_ref.resample(250, npad="auto")

    # del raw
    del raw_notch
    del raw_filtered

    # Independent Components Analysis (ICA) for artifact removal
    ica = mne.preprocessing.ICA(n_components=32, random_state=0)
    ica.fit(raw_downsampled)
    ica.plot_sources(raw_downsampled, block=True, title=str(subject_ids))
    ica.plot_components(title=str(subject_ids))

    raw_ica = ica.apply(raw_downsampled.copy())
    raw_ica.plot(block=True, title=str(subject_ids))

    # Assign events
    events = mne.events_from_annotations(raw_ica)

    # Interpolation of bad channels
    raw_interp = raw_ica.interpolate_bads(reset_bads=True)

    # epoch data
    picks = mne.pick_types(raw_interp.info, meg=False, eeg=True, stim=False, eog=False, exclude='bads')
    epochs_org = mne.Epochs(raw_interp,
                            events=events[0],
                            event_id=events[1],
                            proj=False,
                            picks=picks,
                            baseline=None,
                            preload=True,
                            tmin=tmin,
                            tmax=tmax)

    epochs_org.drop_channels(['F11', 'F12', 'FT11', 'FT12', 'CB1', 'CB2'])

    # Saving clean epochs
    epochs_org.save(str(subject_ids) + '_Cleaned')


# Calling requested functions

if Preprocessing:
    for i in subject_ids:
        pre_processor(i, BIDS_data_path)
