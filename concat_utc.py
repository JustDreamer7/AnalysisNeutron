import pandas as pd
from datetime import date


def concat_utc(stDay, endDay, stYear, endYear, stMonth, endMonth, filecl):
    cols = ['DATE', 'time']
    for i in range(4):
        cols.append("Nn%s" % (i + 1))
    for i in range(4):
        cols.append("N_noise%s" % (i + 1))
    df = pd.DataFrame(columns=cols)
    daterange = pd.date_range(date(stYear, stMonth, stDay), date(endYear, endMonth, endDay))
    for single_date in daterange:
        nms = ['date', 'time']
        for i in range(4):
            nms.append("Nn%s" % (i + 1))
        for i in range(4):
            nms.append("N_noise%s" % (i + 1))
        for i in range(3):
            nms.append("Const%s" % (i + 1))
        try:
            a_fr4 = pd.read_csv(
                '{}\\n_utc_{:02}-{:02}-{:02}.txt'.format(filecl,
                                                     single_date.date().year,
                                                     single_date.date().month,
                                                     single_date.date().day
                                                     ),
                sep=' ', header=None, skipinitialspace=True)
            a_fr4 = a_fr4.dropna(axis=1, how='all')
            a_fr4.columns = nms
            a_fr4['DATE'] = ['{:02}/{:02}/{}'.format(single_date.date().month,
                                                     single_date.date().day,
                                                     single_date.date().year)] * len(a_fr4.index)
            a_fr4 = a_fr4[cols]
            df = pd.concat([df, a_fr4], ignore_index=True)
        except:
            print("такого файла нит n_utc_{:02}-{:02}.{:02}".format(single_date.date().month,
                                                                 single_date.date().day,
                                                                 single_date.date().year - 2000))
    df['DATE'] = pd.to_datetime(df["DATE"])
    return df

    
