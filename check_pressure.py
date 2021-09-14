import datetime

from pressure import pressure


def check_pressure(stday, endday, styear, endyear, stmonth, endmonth, file1cl):
    pressure_uragan = pressure(stday, endday, styear, endyear, stmonth, endmonth, file1cl)
    breaks = []
    for_cutting = []
    for i in range(1, len(pressure_uragan.index)):
        if datetime.datetime(pressure_uragan['Year'][i], pressure_uragan['Month'][i], pressure_uragan['Day'][i],
                             pressure_uragan['Hours'][i], pressure_uragan['Minutes'][i],
                             pressure_uragan['Seconds'][i]) - datetime.datetime(pressure_uragan['Year'][i - 1],
                                                                                pressure_uragan['Month'][i - 1],
                                                                                pressure_uragan['Day'][i - 1],
                                                                                pressure_uragan['Hours'][i - 1],
                                                                                pressure_uragan['Minutes'][i - 1],
                                                                                pressure_uragan['Seconds'][
                                                                                    i - 1]) > datetime.timedelta(0, 25):
            breaks.append(i)
            for_cutting.append([datetime.datetime(pressure_uragan['Year'][i - 1],
                                                  pressure_uragan['Month'][i - 1],
                                                  pressure_uragan['Day'][i - 1],
                                                  pressure_uragan['Hours'][i - 1],
                                                  pressure_uragan['Minutes'][i - 1],
                                                  pressure_uragan['Seconds'][
                                                      i - 1]),
                                datetime.datetime(pressure_uragan['Year'][i], pressure_uragan['Month'][i],
                                                  pressure_uragan['Day'][i],
                                                  pressure_uragan['Hours'][i], pressure_uragan['Minutes'][i],
                                                  pressure_uragan['Seconds'][i])])
    pressure_uragan_with_breaks = []
    rem = 0
    for i in breaks:
        pressure_uragan_with_breaks.append(pressure_uragan.iloc[rem:i].reset_index(drop=True))
        rem = i
    pressure_uragan_with_breaks.append(pressure_uragan.iloc[rem:].reset_index(drop=True))
    return pressure_uragan_with_breaks, for_cutting
