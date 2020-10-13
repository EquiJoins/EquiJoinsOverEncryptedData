import sys,os
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(1, os.path.abspath('..'))

from charm.toolbox.pairinggroup import ZR
from fhipe import ipe
import csv

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
def hash_based_join(table_a_file, a, x, x_c, table_b_file, b, y, y_c):
  (pp, msk) = ipe.setup(6)
  (detB, B, Bstar, group, g1, g2) = msk

  table_a = read_table(table_a_file)
  table_b = read_table(table_b_file)

  k = group.random(ZR)
  k_a = ipe.encryptQuery(msk, k, x_c)
  k_b = ipe.encryptQuery(msk, k, y_c)

  encrypted_table_a = ipe.encryptTable(msk, table_a, a, x)
  encrypted_table_b = ipe.encryptTable(msk, table_b, b, y)
  hash_table = {ipe.decrypt(pp, k_a, c_a):0 for c_a in encrypted_table_a}

  count = 0
  for c_b in encrypted_table_b:
    if ipe.decrypt(pp, k_b, c_b) in hash_table:
      count += 1

  return count

table_a_file = "table_a.in"
a = "a_id" 
x = "a_val"
x_c = "1" 

table_b_file = "table_b.in"
b = "a_id"
y = "b_val"
y_c = "1" 

count = hash_based_join(table_a_file, a, x, x_c, table_b_file, b, y, y_c)
print('{} resulting rows.'.format(count))
