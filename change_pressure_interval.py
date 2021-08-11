from pressure import pressure

def change_pressure_interval(stday, endday, styear, endyear, stmonth, endmonth, file1cl):
    pressure_uragan = pressure(stday, endday, styear, endyear, stmonth, endmonth, file1cl)

    mean_result = []
    counter = 0
    summator = 0
    for i in range(len(pressure_uragan['Minutes'])):
        counter += 1
        summator += pressure_uragan['Pdatch'][i]
        if (pressure_uragan['Minutes'][i] % 10 == 0 or pressure_uragan['Minutes'][i] % 5 == 0) and counter > 7:
            mean_result.append(round(summator / counter / 0.75006156, 2))
            summator = 0
            counter = 0
    mean_result.append(round(summator/counter/0.75006156,2))

    return mean_result