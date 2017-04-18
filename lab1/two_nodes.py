from __future__ import print_function

import sys

sys.path.append('..')

from src.sim import Sim
from src.packet import Packet

from networks.network import Network


# d_trans = num_bits / rate
# total time = time sent + d_prop + d_trans


class DelayHandler(object):
    @staticmethod
    def receive_packet(packet):
        print((packet.created, packet.ident, Sim.scheduler.current_time()))


def setup_network(config_path):
    Sim.scheduler.reset()
    network = Network(config_path)
    n1 = network.get_node('n1')
    n2 = network.get_node('n2')
    n1.add_forwarding_entry(address=n2.get_address('n1'), link=n1.links[0])
    n2.add_forwarding_entry(address=n1.get_address('n2'), link=n2.links[0])
    delay_handler = DelayHandler()
    network.nodes['n2'].add_protocol(protocol='delay', handler=delay_handler)
    return n1, n2


def scenario_one():
    # (0, 1, 1.008)
    n1, n2 = setup_network('networks/two_nodes_1.txt')
    packet = Packet(destination_address=n2.get_address('n1'), ident=1,
                    protocol='delay', length=1000)
    Sim.scheduler.add(delay=0, event=packet, handler=n1.send_packet)
    Sim.scheduler.run()


def scenario_two():
    # (0, 1, 80.01)
    n1, n2 = setup_network('networks/two_nodes_2.txt')
    packet = Packet(destination_address=n2.get_address('n1'), ident=1,
                    protocol='delay', length=1000)
    Sim.scheduler.add(delay=0, event=packet, handler=n1.send_packet)
    Sim.scheduler.run()


def scenario_three():
    # (0, 1, 0.018000000000000002)
    # (0, 2, 0.026000000000000002)
    # (0, 3, 0.034)
    # (2.0, 4, 2.018)
    Sim.scheduler.reset()
    n1, n2 = setup_network('networks/two_nodes_3.txt')
    packet1 = Packet(destination_address=n2.get_address('n1'), ident=1,
                     protocol='delay', length=1000)
    packet2 = Packet(destination_address=n2.get_address('n1'), ident=2,
                     protocol='delay', length=1000)
    packet3 = Packet(destination_address=n2.get_address('n1'), ident=3,
                     protocol='delay', length=1000)
    packet4 = Packet(destination_address=n2.get_address('n1'), ident=4,
                     protocol='delay', length=1000)
    Sim.scheduler.add(delay=0, event=packet1, handler=n1.send_packet)
    Sim.scheduler.add(delay=0, event=packet2, handler=n1.send_packet)
    Sim.scheduler.add(delay=0, event=packet3, handler=n1.send_packet)
    Sim.scheduler.add(delay=2, event=packet4, handler=n1.send_packet)
    Sim.scheduler.run()


def main():
    # scenario_one()
    # scenario_two()
    scenario_three()


if __name__ == '__main__':
    main()
