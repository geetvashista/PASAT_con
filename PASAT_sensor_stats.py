import numpy as np
import os
import pandas as pd
from scipy.stats import f_oneway

def get_data(base_path, char):
    rot_array = []
    for file in os.listdir(base_path):
        name = file.strip('_adj_matrix.npy')
        if name[1] == char:
            if '8' in name:
                rot_array.append(np.load(os.path.join(base_path, file)))
    return np.concatenate(rot_array, axis=0)

# def get_data(base_path, char):
#     rot_array = []
#     for file in os.listdir(base_path):
#         name = file.strip('_adj_matrix.npy')
#         if name[1] == char:
#             rot_array.append(np.load(os.path.join(base_path, file)))
#     return np.concatenate(rot_array, axis=0)


# Load data
base_path = '/home/students/Ddrive_2TB/Cornelius/results/Alpha' # This will determine your band

rot_list = ['1','2','3','4','5','6','7','8']
master_dir = []
for i in rot_list:
    master_dir.append(get_data(base_path=base_path, char=i))

mean_wpli = [np.mean(i, axis=-1) for i in master_dir]
# min_len = 778
# mean_wpli = [i[0:min_len, :] for i in mean_wpli]

r1 = mean_wpli[0]
r2 = mean_wpli[1]
r3 = mean_wpli[2]
r4 = mean_wpli[3]
r5 = mean_wpli[4]
r6 = mean_wpli[5]
r7 = mean_wpli[6]
r8 = mean_wpli[7]

_, p_val = f_oneway(r1, r2, r3, r4, r5, r6, r7, r8, axis=0)

# Getting ch_names if needed
import mne
epoch = mne.read_epochs('/home/students/Ddrive_2TB/Cornelius/Cleaned/2_Cleaned')
ch_names = epoch.ch_names
del epoch

target = []
for index, val in enumerate(list(p_val)):
    if val <= 0.05:
        target.append(index)
[print(ch_names[index]) for index in target]

def pli_direction(array):
    array = np.mean(array, axis=0)
    hold = []
    for index in target:
        hold.append(array[index])
    return np.array(hold)

result_1 = pli_direction(r1)
result_2 = pli_direction(r2)
result_3 = pli_direction(r3)
result_4 = pli_direction(r4)
result_5 = pli_direction(r5)
result_6 = pli_direction(r6)
result_7 = pli_direction(r7)
result_8 = pli_direction(r8)

df = pd.DataFrame({'1': result_1, '2':result_2, '3':result_3, '4':result_4, '5':result_5, '6':result_6, '7':result_7, '8': result_8})
df.to_excel('for_num8.xlsx')

