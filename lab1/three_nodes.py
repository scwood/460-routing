from __future__ import print_function

import sys

sys.path.append('..')

from src.sim import Sim
from src.packet import Packet

from networks.network import Network




class DelayHandler(object):
    @staticmethod
    def receive_packet(packet):
        print((packet.ident, packet.created, Sim.scheduler.current_time()))


def setup_network(config_path):
    Sim.scheduler.reset()
    # Sim.set_debug('Node')
    network = Network(config_path)
    n1 = network.get_node('n1')
    n2 = network.get_node('n2')
    n3 = network.get_node('n3')
    n1.add_forwarding_entry(address=n2.get_address('n1'), link=n1.links[0])
    n1.add_forwarding_entry(address=n3.get_address('n2'), link=n1.links[0])
    n2.add_forwarding_entry(address=n1.get_address('n2'), link=n2.links[0])
    n2.add_forwarding_entry(address=n3.get_address('n2'), link=n2.links[1])
    n3.add_forwarding_entry(address=n1.get_address('n2'), link=n3.links[0])
    n3.add_forwarding_entry(address=n2.get_address('n3'), link=n3.links[0])
    delay_handler = DelayHandler()
    network.nodes['n3'].add_protocol(protocol='delay', handler=delay_handler)
    return n1, n2, n3


def scenario_one_100mbps():
    # (0, 1, 2.016)
    transmission_delay = 0.008
    n1, n2, n3 = setup_network('networks/three_nodes_1_1Mbps.txt')
    for i in range(1000):
        packet = Packet(destination_address=n3.get_address('n2'), ident=i+1,
                        protocol='delay', length=1000)
        Sim.scheduler.add(delay=i*transmission_delay,
                          event=packet, handler=n1.send_packet)
    Sim.scheduler.run()


def scenario_one_1gbps():
    # (0, 1, 2.016)
    transmission_delay = 0.000008
    n1, n2, n3 = setup_network('networks/three_nodes_1_1Gbps.txt')
    for i in range(1000):
        packet = Packet(destination_address=n3.get_address('n2'), ident=i+1,
                        protocol='delay', length=1000)
        Sim.scheduler.add(delay=i*transmission_delay,
                          event=packet, handler=n1.send_packet)
    Sim.scheduler.run()


def scenario_two():
    transmission_delay = 0.008
    n1, n2, n3 = setup_network('networks/three_nodes_2.txt')
    for i in range(1000):
        packet = Packet(destination_address=n3.get_address('n2'), ident=i+1,
                        protocol='delay', length=1000)
        Sim.scheduler.add(delay=i*transmission_delay,
                          event=packet, handler=n1.send_packet)
    Sim.scheduler.run()


def main():
    # scenario_one_100mbps()
    # scenario_one_1gbps()
    scenario_two()


if __name__ == '__main__':
    main()
