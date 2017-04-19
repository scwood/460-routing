from __future__ import print_function

import sys
import json

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
        self.distance_vector[self.name] = {
            'address': None,
            'cost': 0
        }

    def receive_packet(self, packet):
        neighbor_vector = packet.body[0]
        neighbor_node = packet.body[1]
        neighbor_link = self.node.get_link(neighbor_node.hostname)
        modified = False

        for node_name, obj in neighbor_vector.items():
            new_cost = obj['cost']
            new_address = obj['address']
            if node_name not in self.distance_vector: 
                modified = True
                self.distance_vector[node_name] = obj
                self.distance_vector[node_name]['cost'] = new_cost + 1
                self.node.add_forwarding_entry(new_address, neighbor_link)
            elif new_cost + 1 < self.distance_vector[node_name]['cost']:
                modified = True
                self.distance_vector[node_name] = obj
                self.distance_vector[node_name]['cost'] = new_cost + 1
                self.node.add_forwarding_entry(new_address, neighbor_link)
        
        neightbor_address = neighbor_node.get_address(self.name)
        self.distance_vector[neighbor_node.hostname]['address'] = neightbor_address
        self.node.add_forwarding_entry(neightbor_address, neighbor_link)

        print()
        print('To: {}, Packet #{}'.format(self.node.hostname, packet.ident))
        print(json.dumps(self.distance_vector, indent=2))
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
    network = Network('./networks/fifteen-nodes.txt')
    n1 = network.get_node('n1')
    n2 = network.get_node('n2')
    n3 = network.get_node('n3')
    n4 = network.get_node('n4')
    n5 = network.get_node('n5')
    n6 = network.get_node('n6')
    n7 = network.get_node('n7')
    n8 = network.get_node('n8')
    n9 = network.get_node('n9')
    n10 = network.get_node('n10')
    n11 = network.get_node('n11')
    n12 = network.get_node('n12')
    n13 = network.get_node('n13')
    n14 = network.get_node('n14')
    n15 = network.get_node('n15')
    run([(n1, 'n1'),
         (n2, 'n2'),
         (n3, 'n3'),
         (n4, 'n4'),
         (n5, 'n5'),
         (n6, 'n6'),
         (n7, 'n7'),
         (n8, 'n8'),
         (n9, 'n9'),
         (n10, 'n10'),
         (n11, 'n11'),
         (n12, 'n12'),
         (n13, 'n13'),
         (n14, 'n14'),
         (n15, 'n15')])



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

    
    n1 = nodes[0][0]
    n4 = nodes[3][0]
    p = Packet(
        destination_address=8,
        ident=123897, ttl=5, protocol='print', length=100)
    thingie = SomeClass()
    n4.add_protocol(protocol="print", handler=thingie)
    Sim.scheduler.add(delay=1000, event=p, handler=n1.send_packet)
    Sim.scheduler.run()


def main():
    Sim.set_debug('Node')
    # run_five_nodes_line()
    run_five_nodes_ring()
    # run_fifteen_nodes()


if __name__ == '__main__':
    main()
