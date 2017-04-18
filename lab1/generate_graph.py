import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


class Plotter:
    def __init__(self):
        plt.style.use('ggplot')
        pd.set_option('display.width', 1000)

    def linePlot(self):
        data = pd.read_csv('./queueing_delay/averages.csv')
        plt.figure()
        ax = data.plot(x='Queueing Delay', y='Utilization')
        ax.set_xlabel('Utilization')
        ax.set_ylabel('Queueing Delay (ms)')
        fig = ax.get_figure()
        service = (1000.0*8)/1000000
        mu = 1.0/service
        rho = np.arange(0, 1, 1.0/100)
        plt.plot(rho, (1/(2*mu))*(rho/(1-rho)), label='Theory', color='green')
        plt.legend()
        fig.savefig('line.png')


if __name__ == '__main__':
    p = Plotter()
    p.linePlot()
