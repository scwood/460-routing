from __future__ import print_function

import sys

sys.path.append('..')

from src.sim import Sim
from src.packet import Packet

from networks.network import Network

import random


class Generator(object):
    def __init__(self, node, destination, load, duration):
        self.node = node
        self.load = load
        self.destination = destination
        self.duration = duration
        self.start = 0
        self.ident = 1

    def handle(self, event):
        now = Sim.scheduler.current_time()
        if (now - self.start) > self.duration:
            return
        self.ident += 1
        p = Packet(destination_address=self.destination, ident=self.ident,
                   protocol='delay', length=1000)
        Sim.scheduler.add(delay=0, event=p, handler=self.node.send_packet)
        Sim.scheduler.add(delay=random.expovariate(self.load),
                          event='generate', handler=self.handle)


class DelayHandler(object):

    def __init__(self, out_file):
        self.out_file = out_file

    def receive_packet(self, packet):
        self.out_file.write(str(packet.queueing_delay) + '\n')


def setup_network(config_path):
    Sim.scheduler.reset()
    network = Network(config_path)
    n1 = network.get_node('n1')
    n2 = network.get_node('n2')
    n1.add_forwarding_entry(address=n2.get_address('n1'), link=n1.links[0])
    n2.add_forwarding_entry(address=n1.get_address('n2'), link=n2.links[0])
    return network, n1, n2


def main():
    max_rate = 1000000 // (1000 * 8)
    values = [.1, .2, .3, .4, .5, .6, .7, .8, .9, .95, .98]
    for value in values:
        network, n1, n2 = setup_network('networks/queueing_theory.txt')
        delay_handler = DelayHandler(
            open('./queueing_delay/{}.txt'.format(value), 'w'))
        network.nodes['n2'].add_protocol(protocol="delay",
                                         handler=delay_handler)
        load = value * max_rate
        g = Generator(node=n1, destination=n2.get_address('n1'), load=load,
                      duration=10)
        Sim.scheduler.add(delay=0, event='generate', handler=g.handle)
        Sim.scheduler.run()


if __name__ == '__main__':
    main()
