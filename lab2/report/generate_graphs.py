from matplotlib import pyplot
import pandas


class Plotter:
    def __init__(self):
        pyplot.style.use('ggplot')
        pandas.set_option('display.width', 2000)

    def generate_queueing_graph(self):
        data = pandas.read_csv('./queueing.csv')
        pyplot.figure()
        ax = data.plot(x='window', y='queueing delay')
        ax.set_xlabel('Window Size (bytes)')
        ax.set_ylabel('Average Queueing Delay (ms)')
        fig = ax.get_figure()
        pyplot.legend()
        pyplot.tight_layout()
        fig.savefig('queueing.png')

    def generate_throughput_graph(self):
        data = pandas.read_csv('./throughput.csv')
        pyplot.figure()
        ax = data.plot(x='window', y='throughput')
        ax.set_xlabel('Window Size (bytes)')
        ax.set_ylabel('Throughput (bits/s)')
        fig = ax.get_figure()
        pyplot.legend()
        pyplot.tight_layout()
        fig.savefig('throughput.png')

if __name__ == '__main__':
    p = Plotter()
    p.generate_queueing_graph()
    p.generate_throughput_graph()
