from scipy.optimize import curve_fit
def linear(x, a, b):
    return a * x + b

def finding_koefs():
    fig, axs = plt.subplots(figsize=(18, 18), nrows=4, sharex=True)
    bar_koef = []
    N_0 = []
    for i in range(1, 5):
        ax=axs[i-1]
        ax.set_title('Детектор %s' %i, fontsize=18, loc='left')
        if i == 5:
            ax.set_xlabel('Давление', fontsize=20)
        ax.set_ylabel(r'$Cкорость счета, (300с)^{-1}$', fontsize=15)
    #     ax.set_ylim([0,500])
    #     ax.set_xlim([0,df.index.max()])
        if len(df[df['Nn%s'  % i] == 0]) != 0:
            test = []
            for j in df[df['Nn%s'  % i] != 0].index.tolist():
                test.append(mean_result[j])
            ax.scatter([x-993 for x in test], df[df['Nn%s'  % i] != 0]['Nn%s'  % i], label='N%s' % i, s=5)
            param, param_cov = curve_fit(linear, [x-993 for x in test], df[df['Nn%s'  % i] != 0]['Nn%s'  % i])
            fit_line = [y*param[0] + param[1] for y in  [x-993 for x in test]]
            ax.scatter([x-993 for x in test], fit_line, s = 6)
            bar_koef.append(param[0]/param[1]*100)
            N_0.append(param[1])
        else:
            ax.scatter([x-993 for x in mean_result], df['Nn%s'  % i], label='N%s' % i, s=5)
            param, param_cov = curve_fit(linear, [x-993 for x in mean_result], df['Nn%s'  % i])
            fit_line = [y*param[0] + param[1] for y in  [x-993 for x in mean_result]]
            ax.scatter([x-993 for x in mean_result], fit_line, s = 6)
            bar_koef.append(param[0]/param[1]*100)
            N_0.append(param[1])