# Path hack
import sys, os
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(1, os.path.abspath('..'))

from fhipe import ipe

(pp,sk, k) = ipe.setup(7)

(detB, B, Bstar, group, g1, g2) = sk
(ct1,tag1) = ipe.generateVectorX("a".encode(), 3, k, sk)
res = ipe.decrypt(pp,tag1,ct1)
print(res)

(ct2,tag2) = ipe.generateVectorY("a".encode(), bytes(3), bytes(5), k, sk)
res2 = ipe.decrypt(pp, tag2, ct2)

print(res2)
print(res2 == res)