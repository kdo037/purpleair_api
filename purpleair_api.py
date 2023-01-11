#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 11:36:22 2023

@author: khanh
MIT license
"""

from purpleair import PurpleAir
import datetime
import csv
import numpy as np

########################## BEGIN MODIFY SECTION ##################################

# Modify sensor names
sensor_names = ["A outdoor", "B outdoor", "B indoor", "C outdoor",
                "D outdoor", "E outdoor"]
# Modify sensor index
sensor_idx = [82349, 54769, 51449, 131025, 
              47493, 47615]
# Modify sensor read api key
p = PurpleAir('Your API Read Key Here')
# Modify field names which can get from p.get_sensor_data(91695)['sensor']
field_names = 'humidity,humidity_a,temperature,temperature_a,pressure,pressure_a,analog_input,\
pm2.5_alt,pm2.5_alt_a,pm2.5_alt_b,\
scattering_coefficient,scattering_coefficient_a,scattering_coefficient_b'
# Modify start and end time
start_time = datetime.datetime(year=2022, month=7, day=20)
end_time = datetime.datetime(year=2022, month=7, day=24)

########################## END MODIFY SECTION ####################################
    
for participant in range(0, len(sensor_names)):
    count = 0
    data = []
    starttime = start_time
    while starttime <= end_time:
        try:
            data_temp = p.get_sensor_history_csv(sensor_index=sensor_idx[participant], fields=(field_names ), 
                                                 start_timestamp=starttime, end_timestamp=starttime + datetime.timedelta(days=1))
        except ValueError:
            data_temp = p.get_sensor_history_csv(sensor_index=sensor_idx[participant], fields=(field_names, ), 
                                                 start_timestamp=starttime, end_timestamp=starttime + datetime.timedelta(days=1))
        
        # find the index end with \n
        new_line = data_temp.find('\n')
        
        if count == 0:
            data = data_temp
            count = 1
            print('Purpleair: ', participant)
        else:
            data = data + data_temp[(new_line+1):-1]
        print(starttime)
        
        # increase by 1 day
        starttime = starttime + datetime.timedelta(days=1)
        
    f = open(sensor_names[participant]+"_data.csv", "a")
    f.write(data)
    f.close()
    
    # read written csv to sort and convert timestamp
    with open(sensor_names[participant]+"_data.csv", 'r', encoding = 'utf-8', errors = 'ignore') as readFile:
        reader = csv.reader(readFile)
        lines = list(reader)
    
    timestamp = []
    for i in range(1, len(lines)):
        timestamp.append(int(lines[i][0]))
    
    # sort the timestamp
    sort_idx = np.argsort(timestamp)
    
    # write back to file with sort and converted timestamp
    f = open(sensor_names[participant]+"_sort.csv", "a")
    f.write('Datetime' + ',')
    for j in range(0, len(lines[0])):
        f.write(lines[0][j] + ',')
    f.write('\n')
    
    for i in range(0, len(lines)-1):
        # convert timestampe to datetime
        f.write(str(datetime.datetime.fromtimestamp(timestamp[sort_idx[i]]))+ ',')
        for j in range(0, len(lines[0])):
            f.write(lines[sort_idx[i]+1][j] + ',')
        f.write('\n')
    f.close()
    starttime = start_time

























































#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 16:51:44 2023

@author: khanh
"""

