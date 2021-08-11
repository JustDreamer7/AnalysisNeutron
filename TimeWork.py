import pandas as pd
from datetime import date


def timeWork(stDay, endDay, stYear, endYear, stMonth, endMonth, filecl):
    cols = ['DATE']
    for i in range(1,5):
        cols.append("WORKTIME%s" % (i))
    timedict = []
    daterange = pd.date_range(date(stYear, stMonth, stDay), date(endYear, endMonth, endDay))
    # Изменить форму обработки, годовой отчет нельзя сделать нихуя не покажет, если задать не последовательные месяца
    for single_date in daterange:
        nms = ['date', 'time']
        for i in range(4):
            nms.append("Nn%s" % (i + 1))
        for i in range(4):
            nms.append("N_noise%s" % (i + 1))
        for i in range(3):
            nms.append("Const%s" % (i + 1))
        try:
            timelist = []
            timework = pd.read_csv(
                '{}\\n_utc_{:02}-{:02}-{:02}.txt'.format(filecl,
                                                     single_date.date().year,
                                                     single_date.date().month,
                                                     single_date.date().day
                                                     ),
                sep=' ',
                header=None, skipinitialspace=True)
            timework = timework.dropna(axis=1, how='all')
            timework.columns = nms
            timelist.append(
                '{:02}/{:02}/{}'.format(single_date.date().month, single_date.date().day, single_date.date().year))
            for i in range(1,5):
                timelist.append(round((len(timework.index) - len(timework[(timework['Nn%s' % i] == 0) & (timework['N_noise%s' % i] == 0)])) * 5 / 60, 2))
            timedict.append(timelist)
        except:
            print("такого файла нит n_utc_{:02}-{:02}-{:02}.txt".format(single_date.date().year,
                                                                    single_date.date().month,
                                                                    single_date.date().day))
    df = pd.DataFrame(timedict, columns=cols)
    df['DATE'] = pd.to_datetime(df["DATE"])
    return df











# import pandas as pd
# from datetime import date
#
#
# def timeWork(stDay, endDay, stYear, endYear, stMonth, endMonth, filecl):
#     cols = ['DATE', 'WORKTIME']
#     timedict = []
#     daterange = pd.date_range(date(stYear, stMonth, stDay), date(endYear, endMonth, endDay))
#     # Изменить форму обработки, годовой отчет нельзя сделать нихуя не покажет, если задать не последовательные месяца
#     for single_date in daterange:
#         nms = ['date', 'time']
#         for i in range(4):
#             nms.append("Nn%s" % (i + 1))
#         for i in range(4):
#             nms.append("N_noise%s" % (i + 1))
#         for i in range(3):
#             nms.append("Const%s" % (i + 1))
#         try:
#             timelist = []
#             timework = pd.read_csv(
#                 '{}\\n_utc_{:02}-{:02}-{:02}.txt'.format(filecl,
#                                                      single_date.date().year,
#                                                      single_date.date().month,
#                                                      single_date.date().day
#                                                      ),
#                 sep=' ',
#                 header=None, skipinitialspace=True)
#             timework = timework.dropna(axis=1, how='all')
#             timework.columns = nms
#             timelist.append(
#                 '{:02}/{:02}/{}'.format(single_date.date().month, single_date.date().day, single_date.date().year))
#             # timelist.append(round(len(timework.index) * 5 / 60, 2))
#             # timedict.append(timelist)
#         except:
#             print("такого файла нит n_utc_{:02}-{:02}-{:02}.txt".format(single_date.date().year,
#                                                                     single_date.date().month,
#                                                                     single_date.date().day))
#     df = pd.DataFrame(timedict, columns=cols)
#     df['DATE'] = pd.to_datetime(df["DATE"])
#     return df
