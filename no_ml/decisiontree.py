import pandas as pd

def parse_files(name):
    file_path = '../data/' + name + '.txt'
    csv_data = pd.read_csv(
        file_path,
        sep='\t',
        names=['Date', 'TTL', 'Traceroute', 'Delay', 'Latency']
    )

    csv_data['Traceroute'] = csv_data['Traceroute'].str.split(' ')
    csv_data['Delay'] = csv_data['Delay'].str.split(' ')
    return csv_data

#comparing latency
#