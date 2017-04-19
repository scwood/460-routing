from __future__ import print_function

import sys
import json

sys.path.append('..')

from src.sim import Sim
from src.packet import Packet

from networks.network import Network


class BroadcastApp(object):

    packet_ident = 1

    def __init__(self, node):
        self.node = node
        self.distance_vector = {}
        self.distance_vector[self.node.hostname] = {
            'address': None,
            'cost': 0
        }
        self.times_broadcasted = 0
        self.seen_lately = {}
        self.reset_seen_lately()

    def receive_packet(self, packet):
        neighbor_name = packet.body[0]
        neighbor_distance_vector = packet.body[1]
        neighbor_addresses = packet.body[2]
        neighbor_link = self.node.get_link(neighbor_name)
        self.seen_lately[neighbor_name] = True

        for node_name, obj in neighbor_distance_vector.items():
            new_cost = obj['cost']
            new_address = obj['address']
            if new_cost is None:
                self.distance_vector[node_name] = new_cost
            elif (node_name not in self.distance_vector or
                    new_cost + 1 < self.distance_vector[node_name]['cost']):
                self.distance_vector[node_name] = obj
                self.distance_vector[node_name]['cost'] = new_cost + 1
                self.node.add_forwarding_entry(new_address, neighbor_link)
        
        neightbor_address = neighbor_addresses[self.node.hostname]
        self.distance_vector[neighbor_name]['address'] = neightbor_address
        self.node.add_forwarding_entry(neightbor_address, neighbor_link)

        print()
        print('To: {}, Packet #{}'.format(self.node.hostname, packet.ident))
        print(json.dumps(self.distance_vector, indent=2))
        self.times_broadcasted += 1

        if self.times_broadcasted == 3:
            self.detect_broken_links()
            self.broadcast()
            self.delete_broken_links()
            self.reset_seen_lately()
            self.times_broadcasted = 0
        else:
            self.broadcast()
            self.delete_broken_links()

    def reset_seen_lately(self):
        for link in self.node.links:
            self.seen_lately[link.endpoint.hostname] = False

    def detect_broken_links(self):
        for name, seen_lately in self.seen_lately.items():
            if name in self.distance_vector and not seen_lately:
                self.distance_vector[name]['cost'] = None

    def delete_broken_links(self):
        for name, obj in self.distance_vector.items():
            import math
            if obj['cost'] is None:
                del self.distance_vector[name]

    def broadcast(self):
        addresses = {}
        for link in self.node.links:
            addresses[link.endpoint.hostname] = link.address
        p = Packet(
            source_address=self.node.get_address(self.node.hostname),
            destination_address=0,
            ident=BroadcastApp.packet_ident, ttl=1, protocol='dvrouting', length=100,
            body=(self.node.hostname, self.distance_vector, addresses))
        Sim.scheduler.add(delay=30, event=p, handler=self.node.send_packet)
        BroadcastApp.packet_ident += 1


def run_five_nodes_line():
    network = Network('./networks/five-nodes-line.txt')
    n1 = network.get_node('n1')
    n2 = network.get_node('n2')
    n3 = network.get_node('n3')
    n4 = network.get_node('n4')
    n5 = network.get_node('n5')
    run([n1, n2, n3, n4, n5])


def run_five_nodes_ring():
    network = Network('./networks/five-nodes-ring.txt')
    n1 = network.get_node('n1')
    n2 = network.get_node('n2')
    n3 = network.get_node('n3')
    n4 = network.get_node('n4')
    n5 = network.get_node('n5')
    run([n1, n2, n3, n4, n5])


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
    run([n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15])


class PrintingApp(object):
    def receive_packet(self, packet):
        print('Printing things!' + 4)
        a['asdf']


def run(nodes):
    Sim.scheduler.reset()

    apps = []
    for node in nodes:
        b = BroadcastApp(node)
        node.add_protocol(protocol="dvrouting", handler=b)
        apps.append(b)

    for app in apps:
        app.broadcast()

    
    n1 = nodes[0]
    n3 = nodes[2]
    n4 = nodes[3]
    n5 = nodes[4]
    p = Packet(
        destination_address=5,
        ident=123897, ttl=5, protocol='print', length=100)
    printing_app = PrintingApp()
    n3.add_protocol(protocol='print', handler=printing_app)

    Sim.scheduler.add(delay=200, event=p, handler=n1.send_packet)
    # Sim.scheduler.add(delay=100, event=None, handler=n4.get_link('n1').up)

    Sim.scheduler.run()

def main():
    Sim.set_debug('Node')
    # run_five_nodes_line()
    run_five_nodes_ring()
    # run_fifteen_nodes()


if __name__ == '__main__':
    main()
