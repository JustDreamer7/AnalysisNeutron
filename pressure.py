from datetime import date

import pandas as pd


def pressure(stDay, endDay, stYear, endYear, stMonth, endMonth, filecl):
    cols = ['DateTime', 'PD', 'TD', 'Pdatch', 'Temper']
    df = pd.DataFrame(columns=cols)
    daterange = pd.period_range(date(stYear, stMonth, stDay), date(endYear, endMonth, endDay), freq='M')
    for single_date in daterange:
        try:
            nms = ['DateTime', 'PD', 'TD', 'Pdatch', 'Temper']
            timework = pd.read_csv(
                '{}\Press{}_{:02}.dat'.format(filecl,
                                              single_date.year,
                                              single_date.month
                                              ),
                sep='\t', skipinitialspace=True)
            timework = timework.dropna(axis=1, how='all')
            timework.columns = nms
            df = pd.concat([df, timework], ignore_index=True)
        except:
            print("такого файла нит Press{}_{:02}.dat".format(
                single_date.year,
                single_date.month
            ))
    a = []
    b = []
    c = []
    d = []
    e = []
    g = []
    f = []
    k = []
    test = df.isna()
    # print(test)
    print(test[test['DateTime'] == True].index)
    for i in test[test['DateTime'] == True].index:
        print(df[df.index == i])
    try:
        for i in df['DateTime']:
            a.append(str(i).split(' ')[1])
            b.append(str(i).split(' ')[0])
            c.append(int(str(i).split(' ')[0].split('.')[0]))
            d.append(int(str(i).split(' ')[0].split('.')[1]))
            e.append(int(str(i).split(' ')[0].split('.')[2]))
            g.append(int(str(i).split(' ')[1].split(':')[1]))
            f.append(int(str(i).split(' ')[1].split(':')[0]))
            k.append(int(str(i).split(' ')[1].split(':')[2]))
    except:
        # print(df[df['DateTime'] == i])
        print(str(i) + ' - Проблемы с давлением Урагана')
    df['Time'] = a
    df['Date'] = b
    df['Day'] = c
    df['Month'] = d
    df['Year'] = e
    df['Minutes'] = g
    df['Hours'] = f
    df['Seconds'] = k
    del df['DateTime']
    df = df.drop(df[(df['Year'] <= stYear) & (df['Month'] <= stMonth) & (df['Day'] < stDay)].index)
    df = df.drop(df[(df['Year'] >= endYear) & (df['Month'] >= endMonth) & (df['Day'] > endDay)].index)
    df = df.reset_index()
    return df
