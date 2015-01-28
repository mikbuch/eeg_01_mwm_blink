#!/usr/bin/env python

import csv
import matplotlib.pyplot as plt
import os.path

fs=512

input_csv_categ = '../csv_eeg_ann/eeg_categ.csv' 
input_categorized_blink = '../csv_eeg_ann/categorized_blink'
output_eeg_blink_scilab = '../csv_eeg_ann/scilab_eeg_01_sub.csv'

eeg_microvolts=[]
stimulus = []
blink_category = []
blink_time = []
blink_decision = []
blink_categorization = []

eeg_sti_blk = []

if os.path.isfile(output_eeg_blink_scilab):
    os.remove(output_eeg_blink_scilab)

################################################################
#    READING EEG EEG_CATEG.CSV FOR THE SIGNAL AND THE STIMULUS #
################################################################
with open(input_csv_categ, 'r') as f:
    rows = list(csv.reader(f))
    for i in range(len(rows)):
        eeg_microvolts.append(rows[i][0])
        stimulus.append(rows[i][1])

################################################################
#     READING CATEG EEG_BLINK_CATEGORIZED                      #
################################################################
    with open(input_categorized_blink) as f:
        lines = f.read().splitlines()

    j = 0
    for i in range(len(lines)):
        j+=1
        if j==3:
            blink_category.append([\
                    [int(lines[i-2]),int(lines[i-1])],\
                    float(lines[i])\
                    ])
            j = 0 
                
    blink_category = sorted(blink_category)

    j = 0
    k = 0

    for i in blink_category:
        if i[-1] < 0:
            for j in range(int(i[0][1]-i[0][0])+1):
                blink_categorization.append(0)
                k += 1
        else:
            for j in range(int(i[0][1]-i[0][0])+1):
                k += 1
                if j < int(i[0][1]-i[0][0])-1:
                    blink_categorization.append(round(i[1])*6)
                if j == int(i[0][1]-i[0][0])-1:
                    blink_categorization.append(0)
                if j == int(i[0][1]-i[0][0]):
                    blink_categorization.append(0)
    for i in range(127):
        blink_categorization.append(0)

################################################################
#    CORECTNESS                                               #
################################################################
stimulus_ranges= []
for i in range(len(stimulus)):
    if not i == 0 and not i > len(stimulus)-2:
        if stimulus[i] < stimulus[i+1]:
            stimulus_ranges.append([])
            stimulus_ranges[-1].append(i)
        if stimulus[i] > stimulus[i+1]:
            stimulus_ranges[-1].append(i)
            stimulus_ranges[-1].append(i-stimulus_ranges[-1][0])
print('\n') 

for i in range(len(eeg_microvolts)):
    eeg_sti_blk.append([])
    eeg_sti_blk[i].append(eeg_microvolts[i])
    eeg_sti_blk[i].append(stimulus[i])
    if i > len(blink_categorization)-1:
        eeg_sti_blk[i].append(0)
    else:
        eeg_sti_blk[i].append(blink_categorization[i])

categorization = 0 
sti_and_blk = 0
categorization_ranges = []
blink_reality = 0
blink_miscateg = 0
packages_for_blink_global = 4
j = 0


# FIRST STEP: check wether it is in the stimulus or not

for i in range(len(eeg_sti_blk)):
    if eeg_sti_blk[i][2] > 0 and not i == len(eeg_sti_blk):
        if int(eeg_sti_blk[i][1]) > 0:
            j += 1
        categorization += 1
        if categorization == 1:
            categorization_ranges.append([])
            categorization_ranges[-1].append(i)
        if eeg_sti_blk[i+1][2] == 0:
            categorization_ranges[-1].append(i+1)
            categorization_ranges[-1].append(\
                    i+1-categorization_ranges[-1][0])
            categorization = 0
            if j > 0: 
                categorization_ranges[-1].insert(0, 1)
                j = 0
            else:
                categorization_ranges[-1].insert(0, 0)


# SECOND STEP: check if it is a correct blink categorization or not

packages_for_blink = packages_for_blink_global
for i in range(len(categorization_ranges)):
    if len(categorization_ranges)-1 - i <= packages_for_blink:
        packages_for_blink = len(categorization_ranges)-1 - i
    if categorization_ranges[i][0] == 1:
        if i == 0:
            blink_reality += 1
            categorization_ranges[i].insert(1, blink_reality)
            for j in range(packages_for_blink):
                if categorization_ranges[i+j+1][1]\
                   - categorization_ranges[i][2] \
                   < (categorization_ranges[i][4]+2) * packages_for_blink:
                    categorization_ranges[i+j+1].insert(1, blink_reality)
        else:
            if len(categorization_ranges[i-1]) \
            != len(categorization_ranges[i]) \
              and categorization_ranges[i][1] \
              != categorization_ranges[i-1][1]: 
                blink_reality += 1
                categorization_ranges[i].insert(1, blink_reality)
                if i == len(categorization_ranges)-2:
                    if categorization_ranges[i+1][1]\
                       - categorization_ranges[i][3] \
                       < (categorization_ranges[i][4] + 2) \
                         * (packages_for_blink+3):
                         print('inserting')
                         categorization_ranges[i+1]. \
                           insert(1, blink_reality)
                else:
                    for j in range(packages_for_blink):
                        if categorization_ranges[i+j+1][1]\
                           - categorization_ranges[i][2] \
                           < (categorization_ranges[i][4]+2) \
                             * packages_for_blink:
                             categorization_ranges[i+j+1]. \
                               insert(1, blink_reality)
    else:
        if i == 0:
            categorization_ranges[i].insert(1, 0)
        else:
            if len(categorization_ranges[i-1]) \
            != len(categorization_ranges[i]):
                categorization_ranges[i].insert(1, 0)


