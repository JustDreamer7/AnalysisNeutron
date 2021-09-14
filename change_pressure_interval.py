from check_pressure import check_pressure
import pandas as pd

def change_pressure_interval(stday, endday, styear, endyear, stmonth, endmonth, file1cl, cutting_len):
    pressure_uragan, dont_use_it = check_pressure(stday, endday, styear, endyear, stmonth, endmonth, file1cl)
    mean_result_list = []
    # Date = []
    # Time = []
    for frame in pressure_uragan:
        single_break = pd.DataFrame(frame)
        counter = 0
        summator = 0
        mean_result = []
        for i in range(len(single_break['Minutes'])):
            counter += 1
            summator += single_break['Pdatch'][i]
            if (single_break['Minutes'][i] % 10 == 0 or single_break['Minutes'][i] % 5 == 0) and counter > 7:
                # Date.append(str(frame['Date'][i]).split(' ')[0].split('.')[2] + '-' +
                #             str(frame['Date'][i]).split(' ')[0].split('.')[1] + '-' +
                # str(frame['Date'][i]).split(' ')[0].split('.')[0])
                # Time.append('{}:{:02}'.format(frame['Time'][i].split(':')[0], frame['Minutes'][i]))
                mean_result.append(round(summator / counter / 0.75006156, 2))
                summator = 0
                counter = 0
        mean_result.append(round(summator / counter / 0.75006156, 2))
        mean_result_list.append(mean_result)
    corr_mean_result = mean_result_list[0]
    if len(cutting_len) != 0:
        for i in range(1, len(mean_result_list)):
            corr_mean_result = corr_mean_result + [0]*cutting_len[i - 1] + mean_result_list[i]
    return corr_mean_result
