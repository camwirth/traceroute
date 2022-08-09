import pandas as pd

def train(data):
    traceroutes = train_traceroute(data['Traceroute'])
    train_df = pd.DataFrame({'Traceroutes': traceroutes})
    return train_df

def train_traceroute(traceroute):
    traceroute_lst = []
    for idx, route in enumerate(traceroute.value_counts().index.tolist()):
        if traceroute.value_counts()[idx]/len(traceroute) > 0.3:
            traceroute_lst.append(route)
            
    return traceroute_lst