
class Link:
    def __init__(self, source, weight, destination):
        self.source = source
        self.weight = weight
        self.destination = destination


def buildNet(input_list, output_list):
    net = []
    for input in input_list:
        for output in output_list:
           net.append(Link(input, 0.5, output))
    return net

