"""
Copyright (c) 2016, Kevin Lewi
 
Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.
"""

"""
Implementation of function-hiding inner product encryption (FHIPE).
"""

import sys, os, math, random

# Path hack
sys.path.insert(0, os.path.abspath('charm'))
sys.path.insert(1, os.path.abspath('../charm'))

from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
from subprocess import call, Popen, PIPE
from numpy.polynomial import polynomial as P
import numpy as np

def setup(n, group_name = 'MNT159', simulated = False):
  """
  Performs the setup algorithm for IPE.
  
  This function samples the generators from the group, specified optionally by 
  "group_name". This variable must be one of a few set of strings specified by 
  Charm.

  Then, it invokes the C program ./gen_matrices, which samples random matrices 
  and outputs them back to this function. The dimension n is supplied, and the 
  prime is chosen as the order of the group. Additionally, /dev/urandom is 
  sampled for a random seed which is passed to ./gen_matrices.

  Finally, the function constructs the matrices that form the secret key and 
  publishes the pulbic marapeters and secret key (pp, sk).
  """

  group = PairingGroup(group_name)
  g1 = group.random(G1)
  g2 = group.random(G2)
  k = group.random(ZR)

  assert g1.initPP(), "ERROR: Failed to init pre-computation table for g1."
  assert g2.initPP(), "ERROR: Failed to init pre-computation table for g2."
  
  proc = Popen(
    [
      os.path.dirname(os.path.realpath(__file__)) + '/gen_matrices',
      str(n),
      str(group.order()),
      "1" if simulated else "0",
      ""
    ],
    stdout=PIPE
  )
  detB_str = proc.stdout.readline().decode()
  B_str = proc.stdout.readline().decode()
  Bstar_str = proc.stdout.readline().decode()

  detB = int(detB_str)
  B = parse_matrix(B_str, group)
  Bstar = parse_matrix(Bstar_str, group)

  pp = ()
  sk = (detB, B, Bstar, group, g1, g2)
  return (pp, sk, k)

def keygen(sk, x): #outputs the token
  """
  Performs the keygen algorithm for IPE. note that k1 is a vector
  """

  (detB, B, Bstar, group, g1, g2) = sk
  n = len(x)
  alpha = 1

  k1 = [0] * n
  for j in range(n):
    sum = 0
    for i in range(n):
      sum += x[i] * B[i][j]
    k1[j] = alpha * sum

  for i in range(n):
    k1[i] = g1 ** k1[i]
  
  k2 = (g1 ** alpha) ** detB
  
  return (k1, k2)
  
def encrypt(sk, x): #outputs cipher
  """
  Performs the encrypt algorithm for IPE.
  """

  (detB, B, Bstar, group, g1, g2) = sk
  n = len(x)
  beta = 1

  c1 = [0] * n
  for j in range(n):
    sum = 0
    for i in range(n):
      sum += x[i] * Bstar[i][j]
    c1[j] = beta * sum
  
  for i in range(n):
    c1[i] = g2 ** c1[i]

  c2 = g2 ** beta

  return (c1, c2)

def decrypt(pp, skx, cty, max_innerprod = 100):
  """
  Performs the decrypt algorithm for IPE on a secret key skx and ciphertext cty. 
  The output is the inner product <x,y>, so long as it is in the range 
  [0,max_innerprod].
  """

  (k1, k2) = skx
  (c1, c2) = cty
  
  t1 = innerprod_pair(c1, k1)
  t2 = pair(c2,k2)
  return t1

def parse_matrix(matrix_str, group):
  """
  Parses the matrix as output from the call to ./gen_matrices.

  The first number is the number of rows, and the second number is the number 
  of columns. Then, the entries of the matrix follow. These are stored and 
  returned as a matrix.

  This function also needs the pairing group description to be passed in as a 
  parameter.
  """
  L = matrix_str.split(" ")
  rows, cols = int(L[0]), int(L[1])
  A = [[0]*cols for _ in range(rows)]
  L = L[3:]
  assert rows == cols
  assert len(L) == rows * cols
  for i in range(len(L)):
    A[int(i / rows)][i % rows] = group.init(ZR, int(L[i]))
  return A

def innerprod_pair(x, y):
  """
  Computes the inner product of two vectors x and y "in the exponent", using 
  pairings.
  """

  assert len(x) == len(y)
  L = map(lambda i: pair(x[i], y[i]), range(len(x)))
  ret = 1
  for i in L:
    ret *= i
  return ret

