import pandas as pd

from concat_utc import concat_utc


def timeBreak(stDay, endDay, stYear, endYear, stMonth, endMonth, filecl):
    timestop = concat_utc(stDay, endDay, stYear, endYear, stMonth, endMonth, filecl)
    cols = ['claster', 'stDate', 'endDate', 'stTime', 'endTime']
    timedict = []
    try:
        for i in range(1, 5):
            timelist = []
            if len(timestop[(timestop['Nn%s' % i] == 0) & (timestop['N_noise%s' % i] == 0)]) != 0:
                timelist.append(i)
                timelist.append(
                    timestop[(timestop['Nn%s' % i] == 0) & (timestop['N_noise%s' % i] == 0)]['DATE'].tolist()[0])
                timelist.append(
                    timestop[(timestop['Nn%s' % i] == 0) & (timestop['N_noise%s' % i] == 0)]['DATE'].tolist()[-1])
                timelist.append(
                    timestop[(timestop['Nn%s' % i] == 0) & (timestop['N_noise%s' % i] == 0)]['time'].tolist()[0])
                timelist.append(
                    timestop[(timestop['Nn%s' % i] == 0) & (timestop['N_noise%s' % i] == 0)]['time'].tolist()[-1])
                timedict.append(timelist)
    except:
        print("Проверьте вывод до этого.")
    df = pd.DataFrame(timedict, columns=cols)
    df['stDate'] = pd.to_datetime(df["stDate"])
    df['endDate'] = pd.to_datetime(df["endDate"])
    return df
