import probutil.prob as pb

d1 = pb.dpb(range(5), "d1")
d2 = pb.dpb(range(3), "d2")
d3 = pb.dpb([1.1, 2.2, 3.3], "d3") 
print(pb.pbceil(d3))
d4 = pb.pbmax(d1, d2) + pb.pbceil(d3) + d1 + d2 - 3
print(d1)
print(d2)
print(d3)
print(d4)
