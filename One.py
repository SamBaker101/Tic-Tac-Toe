
import random

class Link:
    def __init__(self, source, weight, destination):
        self.source = source
        self.weight = weight
        self.destination = destination


def buildNet(input_list, output_list, w_range):
    net = []
    m, n = w_range
    for input in input_list:
        (xi, yi, mark) = input
        if mark == 0:
            net.append(Link(input, random.uniform(m, n), (xi, yi)))
        else:
            for output in output_list:
                if (xi, yi) != output:
                    net.append(Link(input, random.uniform(m, n), output))
    
    return net

def printNet(net):
    for link in net: print(link.source, link.weight, link.destination)

