
import random

class Link:
    def __init__(self, source, weight, destination):
        self.source = source
        self.weight = weight
        self.destination = destination


def buildNet(input_list, output_list):
    net = []
    for input in input_list:
        (xi, yi, mark) = input
        if mark == 0:
            net.append(Link(input, random.uniform(0.499,0.501), (xi, yi)))
        else:
            for output in output_list:
                if (xi, yi) != output:
                    net.append(Link(input, random.uniform(0.499,0.501), output))
    
    return net

def printNet(net):
    for link in net: print(link.source, link.weight, link.destination)