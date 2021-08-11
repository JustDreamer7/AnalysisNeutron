import os

import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

from change_pressure_interval import change_pressure_interval
from concat_utc import concat_utc


# функция для фита графика скорости счета к разности давлений
def linear(x, a, b):
    return a * x + b


def First_Proccessing(stday, stmonth, styear, endday, endmonth, endyear, path, pathpic, pathfile, file1cl, file2cl, ):
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

    merge_utc = concat_utc(stday, endday, styear, endyear, stmonth, endmonth, file1cl)

    mean_pressure_uragan = change_pressure_interval(stday, endday, styear, endyear, stmonth, endmonth, file2cl)

    fig, axs = plt.subplots(figsize=(18, 18), nrows=4, sharex=True)
    N_bar_koef = []
    N_0 = []
    for i in range(1, 5):
        ax = axs[i - 1]
        ax.set_title('Детектор %s' % i, fontsize=18, loc='left')
        if i == 5:
            ax.set_xlabel('Давление', fontsize=20)
        ax.set_ylabel(r'$Cкорость счета, (300с)^{-1}$', fontsize=15)
        #     ax.set_ylim([0,500])
        #     ax.set_xlim([0,df.index.max()])
        if len(merge_utc[merge_utc['Nn%s' % i] == 0]) != 0:
            test = []
            for j in merge_utc[merge_utc['Nn%s' % i] != 0].index.tolist():
                test.append(mean_pressure_uragan[j])
            ax.scatter([x - 993 for x in test], merge_utc[merge_utc['Nn%s' % i] != 0]['Nn%s' % i], label='N%s' % i, s=5)
            param, param_cov = curve_fit(linear, [x - 993 for x in test],
                                         merge_utc[merge_utc['Nn%s' % i] != 0]['Nn%s' % i])
            fit_line = [y * param[0] + param[1] for y in [x - 993 for x in test]]
            ax.scatter([x - 993 for x in test], fit_line, s=6)
            N_bar_koef.append(param[0] / param[1] * 100)
            N_0.append(param[1])
        else:
            ax.scatter([x - 993 for x in mean_pressure_uragan], merge_utc['Nn%s' % i], label='N%s' % i, s=5)
            param, param_cov = curve_fit(linear, [x - 993 for x in mean_pressure_uragan], merge_utc['Nn%s' % i])
            fit_line = [y * param[0] + param[1] for y in [x - 993 for x in mean_pressure_uragan]]
            ax.scatter([x - 993 for x in mean_pressure_uragan], fit_line, s=6)
            N_bar_koef.append(param[0] / param[1] * 100)
            N_0.append(param[1])

    # На случай если нужно будет добавить в график
    plt.savefig('{}\\{}\\Nn(P){}-{}-{}-{}.png'.format(pathpic, styear, stday, stmonth, endday, endmonth),
                bbox_inches='tight')

    press_for_fixed_N = []
    for i in range(4):
        press_for_fixed_N.append(
            (mean_pressure_uragan - np.mean(mean_pressure_uragan)) * N_bar_koef[i - 1] / 100 * N_0[i - 1])

    fig, axs = plt.subplots(figsize=(18, 18), nrows=4, sharex=True)
    for i in range(1, 5):
        ax = axs[i - 1]
        ax.set_title('Детектор %s' % i, fontsize=18, loc='left')
        ax0 = ax.twinx()
        ax0.set_ylim([970, 1020])
        ax0.set_ylabel('Давление, мбар', fontsize=15)
        if i == 5:
            ax.set_xlabel('Дата', fontsize=20)
        ax.set_ylabel(r'$Cкорость счета, (300с)^{-1}$', fontsize=14)
        ax.set_ylim([0, 500])
        ax.set_xlim([0, merge_utc.index.max()])
        ax.plot(merge_utc.index, merge_utc['Nn%s' % i] + press_for_fixed_N[i - 1], label='N%s' % i, linewidth=1,
                color='black')
        ax.plot(merge_utc.index, merge_utc['Nn%s' % i], label='N%s' % i, linewidth=1, color='red')
        ax0.plot(range(0, len(mean_pressure_uragan)), mean_pressure_uragan, linewidth=2, color='blue')
        ax.set_xticks(list(range(0, merge_utc.index.max(), 288 * 5)))
        ax.set_xticklabels(merge_utc['DATE'].dt.date.unique().tolist()[::5])
    plt.savefig('{}\\{}\\Nn300c_without_mask{}-{}-{}-{}.png'.format(pathpic, styear, stday, stmonth, endday, endmonth),
                bbox_inches='tight')

    fig, axs = plt.subplots(figsize=(18, 18), nrows=4, sharex=True)
    N_noise_bar_koef = []
    N_noise_0 = []
    for i in range(1, 5):
        ax = axs[i - 1]
        ax.set_title('Детектор %s' % i, fontsize=18, loc='left')
        if i == 5:
            ax.set_xlabel('Давление', fontsize=20)
        ax.set_ylabel(r'$Cкорость счета шумов, (300с)^{-1}$', fontsize=14)
        #     ax.set_ylim([0,500])
        #     ax.set_xlim([0,df.index.max()])
        if len(merge_utc[merge_utc['N_noise%s' % i] == 0]) != 0:
            test = []
            for j in merge_utc[merge_utc['N_noise%s' % i] != 0].index.tolist():
                test.append(mean_pressure_uragan[j])
            ax.scatter([x - 993 for x in test], merge_utc[merge_utc['N_noise%s' % i] != 0]['N_noise%s' % i],
                       label='N%s' % i, s=5)
            param, param_cov = curve_fit(linear, [x - 993 for x in test],
                                         merge_utc[merge_utc['N_noise%s' % i] != 0]['N_noise%s' % i])
            fit_line = [y * param[0] + param[1] for y in [x - 993 for x in test]]
            ax.scatter([x - 993 for x in test], fit_line, s=6)
            N_noise_bar_koef.append(param[0] / param[1] * 100)
            N_noise_0.append(param[1])
        else:
            ax.scatter([x - 993 for x in mean_pressure_uragan], merge_utc['N_noise%s' % i], label='N%s' % i, s=5)
            param, param_cov = curve_fit(linear, [x - 993 for x in mean_pressure_uragan], merge_utc['N_noise%s' % i])
            fit_line = [y * param[0] + param[1] for y in [x - 993 for x in mean_pressure_uragan]]
            ax.scatter([x - 993 for x in mean_pressure_uragan], fit_line, s=6)
            N_noise_bar_koef.append(param[0] / param[1] * 100)
            N_noise_0.append(param[1])

    # На случай если нужно будет добавить в график
    plt.savefig('{}\\{}\\Nnoise(P){}-{}-{}-{}.png'.format(pathpic, styear, stday, stmonth, endday, endmonth),
                bbox_inches='tight')

    press_for_fixed_N_noise = []
    for i in range(4):
        press_for_fixed_N_noise.append(
            (mean_pressure_uragan - np.mean(mean_pressure_uragan)) * N_noise_bar_koef[i - 1] / 100 * N_noise_0[i - 1])

    fig, axs = plt.subplots(figsize=(18, 18), nrows=4, sharex=True)
    for i in range(1, 5):
        ax = axs[i - 1]
        ax.set_title('Детектор %s' % i, fontsize=18, loc='left')
        ax0 = ax.twinx()
        ax0.set_ylim([970, 1020])
        ax0.set_ylabel('Давление, мбар', fontsize=15)
        if i == 5:
            ax.set_xlabel('Дата', fontsize=20)
        ax.set_ylabel(r'$Cкорость счета шумов, (300с)^{-1}$', fontsize=14)
        ax.set_ylim([0, 500])
        ax.set_xlim([0, merge_utc.index.max()])
        ax.plot(merge_utc.index, merge_utc['N_noise%s' % i] + press_for_fixed_N_noise[i - 1], label='N%s' % i,
                linewidth=1,
                color='black')
        ax.plot(merge_utc.index, merge_utc['N_noise%s' % i], label='N%s' % i, linewidth=1, color='red')
        ax0.plot(range(0, len(mean_pressure_uragan)), mean_pressure_uragan, linewidth=2, color='blue')
        ax.set_xticks(list(range(0, merge_utc.index.max(), 288 * 5)))
        ax.set_xticklabels(merge_utc['DATE'].dt.date.unique().tolist()[::5])
    plt.savefig(
        '{}\\{}\\Nnoise300c_without_mask{}-{}-{}-{}.png'.format(pathpic, styear, stday, stmonth, endday, endmonth),
        bbox_inches='tight')

    for i in range(1, 5):
        N_file = merge_utc[['DATE', 'time', 'Nn%s' % i]].sort_values('Nn%s' % i, ascending=False)
        N_file.to_csv(
            '{}\\{}\\Nn{}- возрастание{}-{}-{}-{}.csv'.format(pathfile, styear, i, stday, stmonth, endday, endmonth),
            sep=';', index=False)
    for i in range(1, 5):
        N_file = merge_utc[['DATE', 'time', 'Nn%s' % i]].sort_values('Nn%s' % i)
        N_file.to_csv(
            '{}\\{}\\Nn{} - убывание{}-{}-{}-{}.csv'.format(pathfile, styear, i, stday, stmonth, endday, endmonth),
            sep=';', index=False)
    for i in range(1, 5):
        N_file = merge_utc[['DATE', 'time', 'N_noise%s' % i]].sort_values('N_noise%s' % i, ascending=False)
        N_file.to_csv(
            '{}\\{}\\N_noise{} - возрастание{}-{}-{}-{}.csv'.format(pathfile, styear, i, stday, stmonth, endday,
                                                                    endmonth), sep=';', index=False)
    for i in range(1, 5):
        N_file = merge_utc[['DATE', 'time', 'N_noise%s' % i]].sort_values('N_noise%s' % i)
        N_file.to_csv(
            '{}\\{}\\N_noise{} - убывание{}-{}-{}-{}.csv'.format(pathfile, styear, i, stday, stmonth, endday, endmonth),
            sep=';', index=False)