def solve_dlog_naive(g, h, dlog_max):
  """
  Naively attempts to solve for the discrete log x, where g^x = h, via trial and 
  error. Assumes that x is at most dlog_max.
  """

  for j in range(dlog_max):
    if g ** j == h:
      return j
  return -1

def solve_dlog_bsgs(g, h, dlog_max):
  """
  Attempts to solve for the discrete log x, where g^x = h, using the Baby-Step 
  Giant-Step algorithm. Assumes that x is at most dlog_max.
  """

  alpha = int(math.ceil(math.sqrt(dlog_max))) + 1
  g_inv = g ** -1
  tb = {}
  for i in range(alpha + 1):
    tb[(g ** (i * alpha)).__str__()] = i
    for j in range(alpha + 1):
      s = (h * (g_inv ** j)).__str__()
      if s in tb:
        i = tb[s]
        return i * alpha + j
  return -1

def generateVectorX(a, x, k, sk, padding):
  (detB, B, Bstar, group, g1, g2) = sk

  hash_a = group.hash(a)
  enc_input = [hash_a, group.random(ZR),0]+padding #seems to be an issue with the random element
  key_gen_input = [k, 0, group.random(ZR)]+padding #If I set it to a constant value then it is fine otherwise it will not be fine
  encr_results = encrypt(sk,enc_input)
  return (encr_results, keygen(sk,key_gen_input))

def generatePolynomial(x):
  new_poly = [1];
  x = [ -1 * i for i in x]
  for i in x:
    if len(new_poly) == 1:
      new_poly.append(i)
    else:
      add_poly = [i * j for j in new_poly]
      # print("add poly is "+str(add_poly))
      # print(new_poly)
      new_poly.append(add_poly[len(add_poly)-1]) #shift the existing elements forward
      # print("Added "+str(add_poly[len(add_poly)-1])+" to new poly")
      # print(new_poly)
      for j in range(0, len(add_poly)-1):
        # print("Added "+str(add_poly[j])+"to new poly at index "+str(j + 1))
        new_poly[(j + 1)] += add_poly[j]
    # print(new_poly)
  return new_poly

def generateVectorY(b,x_q, x, k, sk):

  (detB, B, Bstar, group, g1, g2) = sk

  hash_b = group.hash(b)
  hash_xq = [group.hash(i) for i in x_q]
  hash_x = [group.hash(i) for i in x]

  p_x = generatePolynomial(hash_xq)

  enc_input =  [hash_b]
  #, hash_x**3, hash_x**2, hash_x, 1        , group.random(ZR),0]
  for i in range(len(hash_xq),0,-1):
    s = 0
    for j in hash_x:
      s += j**i
    enc_input.append(s)
  enc_input.append(len(hash_x))

  key_gen_input = [k]
  #,         0,         0,     -1, hash_xq  , 0               , group.random(ZR)]
  for i in p_x:
    key_gen_input.append(i)

  key_gen_input.append(0)
  key_gen_input.append(group.random(ZR))

  enc_input.append(group.random(ZR))
  enc_input.append(0)

  return (encrypt(sk,enc_input), keygen(sk,key_gen_input))


# def encryptRow(row,x_q, x, k, sk, padding):
#   (detB, B, Bstar, group, g1, g2) = sk

#   hash_b = group.hash(b)
#   hash_xq = [group.hash(i) for i in x_q]

#   enc_input =  [hash_b]
#   #, hash_x**3, hash_x**2, hash_x, 1        , group.random(ZR),0]
#   for i in range(len(hash_x),0,-1):
#     s = 0
#     for j in hash_xq:
#       s += j**i
#     enc_input.append(s)
#   enc_input.append(len(hash_xq))

#   enc_input.append(group.random(ZR))
#   enc_input.append(0)

#   return (encrypt(sk,enc_input))

# def keyGen:
#   (detB, B, Bstar, group, g1, g2) = sk
#   key_gen_input = [k]
#   #,         0,         0,     -1, hash_xq  , 0               , group.random(ZR)]
#   hash_x = [group.hash(i) for i in x]
#   p_x = generatePolynomial(hash_x)

#   for i in p_x:
#     key_gen_input.append(i)

#   key_gen_input.append(0)
#   key_gen_input.append(group.random(ZR))