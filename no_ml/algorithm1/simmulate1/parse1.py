import pandas as pd

#function parses data given ipaddress file name
def parse_files(name):
    #find data in text file and convert to a dataframe separating data
    file_path = '../../../data/' + name + '.txt'
    csv_data = pd.read_csv(
        file_path,
        sep='\t',
        names=['Date', 'TTL', 'Traceroute', 'Delay', 'Latency']
    )

    traceroute_lst = []

    #tracerotue is separated to each ip address
    csv_data['Traceroute'] = csv_data['Traceroute'].str.split(' ')

    #allow data in each line of dataframe to be accessed and parsed
    for index in csv_data.index:
        traceroute = parse_traceroute(csv_data.loc[index, "Traceroute"])

        #ensure there are no errors and append parsed data to total list
        if traceroute != 'ERROR':
            traceroute_lst.append(traceroute)
        else:
            continue
    
    #create a dataframe with the information received 
    df = pd.DataFrame()
    df['IP'] = [name]*len(traceroute_lst)
    df['Traceroute'] = traceroute_lst

    return df

#function returns a list of last 5 ips correctly formatted
def parse_traceroute(traceroute):
    ips = []
    
    #go through each ip in traceroute and ignore stars or empty strings
    for i in range(len(traceroute)):
        if traceroute[i] == '*' or traceroute[i] == '':
            continue
        else:
            ips.append(traceroute[i])
    
    #check that there are at least 5 ips in lst
    if len(ips) < 5:
        return "ERROR"
    
    five_ips = []
    #split last 5 ips and append first 3 bytes of each ip to lst of 5 ips 
    for ip in ips[-5:]:
        ip = ip.split('.')
        single_ip = []
        for i in ip:
            if i == '':
                return 'ERROR'
            else:
                single_ip.append(int(i))
        five_ips.append(single_ip[0:3])

    return five_ips

#list each ip and their location
ips = [
    ["66.219.235.31","Provo, UT"],
    ["66.219.235.215", "Provo, UT"],
    ["66.219.236.117", "Provo, UT"],
    ["69.73.60.141", "Alabama?"],
    ["72.160.10.9", "Kalispell, MT"],
    ["75.174.31.107", "Boise, ID"],
    ["76.8.213.221", "Provo, UT"],
    ["76.8.213.231", "Provo, UT"],
    ["97.117.140.93", "Salt Lake City, UT"],
    ["136.36.62.167", "Provo, UT"],
    ["136.36.203.65", "Provo, UT"],
    ["174.52.180.239", "Sandy, UT?"],
    ["byu.edu", "Provo, UT"],
]

#parse data for each ip
data = [parse_files(ip[0]) for ip in ips]

#save data to a csv file
for i in range(len(data)):
    data[i].to_csv('../parsed_data1/' + ips[i][0] + '.csv')
