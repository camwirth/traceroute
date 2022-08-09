from statistics import mean
import pandas as pd
import ast

def test_traceroute(traceroute_test_data, common_traceroutes):
    passed = False
    traceroute_results = []

    #go through each traceroute in the list of the test data
    for trace in traceroute_test_data:
        #convert the trace from a string to a list
        trace = ast.literal_eval(trace)

        #i don't think this works with reading in data froma file...
        if trace in common_traceroutes:
            passed = True
        else:
            #for each traceroute in the common traceroutes established as trained data
            for trained_trace in common_traceroutes:
                #convert traceroute to a list
                trained_trace = ast.literal_eval(trained_trace)
                score = 0
                #go through each ip in traceroute we are testing
                for ip in trace:
                    #if there are 3 ips in the trained traceroute, the testing traceroute passes
                    if ip in trained_trace:
                        score += 1
                if score >= 2:
                    passed = True
                    break
                # elif trace[3] == trained_trace[3] and trace[4] == trained_trace[4]:
                #     passed = True
                #     break
                else:
                    passed = False
    
        traceroute_results.append(passed)
    return traceroute_results

def test_trace(trained_df, test_df):
    common_traceroutes = trained_df['Traceroutes'].tolist()
    traceroute_results = test_traceroute(test_df['Traceroute'].tolist(), common_traceroutes)
    return moved(traceroute_results)

def test_traceroute_verbose(traceroute_test_data, common_traceroutes):
    passed = False
    traceroute_results = []

    print(common_traceroutes)
    for trace in traceroute_test_data:
        trace = ast.literal_eval(trace)
        if trace in common_traceroutes:
            passed = True
        else:
            print('test: ',trace)
            for trained_trace in common_traceroutes:
                trained_trace = ast.literal_eval(trained_trace)
                print('trained: ', trained_trace)
                score = 0
                for ip in trace:
                    if ip in trained_trace:
                        score += 1
                # print(score)
                if score >= 3:
                    passed = True
                    break
                else:
                    passed = False

            print(score)
            print(passed)
        traceroute_results.append(passed)
    print(traceroute_results)
    return traceroute_results
    # exit(1)
        # traceroute_results.append(passed)
        # return traceroute_results

def test_trace_verbose(trained_df, test_df):
    common_traceroutes = trained_df['Traceroutes'].tolist()
    print('Common Traceroutes')
    print(common_traceroutes)
    traceroute_results = test_traceroute_verbose(test_df['Traceroute'].tolist(), common_traceroutes)
    return moved_verbose(traceroute_results)

def moved_verbose(traceroute_results):
    true = 0
    for result in traceroute_results:
        if result:
            true += 1
    print(true)
    percent_true = true/len(traceroute_results)
    print(percent_true)
    exit(1)

def moved(traceroute_results):
    true_traceroute = return_true_percentage(traceroute_results)
    # print(traceroute_results)
    # print(true_traceroute)
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

