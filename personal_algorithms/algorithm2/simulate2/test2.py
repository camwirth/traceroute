import ast

def test_traceroute(traceroute_test_data, common_traceroutes):
    passed = False
    traceroute_results = []

    #go through each traceroute in the list of the test data
    for trace in traceroute_test_data:
        #convert the trace from a string to a list
        trace = ast.literal_eval(trace)

        for trained_trace in common_traceroutes:
            score = 0
            #convert traceroute to a list
            trained_trace = ast.literal_eval(trained_trace)
            for ip in trace:
                if ip in trained_trace:
                    score += 1
            if score >= 2:
                passed = True
                break
            else:
                passed = False

        traceroute_results.append(passed)
    return traceroute_results

def test_trace(trained_df, test_df):
    common_traceroutes = trained_df['Traceroutes'].reset_index(drop=True).to_list()
    traceroute_results = test_traceroute(test_df['Traceroute'].tolist(), common_traceroutes)
    return moved(traceroute_results)

def moved(traceroute_results):
    true_traceroute = return_true_percentage(traceroute_results)
    if true_traceroute >= 0.9:
        return False
    else: 
        return True

def return_true_percentage(results):
    true = 0
    for result in results:
        if result:
            true += 1
    percent_true = true/len(results)
    return percent_true