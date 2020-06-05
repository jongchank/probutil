import random
import math
from collections import Counter

class Discrete:
    def __init__(self, dist, name = ""):
        if not isinstance(dist, dict):
            raise TypeError("Argument should be a dictionary")
        if not math.isclose(sum(dist.values()), 1, abs_tol=0.000001):
            raise ValueError("Sum of probabilities should be one")
        self.dist = dist
        self.name = name

    def __str__(self):
        out = "-----[" + self.name + "]-----\n"
        for value, prob in sorted(self.dist.items()):
            out += "P(X = {value}) = {prob:4.2f}\n".format(value = value, prob = prob)
        return out.rstrip("\n")

    def __add__(self, other):
        a_dict = self.dist
        if isinstance(other, Discrete):
            b_dict = other.dist
            out_dict = dict()
            for a_value, a_prob in a_dict.items():                
                for b_value, b_prob in b_dict.items():                
                    out_value = a_value + b_value
                    out_prob = a_prob * b_prob
                    if out_value not in out_dict:
                        out_dict.update({out_value:out_prob}) 
                    else:
                        out_dict.update({out_value:out_dict[out_value] + out_prob})
            return Discrete(out_dict, self.name + "+" + other.name)
        else:
            return Discrete({value + other: prob for value, prob in a_dict.items()}, self.name + "+" + str(other))

    def __radd__(self, other):
        out = self + other;
        out.name = str(other) + "+" + self.name
        return out

    def __neg__(self):
        a_dict = self.dist
        return Discrete({-value: prob for value, prob in a_dict.items()}, "-" + self.name)

    def __sub__(self, other):
        out = self + (-other)
        if isinstance(other, Discrete):
            out.name = self.name + "-" + other.name
        else:
            out.name = self.name + "-" + str(other)
        return out

    def __rsub__(self, other):
        out = self + (-other)
        out.name = str(other) + "-" + self.name
        return out

    def __truediv__(self, other):
        a_dict = self.dist
        if isinstance(other, Discrete):
            raise TypeError("Division by Discrete not supported")
        else:
            return Discrete({value / other: prob for value, prob in a_dict.items()}, self.name + "/" + str(other)) 

    def __mul__(self, other):
        a_dict = self.dist
        if isinstance(other, Discrete):
            raise TypeError("Multiplication between Discretes not supported")
        else:
            return Discrete({value * other: prob for value, prob in a_dict.items()}, self.name + "*" + str(other)) 

    def __rmul__(self, other):
        out = self * other;
        out.name = str(other) + "*" + self.name
        return out

    def rvs(self, n):
        return random.choices(list(self.dist.keys()), list(self.dist.values()), k = n)

    def raw(self):
        # dictionary is not guaranteed to be sorted
        return [key for key in sorted(self.dist.keys())], [self.dist[key] for key in sorted(self.dist.keys())]

    def setname(self, name):
        self.name = name

    def quantile(self, q):
        p_sum = 0
        for value, prob in sorted(self.dist.items()):
            p_sum += prob
            if p_sum >= q:
                return value

    def median(self):
        return self.quantile(0.5)

    def mean(self):
        out = 0.0
        for value, prob in self.dist.items():
            out += value * prob
        return out

    def var(self):
        out = 0.0
        e = self.mean()
        for value, prob in self.dist.items():
            out += (value - e) ** 2 * prob
        return out

    def std(self):
        return math.sqrt(self.var())

    def probsum(self):
        return sum(self.dist.values())

def dpb(dist, name = "unknown", rand = False):
    if isinstance(dist, dict):
        if rand == True:
            raise Exception("Random distribution is not supported with a dict")
        return Discrete(dist, name)
    elif isinstance(dist, range) or isinstance(dist, set):
        if rand == True:  # random distribution
            n = len(dist)
            lst = [0] * n
            for _ in range(100):
                lst[random.randint(0, n - 1)] += 0.01 
            return Discrete(dict(zip(dist, lst)), name)
        else:   # uniform distribution
            n = len(dist)
            lst = [1 / n] * n
            return Discrete(dict(zip(dist, lst)), name)
    elif isinstance(dist, list) or isinstance(dist, tuple):
        if rand == True:
            raise Exception("Random distribution is not supported with a list or tuple")
        if ((isinstance(dist[0], list) or isinstance(dist[0], list)) and
            (isinstance(dist[1], list) or isinstance(dist[1], list))):
            if len(dist[0]) != len(dist[1]):
                raise Exception("Values list and probabilities list should be of the same length") 
            d = dict()
            for v, p in zip(dist[0], dist[1]):
                if v not in d:
                    d.update({v:p}) 
                else:
                    d.update({v:d[v] + p})
            return Discrete(d, name)
        else:
            n = len(dist)
            vs = Counter(dist).keys()
            ps = [c / n for c in Counter(dist).values()]
            return Discrete(dict(zip(vs, ps)), name)
    else:
        raise TypeError("Invalid data type: " + type(dist))

def pbmax2(prob1, prob2):
    if not isinstance(prob1, Discrete):
        raise Exception("First argument should be a Discrete object")
    a_dict = prob1.dist
    if isinstance(prob2, Discrete):
        b_dict = prob2.dist
        out_dict = dict()
        for a_value, a_prob in a_dict.items():                
            for b_value, b_prob in b_dict.items():                
                out_value = max([a_value, b_value])
                out_prob = a_prob * b_prob
                if out_value not in out_dict:
                    out_dict.update({out_value:out_prob}) 
                else:
                    out_dict.update({out_value:out_dict[out_value] + out_prob})
        return Discrete(out_dict)
    else:
        b_value = prob2
        out_dict = dict()
        for a_value, a_prob in a_dict.items():                
            out_value = max([a_value, b_value])
            out_prob = a_prob
            if out_value not in out_dict:
                out_dict.update({out_value:out_prob}) 
            else:
                out_dict.update({out_value:out_dict[out_value] + out_prob})
        return Discrete(out_dict)

def pbmax(*args):
    out = args[0]
    name = "max(" + args[0].name + ","
    for a in args[1:]:
        out = pbmax2(out, a)
        if isinstance(a, Discrete): 
            name += a.name + ","
        else:
            name += str(a) + ", "
    out.name = name.rstrip(",") + ")"
    return out 

def pbceil(prob):
    in_dict = prob.dist
    out_dict = dict()
    for in_value, in_prob in in_dict.items():
        out_value = math.ceil(in_value)
        out_prob = in_prob
        if out_value not in out_dict:
            out_dict.update({out_value: out_prob})
        else:
            out_dict.update({out_value: out_dict[out_value] + out_prob})
    return Discrete(out_dict, "ceil(" + prob.name + ")")

def main():
    print("This is main")

if __name__ == "__main__":
    main()
