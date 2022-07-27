from parse_data import parse_files
from statistics import stdev
from statistics import mean

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

def train_latency(latencies):
    latency_stdev = stdev(latencies)
    latency_mean = mean(latencies)
    min_threshold = latency_mean - latency_stdev
    max_threshold = latency_mean + latency_stdev
    return min_threshold, max_threshold

def train_ttl(ttl):
    ttl_stdev = stdev(ttl)
    ttl_mean = mean(ttl)
    min_threshold = ttl_mean - ttl_stdev
    max_threshold = ttl_mean + ttl_stdev
    return min_threshold, max_threshold

def train_delay(delays):
    mean_delays = []
    for delay in delays:
        mean_delays.append(mean(delay))
    delay_stdev = stdev(mean_delays)
    delay_mean = mean(mean_delays)
    min_threshold = delay_mean - delay_stdev
    max_threshold = delay_mean + delay_stdev
    return min_threshold, max_threshold

# def train_traceroute(traceroute):



