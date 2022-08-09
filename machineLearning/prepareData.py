import pandas as pd
import math 

#include 5 ips in traceroute
number_of_data = 5

#function returns a list of each byte of the last 5 ips in a list
def parse_traceroute(traceroute):
    ips = []

    #go through each ip in the traceroute, ignore stars or empty strings
    for i in range(len(traceroute)):
        if traceroute[i] == '*' or traceroute[i] == '':
            continue
        else:
            ips.append(traceroute[i])

    #make sure there are at least 5 ips in each traceroute
    if(len(ips) < number_of_data):
        return 'ERROR'

    #go through each of the last 5 ips in data set
    numbers=[]
    for ip in ips[-number_of_data:]:
        ip = ip.split('.')
        #split ips into a list, remove empty strings and append to list
        for num in ip:
            if num == '':
                return 'ERROR'
            else:
                num = int(num)
                numbers.append(num)

    #return list of all bytes of the last 5 ips
    return numbers

#function returns the last 5 delays in delay 
def parse_delay(delay):
    delays = []
    #go through each delay in set, remove stars or empty strings
    for i in range(len(delay)):
        if delay[i] == '*' or delay[i] == '':
            continue
        else:
            delays.append(delay[i])
    #make sure there are at least 5 delays in each set
    if len(delays)<number_of_data:
        return 'ERROR'
    
    #return last 5 delays
    return delays[-number_of_data:]
     
#function prepares data for ip and returns a dataframe with pased data
def prepare_data(name):
    #open file and parse as a dataframe separating different data
    file_path = '../data/' + name + '.txt'
    csv_data = pd.read_csv(
        file_path,
        sep="\t",
        names=["Date", "TTL", "Traceroute", "Delay", "Latency"])

    data = []
    #split traceroute and delay into separate lists of ip addresses
    csv_data["Traceroute"] = csv_data["Traceroute"].str.split(" ")
    csv_data['Delay'] = csv_data['Delay'].str.split(' ')

    #for each set in the dataframe
    for index in csv_data.index:
        #parse traceroute, delay, latency, and ttl
        traceroute = parse_traceroute(csv_data.loc[index, "Traceroute"])
        delay = parse_delay(csv_data.loc[index, 'Delay'])
        latency = float(csv_data.loc[index, 'Latency'])
        ttl = float(csv_data.loc[index, 'TTL'])

        #check for errors and make sure latency exists
        if traceroute != 'ERROR' and delay != 'ERROR' and not math.isnan(latency):
            #put parsed information into a list and append it to total data list
            data_info = []
            data_info.append(latency)
            data_info.append(ttl)
            data_info += traceroute+delay
            data.append(data_info)
        else:
            continue

    #create a dictionary with the list of total data and accuracy -1 as a placeholder
    data_dictionary = {
        'Data': data,
        'Accurate': [-1]*len(data)
    }
    #convert dictionary to a dataframe and return
    return pd.DataFrame(data_dictionary)