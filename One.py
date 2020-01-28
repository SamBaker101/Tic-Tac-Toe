
import random

class Link:
    def __init__(self, source, weight, destination):
        self.source = source
        self.weight = weight
        self.destination = destination


def buildNet(input_list, output_list):
    net = []
    for input in input_list:
        for output in output_list:
           net.append(Link(input, random.uniform(0.499,0.501), output))
    return net