print(' ' + 44*'#')
print(' ' + '#    ' + 'categorization_ranges')
print(' ' + 32*'#')
j = 0
for i in categorization_ranges:
    j += 1
    print(' ' + '#    ' + '{0:02}'.format(j) + ' ' + str(i))
print(' ' + 44*'#')

print('\n')

# THIRD STEP: define wrong catogorization
# split blink categorization into proper and wrong ones

blink_correct = []
blink_incorrect = []
blink_incorrect_reality = 0
packages_for_blink = packages_for_blink_global

for i in categorization_ranges:
    if i[0] == 0 and i[1] == 0:
        blink_incorrect.append(i)
    if i[1] != 0:
        blink_correct.append(i)

for i in range(len(blink_incorrect)):
    if len(blink_incorrect)-1 - i < packages_for_blink:
        packages_for_blink =  len(blink_incorrect)-1 - i
    if blink_incorrect[i][0] == 0 and blink_incorrect[i][1] == 0:
        blink_incorrect_reality += 1
        blink_incorrect[i][1] = blink_incorrect_reality
        for j in range(packages_for_blink):
            if blink_incorrect[i+1+j][3] - blink_incorrect[i][2] < \
            (blink_incorrect[i][4] + 2) * packages_for_blink_global:
                blink_incorrect[i+1+j][1] = blink_incorrect_reality


################################################################
#     PRINTING FOR DEBUG                                       #
################################################################
def info_blinks_printing():
#     print('\n')
#     print(' ' + 44*'#')
#     print(' ' + '#    ' + 'categorization_ranges')
#     print(' ' + 32*'#')
#     j = 0
#     for i in categorization_ranges:
#         j += 1
#         print(' ' + '#    ' + '{0:02}'.format(j) + ' ' + str(i))
#     print(' ' + 44*'#')

    print('\n')
    print(' ' + 44*'#')
    print(' ' + '#    ' + 'blink_correct')
    print(' ' + 32*'#')
    j = 0
    for i in blink_correct:
        j += 1
        print(' ' + '#    ' + '{0:02}'.format(j) + ' ' + str(i))
    print(' ' + 44*'#')

    print('\n')
    print(' ' + 44*'#')
    print(' ' + '#    ' + 'blink_incorrect')
    print(' ' + 32*'#')
    j = 0
    for i in blink_incorrect:
        j += 1
        print(' ' + '#    ' + '{0:02}'.format(j) + ' ' + str(i))
    print(' ' + 44*'#')
    print('\n')
    print('{0:02}'.format(blink_reality) + ' blinks_categorized_correctly')
    print('{0:02}'.format(blink_incorrect_reality) + ' blinks_categorized_incorrectly')

def info_files_and_lists_printing():
    input_lines_eeg = sum(1 for line in open(input_csv_categ))
    input_lines_categ = sum(1 for line in open(input_categorized_blink))
    print('')
    print('--------------------------------------------------')
    print('eeg_file lines: ....... ' + str(input_lines_eeg))
    print('categ_file lines: ..... ' + str(input_lines_categ))
    print('categ_file samples : .. ' + str(input_lines_categ/float(3)*128))
    print('--------------------------------------------------')
    print('')
    print('--------------------------------------------------')
    print('length of eeg: ........ ' + str(len(eeg_microvolts)))
    print('seconds of eeg: ....... ' + str(len(eeg_microvolts)/float(512)))
    print('--------------------------------------------------')
    print('length of stimulus: ... ' + str(len(stimulus)))
    print('seconds of stimulus: .. ' + str(len(stimulus)/float(512)))
    print('--------------------------------------------------')
    print('len(blink_category): .. ' + str(len(blink_category)))
    print('length of categoriz: .. ' + str(len(blink_categorization)))
    print('--------------------------------------------------')

info_blinks_printing()
info_files_and_lists_printing()

################################################################
#     WRITING CSV FOR THE FURTHER SCILAB PLOT GENERATION       #
################################################################

for i in range(len(eeg_microvolts)):
    f = open(output_eeg_blink_scilab,'a')
    f.write('%s, %s, %f\n' \
          %(eeg_microvolts[i], stimulus[i], blink_categorization[i]))
    f.close()

################################################################
#     PLOTTING DATA                                            #
################################################################

plt.plot(eeg_microvolts, color='b')
plt.plot(stimulus, color='k',linewidth=2.0)
plt.plot(blink_categorization, color='r',linewidth=1.0)
plt.xlabel('sample number (512 samples per second)')
plt.ylabel('amplitude (micro Volts)')
plt.show()
