from datetime import date

import pandas as pd


def vaisala(stDay, endDay, stYear, endYear, stMonth, endMonth, filecl):
    cols = ['TIME', 'TA', 'RH', 'PR']
    df = pd.DataFrame(columns=cols)
    daterange = pd.date_range(date(stYear, stMonth, stDay), date(endYear, endMonth, endDay))
    for single_date in daterange:
        try:
            vais = pd.read_csv(
                '{}\Station02__SMSAWS__{}{:02}{:02}.txt'.format(filecl,
                                                                single_date.year,
                                                                single_date.month,
                                                                single_date.day
                                                                ),
                sep='\t', skipinitialspace=True)
            vais = vais[['TIME', 'TA', 'RH', 'PR']]
            df = pd.concat([df, vais], ignore_index=True)
        except:
            print("такого файла нит Station02__SMSAWS__{}{:02}{:02}.txt".format(
                single_date.year,
                single_date.month,
                single_date.day
            ))
    data = []
    time = []
    for i in df['TIME']:
        item = i.split(' ')
        data.append(item[0])
        time.append(item[1])
    df['time'] = time
    df['date'] = data
    return df
