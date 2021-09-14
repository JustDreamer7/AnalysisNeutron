import os
from datetime import *

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

from all_merge import all_merge
from change_pressure_interval import change_pressure_interval
from check_pressure import check_pressure
from concat_utc import concat_utc
from vaisala import vaisala


# функция для фита графика скорости счета к разности давлений
def linear(x, a, b):
    return a * x + b


def First_Proccessing(stday, stmonth, styear, endday, endmonth, endyear, path, pathpic, pathfile, file_neutron_data,
                      file_uragan_pressure, file_vaisala_pressure, proccessing_pressure):
    datedirect = pathpic + '/{}'.format(styear)
    if ~os.path.exists(datedirect):
        try:
            os.mkdir(datedirect)
        except OSError:
            print("Создать директорию %s не удалось" % datedirect)
        else:
            print("Успешно создана директория %s " % datedirect)
    datedirect = pathfile + '/{}'.format(styear)
    if ~os.path.exists(datedirect):
        try:
            os.mkdir(datedirect)
        except OSError:
            print("Создать директорию %s не удалось" % datedirect)
        else:
            print("Успешно создана директория %s " % datedirect)

    font = {'weight': 'bold',
            'size': 14}

    plt.rc('font', **font)

    merge_utc = concat_utc(stday, endday, styear, endyear, stmonth, endmonth, file_neutron_data)
    cutting_len = []
    dont_use_it, cutting_intervals_uragan = check_pressure(stday, endday, styear, endyear, stmonth, endmonth,
                                                           file_uragan_pressure)

    if len(cutting_intervals_uragan) != 0:
        new_time = []
        for g in range(len(merge_utc['time'])):
            new_time.append(datetime(int(str(merge_utc['DATE'][g]).split(' ')[0].split('-')[0]),
                                     int(str(merge_utc['DATE'][g]).split(' ')[0].split('-')[1]),
                                     int(str(merge_utc['DATE'][g]).split(' ')[0].split('-')[2]),
                                     int(merge_utc['time'][g].split(':')[0]),
                                     int(merge_utc['time'][g].split(':')[1])))
        merge_utc['new_format_time'] = new_time

        for i in range(1, 5):
            for a in cutting_intervals_uragan:
                merge_utc['Nn%s' % i] = merge_utc['Nn%s' % i].where(
                    (merge_utc['new_format_time'] < a[0]) | (
                            merge_utc['new_format_time'] > a[1]), 0)
                merge_utc['N_noise%s' % i] = merge_utc['N_noise%s' % i].where(
                    (merge_utc['new_format_time'] < a[0]) | (
                            merge_utc['new_format_time'] > a[1]), 0)

        for a in cutting_intervals_uragan:
            cutting_len.append(len(merge_utc.index) - len(merge_utc[(merge_utc['new_format_time'] < a[0]) | (
                    merge_utc['new_format_time'] > a[1])].index))

    mean_pressure_uragan = change_pressure_interval(stday, endday, styear, endyear, stmonth, endmonth,
                                                    file_uragan_pressure, cutting_len)

    if len(mean_pressure_uragan) >= len(merge_utc.index):
        mean_pressure_uragan = mean_pressure_uragan[0:len(merge_utc.index)]

    def make_corr_data(type_of_impulse, pressure, type_of_impulse_sign, pathpic, styear, stday, stmonth, endday,
                       endmonth):
        fig, axs = plt.subplots(figsize=(18, 18), nrows=4, sharex=True)
        N_bar_koef = []
        N_0 = []
        for i in range(1, 5):
            ax = axs[i - 1]
            ax.set_title('Детектор %s' % i, fontsize=18, loc='left')
            if i == 5:
                ax.set_xlabel('Давление', fontsize=20)
            ax.set_ylabel(type_of_impulse_sign + r'$, (300с)^{-1}$', fontsize=15)
            #     ax.set_ylim([0,500])
            #     ax.set_xlim([0,df.index.max()])
            if len(merge_utc[merge_utc[type_of_impulse + '%s' % i] == 0]) != 0:
                test = []
                for j in merge_utc[merge_utc[type_of_impulse + '%s' % i] != 0].index.tolist():
                    if mean_pressure_uragan[j] != 0:
                        test.append(mean_pressure_uragan[j])
                    else:
                        merge_utc.loc[j, type_of_impulse + '%s' % i] = 0
                ax.scatter([x - pressure for x in test],
                           merge_utc[merge_utc[type_of_impulse + '%s' % i] != 0][type_of_impulse + '%s' % i],
                           label=type_of_impulse + '%s' % i, s=5)
                param, param_cov = curve_fit(linear, [x - pressure for x in test],
                                             merge_utc[merge_utc[type_of_impulse + '%s' % i] != 0][
                                                 type_of_impulse + '%s' % i])
                fit_line = [y * param[0] + param[1] for y in [x - pressure for x in test]]
                ax.scatter([x - pressure for x in test], fit_line, s=6)
                N_bar_koef.append(param[0] / param[1] * 100)
                N_0.append(param[1])
            else:
                ax.scatter([x - pressure for x in mean_pressure_uragan], merge_utc[type_of_impulse + '%s' % i],
                           label=type_of_impulse + '%s' % i, s=5)
                param, param_cov = curve_fit(linear, [x - pressure for x in mean_pressure_uragan],
                                             merge_utc[type_of_impulse + '%s' % i])
                fit_line = [y * param[0] + param[1] for y in [x - pressure for x in mean_pressure_uragan]]
                ax.scatter([x - pressure for x in mean_pressure_uragan], fit_line, s=6)
                N_bar_koef.append(param[0] / param[1] * 100)
                N_0.append(param[1])

        plt.savefig(
            '{}\\{}\\{}(P){:02}-{:02}-{:02}-{:02}.png'.format(pathpic, styear, type_of_impulse, stday, stmonth,
                                                              endday, endmonth),
            bbox_inches='tight')

        press_for_fixed_N = []
        for i in range(4):
            intermediate_corr = []
            for x in mean_pressure_uragan:
                if x != 0:
                    intermediate_corr.append((x - pressure) * N_bar_koef[i] / 100 * N_0[i])
                else:
                    intermediate_corr.append(0)
            press_for_fixed_N.append(intermediate_corr)

        return press_for_fixed_N

    if proccessing_pressure == 'mean_value':
        press_for_fixed_N = make_corr_data('Nn', np.mean(mean_pressure_uragan), 'Скорость счета', pathpic, styear,
                                           stday,
                                           stmonth, endday,
                                           endmonth)
        press_for_fixed_N_noise = make_corr_data('N_noise', np.mean(mean_pressure_uragan), 'Скорость счета шумов',
                                                 pathpic,
                                                 styear, stday,
                                                 stmonth, endday,
                                                 endmonth)
    else:
        press_for_fixed_N = make_corr_data('Nn', 993, 'Скорость счета', pathpic, styear,
                                           stday,
                                           stmonth, endday,
                                           endmonth)
        press_for_fixed_N_noise = make_corr_data('N_noise', 993, 'Скорость счета шумов',
                                                 pathpic,
                                                 styear, stday,
                                                 stmonth, endday,
                                                 endmonth)

    fig, axs = plt.subplots(figsize=(18, 18), nrows=4, sharex=True)
    corr_N = []
    for i in range(1, 5):
        merge_utc['corr_N%s' % i] = merge_utc['Nn%s' % i] - press_for_fixed_N[i - 1]
        merge_utc['corr_N%s' % i].where(merge_utc['corr_N%s' % i] > 10, 0, inplace=True)
        merge_utc['corr_N%s' % i].where(merge_utc['corr_N%s' % i] != merge_utc['Nn%s' % i], 0, inplace=True)
        corr_N.append(merge_utc['corr_N%s' % i])
        ax = axs[i - 1]
        ax.set_title('Детектор %s' % i, fontsize=18, loc='left')
        ax0 = ax.twinx()
        ax0.set_ylim([970, 1020])
        ax0.set_ylabel('Давление, мбар', fontsize=15)
        if i == 5:
            ax.set_xlabel('Дата', fontsize=20)
        ax.set_ylabel(r'$Cкорость счета, (300с)^{-1}$', fontsize=14)
        # ax.set_ylim([0, 500])
        ax.set_xlim([0, merge_utc.index.max()])
        ax.plot(merge_utc.index, merge_utc['Nn%s' % i], label='N%s' % i, linewidth=1, color='black')
        ax.plot(merge_utc.index, merge_utc['corr_N%s' % i], label='N%s' % i, linewidth=1,
                color='red')

        ax0.plot(range(0, len(mean_pressure_uragan)), mean_pressure_uragan, linewidth=2, color='blue')
        ax.set_xticks(list(range(0, merge_utc.index.max(), 288 * 5)))
        ax.set_xticklabels(merge_utc['DATE'].dt.date.unique().tolist()[::5])
    plt.savefig('{}\\{}\\Nn300c_without_mask{:02}-{:02}-{:02}-{:02}.png'.format(pathpic, styear, stday, stmonth, endday,
                                                                                endmonth),
                bbox_inches='tight')

    fig, axs = plt.subplots(figsize=(18, 18), nrows=4, sharex=True)
    corr_N_noise = []
    for i in range(1, 5):
        merge_utc['corr_N_noise%s' % i] = merge_utc['N_noise%s' % i] - press_for_fixed_N_noise[i - 1]
        merge_utc['corr_N_noise%s' % i].where(merge_utc['corr_N_noise%s' % i] > 10, 0, inplace=True)
        merge_utc['corr_N%s' % i].where(merge_utc['corr_N_noise%s' % i] != merge_utc['N_noise%s' % i], 0, inplace=True)
        corr_N_noise.append(merge_utc['corr_N_noise%s' % i])
        ax = axs[i - 1]
        ax.set_title('Детектор %s' % i, fontsize=18, loc='left')
        ax0 = ax.twinx()
        ax0.set_ylim([970, 1020])
        ax0.set_ylabel('Давление, мбар', fontsize=15)
        if i == 5:
            ax.set_xlabel('Дата', fontsize=20)
        ax.set_ylabel(r'$Cкорость счета шумов, (300с)^{-1}$', fontsize=14)
        # ax.set_ylim([0, 500])
        ax.set_xlim([0, merge_utc.index.max()])
        ax.plot(merge_utc.index, merge_utc['N_noise%s' % i], label='N%s' % i, linewidth=1, color='black')
        ax.plot(merge_utc.index, merge_utc['corr_N_noise%s' % i], label='N%s' % i,
                linewidth=1,
                color='red')
        ax0.plot(range(0, len(mean_pressure_uragan)), mean_pressure_uragan, linewidth=2, color='blue')
        ax.set_xticks(list(range(0, merge_utc.index.max(), 288 * 5)))
        ax.set_xticklabels(merge_utc['DATE'].dt.date.unique().tolist()[::5])
    plt.savefig(
        '{}\\{}\\Nnoise300c_without_mask{:02}-{:02}-{:02}-{:02}.png'.format(pathpic, styear, stday, stmonth, endday,
                                                                            endmonth),
        bbox_inches='tight')

    for i in range(1, 5):
        N_file = merge_utc[['DATE', 'time', 'Nn%s' % i]].sort_values('Nn%s' % i, ascending=False)
        N_file.to_csv(
            '{}\\{}\\Nn{}- возрастание{:02}-{:02}-{:02}-{:02}.csv'.format(pathfile, styear, i, stday, stmonth, endday,
                                                                          endmonth),
            sep=';', index=False)
    for i in range(1, 5):
        N_file = merge_utc[['DATE', 'time', 'Nn%s' % i]].sort_values('Nn%s' % i)
        N_file.to_csv(
            '{}\\{}\\Nn{} - убывание{:02}-{:02}-{:02}-{:02}.csv'.format(pathfile, styear, i, stday, stmonth, endday,
                                                                        endmonth),
            sep=';', index=False)
    for i in range(1, 5):
        N_file = merge_utc[['DATE', 'time', 'N_noise%s' % i]].sort_values('N_noise%s' % i, ascending=False)
        N_file.to_csv(
            '{}\\{}\\N_noise{} - возрастание{:02}-{:02}-{:02}-{:02}.csv'.format(pathfile, styear, i, stday, stmonth,
                                                                                endday,
                                                                                endmonth), sep=';', index=False)
    for i in range(1, 5):
        N_file = merge_utc[['DATE', 'time', 'N_noise%s' % i]].sort_values('N_noise%s' % i)
        N_file.to_csv(
            '{}\\{}\\N_noise{} - убывание{:02}-{:02}-{:02}-{:02}.csv'.format(pathfile, styear, i, stday, stmonth,
                                                                             endday, endmonth),
            sep=';', index=False)

    vaisala_data = vaisala(stday, endday, styear, endyear, stmonth, endmonth, file_vaisala_pressure)
    merged_df = all_merge(stday, endday, styear, endyear, stmonth, endmonth, file_neutron_data)

    merged_df['PmbarN'] = merged_df['PmmrtstN'] / 0.75006156
    merged_df['Pmbar'] = mean_pressure_uragan
    merged_df['Pmmrtst'] = [round(x * 0.75006156, 2) for x in mean_pressure_uragan]

    origin_date = []
    for i in range(len(merged_df.index)):
        origin_date.append(str(merged_df['DATE'][i]).split(' ')[0] + ' ' + str(merged_df['Time'][i]))

    TA = ['-'] * len(merged_df.index)
    RH = ['-'] * len(merged_df.index)
    PR = ['-'] * len(merged_df.index)
    vaisala_data['date'] = pd.to_datetime(vaisala_data['date'])
    for i in range(len(merged_df.index)):
        for j in range(len(vaisala_data.index)):
            if vaisala_data['date'][j] == merged_df['DATE'][i] and vaisala_data['time'][j].split(':')[0] == \
                    merged_df['Time'][i].split(':')[0] \
                    and abs(int(vaisala_data['time'][j].split(':')[1]) - int(merged_df['Time'][i].split(':')[1])) <= 3:
                if TA[i] == '-':
                    TA[i] = str(
                        str(vaisala_data['TA'][j]).split('.')[0] + ',' + str(vaisala_data['TA'][j]).split('.')[1])
                if RH[i] == '-':
                    RH[i] = vaisala_data['RH'][j]
                if PR[i] == '-':
                    PR[i] = vaisala_data['PR'][j]
                vaisala_data = vaisala_data.drop(index=[j]).reset_index(drop=True)
                break

    merged_df['Tavais'] = TA
    merged_df['Rhvais'] = RH
    merged_df['Prvais '] = PR
    merged_df['DATE'] = origin_date
    del merged_df['Time']
    merged_df.to_csv(
        '{}\\{}\\DCorr_{:02}-{:02}-{:02}-{:02}.csv'.format(pathfile, styear, stday, stmonth, endday, endmonth),
        sep=';', index=False)

    vaisala_data = vaisala(stday, endday, styear, endyear, stmonth, endmonth, file_vaisala_pressure)
    vaisala_data['date'] = pd.to_datetime(vaisala_data['date'])
    cols = ['Date', 'Time']
    for i in range(4):
        cols.append('Ncor0%s' % i)
        cols.append('NcorNoise0%s' % i)
    cols.append('Pmbar')
    corr_merged_df = pd.DataFrame(
        np.array([merge_utc['DATE'].astype(object), merge_utc['time'], corr_N[0], corr_N_noise[0],
                  corr_N[1],
                  corr_N_noise[1], corr_N[2], corr_N_noise[2],
                  corr_N[3], corr_N_noise[3], mean_pressure_uragan]).T, columns=cols)

    # if len(corr_merged_df.index) == len(vaisala_data.index):
    #     corr_merged_df['Tavais'] = vaisala_data['TA']
    # else:
    TA = ['-'] * len(corr_merged_df.index)
    for i in range(len(corr_merged_df.index)):
        for j in range(len(vaisala_data.index)):
            if vaisala_data['date'][j] == corr_merged_df['Date'][i] and vaisala_data['time'][j].split(':')[0] == \
                    corr_merged_df['Time'][i].split(':')[0] \
                    and abs(
                int(vaisala_data['time'][j].split(':')[1]) - int(corr_merged_df['Time'][i].split(':')[1])) <= 3:
                if TA[i] == '-':
                    TA[i] = str(
                        str(vaisala_data['TA'][j]).split('.')[0] + ',' + str(vaisala_data['TA'][j]).split('.')[1])
                vaisala_data = vaisala_data.drop(index=[j]).reset_index(drop=True)
                break
    corr_merged_df['Tavais'] = TA
    corr_merged_df['Date'] = origin_date
    del corr_merged_df['Time']
    corr_merged_df.to_csv(
        '{}\\{}\\NDATA_Temp_All_{:02}-{:02}-{:02}-{:02}.csv'.format(pathfile, styear, stday, stmonth, endday, endmonth),
        sep=';', index=False)
