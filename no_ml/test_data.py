from train_data import train_data
from parse_data import parse_files
from statistics import mean, median

ips = [
    "66.219.235.31",
    "66.219.235.215",
    "66.219.236.117",
    "69.73.60.141",
    "72.160.10.9",
    "75.174.31.107",
    "76.8.213.221",
    "76.8.213.231",
    "97.117.140.93",
    "136.36.62.167",
    "136.36.203.65",
    "174.52.180.239",
    "byu.edu",
]

data = [parse_files(ip) for ip in ips]

trained_data_df = train_data(data)
# print(trained_data_df)
# for i in range(len(data)):
    # data[i].to_csv('./parsed_data/' + ips[i], index=False)

def test_latency(latency_test_data, min_latency, max_latency):
    # min_lat = median(latency_test_data)
    # print(min_lat)
    # print(min_latency)
    # print(max_latency)
    # if min_lat >= min_latency and min_latency <= max_latency:
    #     return True
    # else:
    #     return False
    latency_results = []
    for i in latency_test_data:
        if i >= min_latency and i <= max_latency:
            latency_results.append(True)
        else:
            latency_results.append(False)
    return latency_results

def test_ttl(ttl_test_data, min_ttl, max_ttl):
    ttl_results = []
    for i in ttl_test_data:
        if i >= min_ttl and i <= max_ttl:
            ttl_results.append(True)
        else:
            ttl_results.append(False)
    return ttl_results

def test_delay(delay_test_data, min_delay, max_delay):
    delay_results = []
    for i in delay_test_data:
        delay_mean = mean(i)
        if delay_mean >= min_delay and delay_mean <= max_delay:
            delay_results.append(True)
        else:
            delay_results.append(False)
    return delay_results

def test_traceroute(traceroute_test_data, common_traceroutes, p):
    # print(common_traceroutes)
    passed = False
    traceroute_results = []

    for trace in traceroute_test_data:
        if trace in common_traceroutes:
            passed = True
        else:
            for traceroute in common_traceroutes:
                score = 0
                for i in range(len(traceroute)):
                    # if traceroute[i] == trace[i]:
                    if trace[i] in traceroute:
                        score += 1
                if score >= 3:
                    passed = True
            if not passed:
                for traceroute in common_traceroutes:
                    if traceroute[3] in trace and traceroute[4] in trace:
                        passed = True
                    else: 
                        passed = False

        # else:
        #     passed = False
        #     trace = trace[3:]
        #     score = 0
        #     for traceroute in common_traceroutes:
        #         traceroute = traceroute[3:]
        #         if not passed:
        #             for i in range(len(traceroute)):
        #                 for j in range(len(traceroute[i])):
        #                     if traceroute[i][j] == trace[i][j]:
        #                         score += 1
        #         if score >= 6:
        #             passed = True
        #         else:
        #             passed = False
        traceroute_results.append(passed)
    return traceroute_results

def test_data(trained_data_df):
    for ip in ips:
        file = open('./outcome/' + ip, 'w')
        file.write('Information for ' + ip)
        file.write('\n\n')

        ip_trained = trained_data_df.loc[trained_data_df['IP'] == ip]
        # print(ip_trained)
        min_latency = ip_trained['Min-Latency'].tolist()[0]
        max_latency = ip_trained['Max-Latency'].tolist()[0]
        min_ttl = ip_trained['Min-ttl'].tolist()[0]
        max_ttl = ip_trained['Max-ttl'].tolist()[0]
        min_delay = ip_trained['Min-delay'].tolist()[0]
        max_delay = ip_trained['Max-delay'].tolist()[0]
        common_traceroutes = ip_trained['Traceroutes'].tolist()

        for i in range(len(data)):
            if ip == ips[i]:
                p = True
            else:
                p = False
            latency_results = test_latency(data[i]['Latency'].tolist()[-1000:], min_latency, max_latency)
            ttl_results = test_ttl(data[i]['TTL'].tolist()[-1000:], min_ttl, max_ttl)
            delay_results = test_delay(data[i]['Delay'].tolist()[-1000:], min_delay, max_delay)
            traceroute_results = test_traceroute(data[i]['Traceroute'].tolist()[-1000:], common_traceroutes, p)
            
            print_results(ips[i], latency_results, ttl_results, delay_results, traceroute_results, file)

def print_results(test_ip, latency_results, ttl_results, delay_results, traceroute_results, file):
    file.write("-"*56+'\n')
    file.write("Testing " + test_ip + '\n')
    
    true_latency, false_latency = return_results(latency_results)
    true_ttl, false_ttl = return_results(ttl_results)
    true_delay, false_delay = return_results(delay_results)
    true_traceroute, false_traceroute = return_results(traceroute_results)

    file.write("\n---Latency---\n")
    # if latency_results:
    #     file.write('Passed Latency Threshold\n')
    # else:
    #     file.write('Failed to pass Latency Threshold\n')
    file.write("Positives: " + str(true_latency) + '\n')
    file.write("Negatives: " + str(false_latency) + '\n')
    file.write("\n---Time To Live---\n")
    file.write("Positives: " + str(true_ttl) + '\n')
    file.write("Negatives: " + str(false_ttl) + '\n')
    file.write("\n---Delay---\n")
    file.write("Positives: " + str(true_delay) + '\n')
    file.write("Negatives: " + str(false_delay) + '\n')
    file.write("\n---Traceroute---\n")
    file.write("Positives: " + str(true_traceroute) + '\n')
    file.write("Negatives: " + str(false_traceroute) + '\n')
    file.write('\n')

def return_results(results):
    true_result = 0
    false_result = 0

    for r in results:
        if r:
            true_result += 1
        else: 
            false_result += 1
    return true_result, false_result

test_data(trained_data_df)



# def test_geoip():

# def test_data():