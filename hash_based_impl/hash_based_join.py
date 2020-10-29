import sys,os
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(1, os.path.abspath('..'))

from charm.toolbox.pairinggroup import ZR
from fhipe import ipe
import csv

IN_CLAUSE_MAX_SIZE=10

# infile contains a CSV of a database table
# returns an array of dictionaries where keys are
# the table attributes and values are strings
def read_table(infile):
  with open(infile) as f:
    return [{k: str(v) for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]

# for a query:
# SELECT * FROM A
# INNER JOIN B ON A.a = B.b
# WHERE A.x IN (x_c) AND B.y IN (y_c)
# such that a is a primary key, and b is the corresponding foreign key
# returns the count of resulting rows
def hash_based_join(pp, msk, x_c, y_c):
  k = group.random(ZR)
  k_a = ipe.encryptQuery(msk, k, x_c, IN_CLAUSE_MAX_SIZE)
  k_b = ipe.encryptQuery(msk, k, y_c, IN_CLAUSE_MAX_SIZE)

  hash_table = {ipe.decrypt(pp, k_a, c_a):pk for (pk, c_a) in encrypted_table_a}

  matches = []
  for (pk, c_b) in encrypted_table_b:
    match = hash_table.get(ipe.decrypt(pp, k_b, c_b))
    if match:
      matches.append((match, pk))
  return matches 


"""
Driver: reads in tables, encrypts tables once so that many queries can be run against it
"""
table_a_file = "table_a.in"
a = "buyer_id" 
pk_a = a
x = "gender"
x_c = ["F"] 

table_b_file = "table_b.in"
b = "buyer_id"
pk_b = "order_id"
y = "amount"
y_c = ["200"]

table_a = read_table(table_a_file)
table_b = read_table(table_b_file)

(pp, msk) = ipe.setup(3+IN_CLAUSE_MAX_SIZE+1)
(detB, B, Bstar, group, g1, g2) = msk
encrypted_table_a = ipe.encryptTable(msk, table_a, pk_a, a, x, IN_CLAUSE_MAX_SIZE)
encrypted_table_b = ipe.encryptTable(msk, table_b, pk_b, b, y, IN_CLAUSE_MAX_SIZE)

# queries
females_spending_200 = hash_based_join(pp, msk, x_c, y_c)
print('matches: {}'.format(females_spending_200))

