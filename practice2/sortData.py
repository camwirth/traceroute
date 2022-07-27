import pandas as pd
import math
import random
import argparse
import parsingDataFile as parse

TTL = 0
TRACEROUTE = 1
DELAY = 2
LATENCY = 3
CORRECT = 4

parser = argparse.ArgumentParser()
parser.add_argument('--percent', type=float, default=0.5, help='percentage of data that are false')
parser.add_argument('--size', type=int, default=100, help='size of the data group')
args = parser.parse_args()

percent = args.percent
size = args.size

false_size = int(size*percent)
true_size = int(size*(1-percent))

output_data = [
    '../data/byu.edu.txt',
    '../data/66.219.235.31.txt',
    '../data/66.219.235.215.txt',
    '../data/66.219.236.117.txt',
    '../data/69.73.60.141.txt',
    '../data/72.160.10.9.txt',
    '../data/75.174.31.107.txt',
    '../data/76.8.213.221.txt',
    '../data/76.8.213.231.txt',
    '../data/97.117.140.93.txt',
    '../data/136.36.62.167.txt',
    '../data/136.36.203.65.txt',
    '../data/174.52.180.239.txt',
]

true_data = '../data/66.219.235.31.txt'
false_data = [
    '../data/byu.edu.txt',
    '../data/66.219.235.215.txt',
    '../data/66.219.236.117.txt',
    '../data/69.73.60.141.txt',
    '../data/72.160.10.9.txt',
    '../data/75.174.31.107.txt',
    '../data/76.8.213.221.txt',
    '../data/76.8.213.231.txt',
    '../data/97.117.140.93.txt',
    '../data/136.36.62.167.txt',
    '../data/136.36.203.65.txt',
    '../data/174.52.180.239.txt',
]

def parse_data(data_file, data_list correct):
    csv_data = pd.read_csv(
        data_file, sep='\t', names=['DATE', 'TTL', 'TRACEROUTE', 
        'DELAY', 'LATENCY'])
    
    csv_data['TRACEROUTE'] = csv_data['TRACEROUTE'].str.split(' ')
    csv_data['DELAY'] = csv_data['DELAY'].str.split(' ')

    for index in csv_data.index:
        ttl = parse.ttl(csv_data.loc[index, 'TTL'])
        traceroute = parse.traceroute(csv_data.loc[index, 'TRACEROUTE'])
        delay = parse.delay(csv_data.loc[index, 'DELAY'])
        latency = parse.latency(csv_data.loc[index, 'LATENCY'])

        if(not math.isnan(latency) and traceroute != 'ERROR' and delay != 'ERROR'):
             data_list[TTL].append(ttl)
             data_list[TRACEROUTE].append(traceroute)
             data_list[DELAY].append(delay)
             data_list[LATENCY].append(latency)
             data_list[CORRECT].append(correct)
        else:
            continue

def parse_false_data(false_data, data_list):
    for data in false_data:
        parse_data(data, data_list, False)
    return data_list

def combine_lists(true_data_list, false_data_list):
    train_data = [[], [], [], [], []]
    test_data = [[], [], [], [], []]

    i=0
    while(i<5):
        random.shuffle(false_data_list[i])
        i=i+1
    
    i=0
    while(i<5):
        train_data[i] = true_data_list[i][:true_size] + false_data_list[i][:true_size]
        test_data[i] = true_data_list[i][true_size:] + false_data_list[i][true_size:]
        random.shuffle(train_data[i])
        random.shuffle(test_data[i])
        print()
        print(i)
        print(train_data[i])
        i=i+1

    return train_data, test_data

def collect_data(true_data, false_data):
    true_list = [[], [], [], [], []]
    false_list = [[], [], [], [], []]

    parse_data(true_data, true_list, True)
    #print(true_list)
    parse_false_data(false_data, false_list)

    train_data, test_data = combine_lists(true_list, false_list)

    return train_data, test_data

    
def main():
    train_data, test_data = collect_data(true_data,false_data)
    # false_data = []
    # for true_data in output_data:
    #     for data in output_data:
    #         if data != true_data:
    #             false_data.append(data)
    #     train_data, test_data = collect_data(true_data, false_data)
    #     print(train_data)
    #     print(test_data)

main()
