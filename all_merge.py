from datetime import date

import pandas as pd


def all_merge(stDay, endDay, stYear, endYear, stMonth, endMonth, filecl):
    cols = ['DATE', 'Time']
    for i in range(4):
        cols.append("CotR%s" % (i + 1))
    for i in range(4):
        cols.append("CotRFC%s" % (i + 1))
    cols.append('PmmrtstN')
    cols.append('TN')
    cols.append('AH')
    df = pd.DataFrame(columns=cols)
    daterange = pd.date_range(date(stYear, stMonth, stDay), date(endYear, endMonth, endDay))
    for single_date in daterange:
        try:
            a_fr4 = pd.read_csv(
                '{}\\n_utc_{:02}-{:02}-{:02}.txt'.format(filecl,
                                                         single_date.date().year,
                                                         single_date.date().month,
                                                         single_date.date().day
                                                         ),
                sep=' ', header=None, skipinitialspace=True)
            a_fr4 = a_fr4.dropna(axis=1, how='all')
            a_fr4.columns = cols
            a_fr4['DATE'] = ['{:02}/{:02}/{}'.format(single_date.date().month,
                                                     single_date.date().day,
                                                     single_date.date().year)] * len(a_fr4.index)
            df = pd.concat([df, a_fr4], ignore_index=True)
        except:
            print("такого файла нит n_utc_{:02}-{:02}.{:02}".format(single_date.date().month,
                                                                    single_date.date().day,
                                                                    single_date.date().year - 2000))
    df['DATE'] = pd.to_datetime(df["DATE"])
    return df
