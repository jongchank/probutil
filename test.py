import probutil.prob as pb

d1 = pb.dpb(range(5), "d1")
d2 = pb.dpb(range(3), "d2")
d3 = pb.dpb({1.1, 2.2, 3.3}, "d3") 
print(pb.pbceil(d3))
d4 = pb.pbmax(d1, d2) + pb.pbceil(d3) + d1 + d2 - 3
print(d1)
print(d2)
print(d3)
print(d4)
d5 = pb.dpb({1:0.2, 2:0.3, 3:0.5}, "d5")
vs, ps = d4.raw()
print(vs)
print(ps)
print(d4.dist)
print(d4.probsum())

d6 = pb.dpb([1, 1, 2, 3, 3, 3, 4, 5,5, 5])
print(d6)

d6 = pb.dpb((1, 1, 2, 3, 3, 3, 4, 5,5, 5))
print(d6)
