import pandas as pd

def train(data):
    training_data_df = pd.DataFrame()
    traceroutes = train_traceroute(data['Traceroute'])
    train_df = pd.DataFrame({'Traceroutes': traceroutes})
    training_data_df = pd.concat([training_data_df, train_df], ignore_index=True)
    return training_data_df

def train_traceroute(traceroute):
    traceroute_lst = []
    for trace in traceroute:
        if trace not in traceroute_lst:
            traceroute_lst.append(trace)

    # for idx, route in enumerate(traceroute.value_counts().index.tolist()):
    #     if traceroute.value_counts()[idx]/len(traceroute) > 0.3:
    #         traceroute_lst.append(route)
    return traceroute_lst