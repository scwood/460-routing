from __future__ import print_function

import sys

sys.path.append('..')

from src.sim import Sim
from src.packet import Packet

from networks.network import Network


class BroadcastApp(object):

    packet_ident = 1

    def __init__(self, node, name):
        self.node = node
        self.name = name
        self.distance_vector = {}
        self.distance_vector[self.name] = 0

    def receive_packet(self, packet):
        neighbor_vector = packet.body[0]
        neighbor_node = packet.body[1]
        modified = False
        for node_name, distance in neighbor_vector.items():
            if node_name not in self.distance_vector:
                modified = True
                self.distance_vector[node_name] = neighbor_vector[node_name] + 1
                self.node.add_forwarding_entry(address=neighbor_node.get_address(self.name),
                                               link=self.node.get_link(neighbor_node.hostname))
            elif neighbor_vector[node_name] + 1 < self.distance_vector[node_name]:
                modified = True
                self.distance_vector[node_name] = neighbor_vector[node_name] + 1
                self.node.add_forwarding_entry(address=neighbor_node.get_address(self.name),
                                               link=self.node.get_link(neighbor_node.hostname))
        print()
        print('To: {}, Packet #{}'.format(self.node.hostname, packet.ident))
        print(self.distance_vector)
        if modified:
            self.broadcast()

    def broadcast(self):
        p = Packet(
            source_address=self.node.get_address(self.name),
            destination_address=0,
            ident=BroadcastApp.packet_ident, ttl=1, protocol='dvrouting', length=100,
            body=(self.distance_vector, self.node))
        Sim.scheduler.add(delay=30, event=p, handler=self.node.send_packet)
        BroadcastApp.packet_ident += 1


def run_five_nodes_line():
    network = Network('./networks/five-nodes-line.txt')
    n1 = network.get_node('n1')
    n2 = network.get_node('n2')
    n3 = network.get_node('n3')
    n4 = network.get_node('n4')
    n5 = network.get_node('n5')
    run([(n1, 'n1'),
         (n2, 'n2'),
         (n3, 'n3'),
         (n4, 'n4'),
         (n5, 'n5')])


def run_five_nodes_ring():
    network = Network('./networks/five-nodes-ring.txt')
    n1 = network.get_node('n1')
    n2 = network.get_node('n2')
    n3 = network.get_node('n3')
    n4 = network.get_node('n4')
    n5 = network.get_node('n5')
    run([(n1, 'n1'),
         (n2, 'n2'),
         (n3, 'n3'),
         (n4, 'n4'),
         (n5, 'n5')])


def run_fifteen_nodes():
    pass


class SomeClass(object):
    def receive_packet(self, packet):
        print('stuff')


def run(nodes):
    Sim.scheduler.reset()

    apps = []
    for tuple in nodes:
        node = tuple[0]
        name = tuple[1]
        b = BroadcastApp(node, name)
        node.add_protocol(protocol="dvrouting", handler=b)
        apps.append(b)

    for app in apps:
        app.broadcast()

    
    # n1 = nodes[0][0]
    # n2 = nodes[1][0]
    # n3 = nodes[2][0]
    # n5 = nodes[4][0]
    # n1.add_forwarding_entry(address=n2.get_address('n1'), link=n1.get_link('n2'))
    # n2.add_forwarding_entry(address=n3.get_address('n2'), link=n2.get_link('n3'))
    # n3.add_forwarding_entry(address=n4.get_address('n3'), link=n3.get_link('n4'))
    # p = Packet(
    #     destination_address=n5.get_address('n1'),
    #     ident=123897, ttl=5, protocol='print', length=100)
    # thingie = SomeClass()
    # n5.add_protocol(protocol="print", handler=thingie)
    # Sim.scheduler.add(delay=1000, event=p, handler=n1.send_packet)
    # Sim.scheduler.run()


def main():
    Sim.set_debug('Node')
    run_five_nodes_line()
    run_five_nodes_ring()
    run_fifteen_nodes()


if __name__ == '__main__':
    main()
