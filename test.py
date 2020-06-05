import numpy as np
import probutil.prob as pb

# make a discrete probability distribution (DPB) from a dictionary
d = pb.dpb({1:0.1, 2:0.5, 3:0.3, 4:0.1})
# print a DPB
print(d)
# you can create a DPB with a name
d = pb.dpb({1:0.1, 2:0.5, 3:0.3, 4:0.1}, "with a name")
# print a DPB shows its name
print(d)
# make a uniform DPB with a range
d = pb.dpb(range(5), "uniform with a range")
print(d)
# make a random DPB with a range
d = pb.dpb(range(5), "random with a range", True)
print(d)
# make a uniform DPB with a set
d = pb.dpb({1, 3, 5}, "uniform with a set")
print(d)
# make a random DPB with a set
d = pb.dpb({1, 3, 5}, "random with a set", True)
print(d)
# make a DPB with a list of samples. Dups allowed
d = pb.dpb([1, 1, 1, 1, 1, 1, 2, 3, 4, 5], "with a list")
print(d)
# make a DPB with a tuple of samples. Dups allowed
d = pb.dpb((1, 1, 1, 1, 1, 1, 2, 3, 4, 5), "with a tuple")
print(d)
# make a PDB with a matrix. First row: list of values, second row: list of probabilities. Dups allowed
d = pb.dpb([[  1,   1,   3,   4,   5],
            [0.1, 0.2, 0.3, 0.2, 0.2]], "with a matrix")
print(d)
# adding two DPBs
d1 = pb.dpb({1:0.2, 2:0.3, 3:0.5}, "d1")
d2 = pb.dpb({1:0.1, 2:0.5, 3:0.4}, "d2")
d3 = d1 + d2
# d3's name is automatically set as "d1+d2"
print(d3)
# you can set another name
d3.setname("d3")
print(d3)
# adding a DPB and a constant
d3 = d1 + 1
d4 = 3 + d1
print(d3)
print(d4)
# subtract
d3 = d1 - d2
print(d3)
d3 = 10 - d1
print(d3)

d1 = pb.dpb([1, 1, 1, 1, 2, 2, 3, 4, 5, 6, 7, 8, 9, 10], "d1")
print(d1)

# how to do element-wise operation for a distribution

# get raw values list and probabilities list
vs, ps = d1.raw()
# convert values list to numpy array
vs = np.array(vs)
# use numpy element-wise operations
vs = list(np.ceil(vs / 3) * 5 - vs)
# make a new probability distribution
d2 = pb.dpb([vs, ps], "d2")
print(d2)
