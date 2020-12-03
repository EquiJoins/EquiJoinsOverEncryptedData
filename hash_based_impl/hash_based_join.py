import sys,os,time
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(1, os.path.abspath('..'))

from charm.toolbox.pairinggroup import ZR
from fhipe import ipe
import csv
import timeit

IN_CLAUSE_MAX_SIZE=1
selectivity_1 = False

# infile contains a CSV of a database table
# returns an array of dictionaries where keys are
# the table attributes and values are strings
def read_table(infile, delimiter=","):
  with open(infile) as f:
    return [{k: str(v) for k, v in row.items()} for row in csv.DictReader(f, delimiter=delimiter, skipinitialspace=True)]

# for a query:
# SELECT * FROM A
# INNER JOIN B ON A.a = B.b
# WHERE A.x IN (x_c) AND B.y IN (y_c)
# such that a is a primary key, and b is the corresponding foreign key
# returns the count of resulting rows
def hash_based_join(pp, msk, encrypted_table_a, encrypted_table_b, x_c, y_c):
  decryptions = []
  (detB, B, Bstar, group, g1, g2) = msk

  k = group.random(ZR)
  k_a = ipe.encryptQuery(msk, k, x_c, IN_CLAUSE_MAX_SIZE)
  k_b = ipe.encryptQuery(msk, k, y_c, IN_CLAUSE_MAX_SIZE)

  # apply selection first: skip decryption of row if row doesn't satisfy where condition
  hash_table = {}
  for (pk, x, c_a) in encrypted_table_a:
    if len(x_c) == 0 or x in x_c:
      d_start = time.time()
      d = ipe.decrypt(pp, k_a, c_a)
      d_end = time.time()
      decryptions.append(d_end - d_start)
      hash_table[d] = pk

  matches = []
  for (pk, y, c_b) in encrypted_table_b:
    if len(y_c) != 0 and y not in y_c:
      continue

    d_start = time.time()
    d = ipe.decrypt(pp, k_b, c_b)
    d_end = time.time()
    decryptions.append(d_end - d_start)
    match = hash_table.get(d)
    if match:
      matches.append((match, pk))
  return (matches, decryptions) 


######################################### EXPERIMENTS ###########################################
# NOTE: you must add a row with column heads to the tables that you will use. one should use the
# attribute names used here: http://www.tpc.org/tpc_documents_current_versions/pdf/tpc-h_v2.17.1.pdf#page=13

def experiment_1(pp, msk, sf, iters):
  print("--------------------------- sf="+sf)
  
  table_a_file = "data/"+sf+"/customer.tbl"
  a = "custkey" 
  pk_a = a
  x = "selectivity"

  table_b_file = "data/"+sf+"/orders.tbl"
  b = "custkey"
  pk_b = "orderkey"
  y = "selectivity"

  print('starting to encrypt customer')
  table_a = read_table(table_a_file, '|')
  encrypted_table_a = ipe.encryptTable(msk, table_a, pk_a, a, x, IN_CLAUSE_MAX_SIZE)
  print('done encrypting customer')

  print('starting to encrypt orders')
  table_b = read_table(table_b_file, '|')
  encrypted_table_b = ipe.encryptTable(msk, table_b, pk_b, b, y, IN_CLAUSE_MAX_SIZE)
  print('done encrypting orders')

  print('')
  selectivity_100_results = []
  selectivity_50_results = []
  selectivity_25_results = []
  selectivity_12_5_results = []
  selectivity_1_results = []

  for i in range(iters):
    # selectivity = 1/100
    x_c = ["100"]
    y_c = ["100"]
    query_start = time.time()
    (matches, decryptions) = hash_based_join(pp, msk, encrypted_table_a, encrypted_table_b, x_c, y_c)
    query_end = time.time()
    selectivity_100_results.append(query_end - query_start)
    print('selectivity=1/100 took: {}s overall'.format(query_end - query_start))
    print('time spent NOT doing decryption: {}s'.format((query_end - query_start) - sum(decryptions)))
    print('time per decryption took: {}ms'.format((sum(decryptions) / len(decryptions)) * 1000))
    print('num matches: {}'.format(len(matches)))
    print('')

    # selectivity = 1/50
    x_c = ["50"]
    y_c = ["50"]
    query_start = time.time()
    (matches, decryptions) = hash_based_join(pp, msk, encrypted_table_a, encrypted_table_b, x_c, y_c)
    query_end = time.time()
    selectivity_50_results.append(query_end - query_start)
    print('selectivity=1/50 took: {}s overall'.format(query_end - query_start))
    print('time spent NOT doing decryption: {}s'.format((query_end - query_start) - sum(decryptions)))
    print('time per decryption took: {}ms'.format((sum(decryptions) / len(decryptions)) * 1000))
    print('num matches: {}'.format(len(matches)))
    print('')

    # selectivity = 1/25
    x_c = ["25"]
    y_c = ["25"]
    query_start = time.time()
    (matches, decryptions) = hash_based_join(pp, msk, encrypted_table_a, encrypted_table_b, x_c, y_c)
    query_end = time.time()
    selectivity_25_results.append(query_end - query_start)
    print('selectivity=1/25 took: {}s overall'.format(query_end - query_start))
    print('time spent NOT doing decryption: {}s'.format((query_end - query_start) - sum(decryptions)))
    print('time per decryption took: {}ms'.format((sum(decryptions) / len(decryptions)) * 1000))
    print('num matches: {}'.format(len(matches)))
    print('')

    # selectivity = 1/12.5
    x_c = ["12.5"]
    y_c = ["12.5"]
    query_start = time.time()
    (matches, decryptions) = hash_based_join(pp, msk, encrypted_table_a, encrypted_table_b, x_c, y_c)
    query_end = time.time()
    selectivity_12_5_results.append(query_end - query_start)
    print('selectivity=1/12.5 took: {}s overall'.format(query_end - query_start))
    print('time spent NOT doing decryption: {}s'.format((query_end - query_start) - sum(decryptions)))
    print('time per decryption took: {}ms'.format((sum(decryptions) / len(decryptions)) * 1000))
    print('num matches: {}'.format(len(matches)))
    print('')

    # selectivity = 1/1
    if selectivity_1:
      x_c = []
      y_c = []
      query_start = time.time()
      (matches, decryptions) = hash_based_join(pp, msk, encrypted_table_a, encrypted_table_b, x_c, y_c)
      query_end = time.time()
      selectivity_1_results.append(query_end - query_start)
      print('selectivity=1/1 took: {}s overall'.format(query_end - query_start))
      print('time spent NOT doing decryption: {}s'.format((query_end - query_start) - sum(decryptions)))
      print('time per decryption took: {}ms'.format((sum(decryptions) / len(decryptions)) * 1000))
      print('num matches: {}'.format(len(matches)))
      print('')
  
  # aggregations
  print('--------------- AVERAGES OVER ITERATIONS')
  print('selectivity=1/100 took: {}s on average'.format(sum(selectivity_100_results) / len(selectivity_100_results)))
  print('selectivity=1/50 took: {}s on average'.format(sum(selectivity_50_results) / len(selectivity_50_results)))
  print('selectivity=1/25 took: {}s on average'.format(sum(selectivity_25_results) / len(selectivity_25_results)))
  print('selectivity=1/12.5 took: {}s on average'.format(sum(selectivity_12_5_results) / len(selectivity_12_5_results)))
  if selectivity_1:
    print('selectivity=1/1 took: {}s on average'.format(sum(selectivity_1_results) / len(selectivity_1_results)))

  print('\n\n')


def experiment_2(in_clause_max_size, iters):
  print("--------------------------- in_clause_max_size={}".format(in_clause_max_size))
  global IN_CLAUSE_MAX_SIZE
  IN_CLAUSE_MAX_SIZE = in_clause_max_size
  (pp, msk) = ipe.setup(3+IN_CLAUSE_MAX_SIZE+1)
  
  table_a_file = "data/0.01/customer.tbl"
  a = "custkey" 
  pk_a = a
  x = "selectivity"

  table_b_file = "data/0.01/orders.tbl"
  b = "custkey"
  pk_b = "orderkey"
  y = "selectivity"

  print('starting to encrypt customer')
  table_a = read_table(table_a_file, '|')
  encrypted_table_a = ipe.encryptTable(msk, table_a, pk_a, a, x, IN_CLAUSE_MAX_SIZE)
  print('done encrypting customer')

  print('starting to encrypt orders')
  table_b = read_table(table_b_file, '|')
  encrypted_table_b = ipe.encryptTable(msk, table_b, pk_b, b, y, IN_CLAUSE_MAX_SIZE)
  print('done encrypting orders')

  print('')
  selectivity_100_results = []
  selectivity_50_results = []
  selectivity_25_results = []
  selectivity_12_5_results = []
  selectivity_1_results = []

  for i in range(iters):
    # selectivity = 1/100
    x_c = ["100"]
    y_c = ["100"]
    query_start = time.time()
    (matches, decryptions) = hash_based_join(pp, msk, encrypted_table_a, encrypted_table_b, x_c, y_c)
    query_end = time.time()
    selectivity_100_results.append(query_end - query_start)
    print('selectivity=1/100 took: {}s overall'.format(query_end - query_start))
    print('time spent NOT doing decryption: {}s'.format((query_end - query_start) - sum(decryptions)))
    print('time per decryption took: {}ms'.format((sum(decryptions) / len(decryptions)) * 1000))
    print('num matches: {}'.format(len(matches)))
    print('')

    # selectivity = 1/50
    x_c = ["50"]
    y_c = ["50"]
    query_start = time.time()
    (matches, decryptions) = hash_based_join(pp, msk, encrypted_table_a, encrypted_table_b, x_c, y_c)
    query_end = time.time()
    selectivity_50_results.append(query_end - query_start)
    print('selectivity=1/50 took: {}s overall'.format(query_end - query_start))
    print('time spent NOT doing decryption: {}s'.format((query_end - query_start) - sum(decryptions)))
    print('time per decryption took: {}ms'.format((sum(decryptions) / len(decryptions)) * 1000))
    print('num matches: {}'.format(len(matches)))
    print('')

    # selectivity = 1/25
    x_c = ["25"]
    y_c = ["25"]
    query_start = time.time()
    (matches, decryptions) = hash_based_join(pp, msk, encrypted_table_a, encrypted_table_b, x_c, y_c)
    query_end = time.time()
    selectivity_25_results.append(query_end - query_start)
    print('selectivity=1/25 took: {}s overall'.format(query_end - query_start))
    print('time spent NOT doing decryption: {}s'.format((query_end - query_start) - sum(decryptions)))
    print('time per decryption took: {}ms'.format((sum(decryptions) / len(decryptions)) * 1000))
    print('num matches: {}'.format(len(matches)))
    print('')

    # selectivity = 1/12.5
    x_c = ["12.5"]
    y_c = ["12.5"]
    query_start = time.time()
    (matches, decryptions) = hash_based_join(pp, msk, encrypted_table_a, encrypted_table_b, x_c, y_c)
    query_end = time.time()
    selectivity_12_5_results.append(query_end - query_start)
    print('selectivity=1/12.5 took: {}s overall'.format(query_end - query_start))
    print('time spent NOT doing decryption: {}s'.format((query_end - query_start) - sum(decryptions)))
    print('time per decryption took: {}ms'.format((sum(decryptions) / len(decryptions)) * 1000))
    print('num matches: {}'.format(len(matches)))
    print('')

    # selectivity = 1/1
    if selectivity_1:
      x_c = []
      y_c = []
      query_start = time.time()
      (matches, decryptions) = hash_based_join(pp, msk, encrypted_table_a, encrypted_table_b, x_c, y_c)
      query_end = time.time()
      selectivity_1_results.append(query_end - query_start)
      print('selectivity=1/1 took: {}s overall'.format(query_end - query_start))
      print('time spent NOT doing decryption: {}s'.format((query_end - query_start) - sum(decryptions)))
      print('time per decryption took: {}ms'.format((sum(decryptions) / len(decryptions)) * 1000))
      print('num matches: {}'.format(len(matches)))
      print('')
  
  # aggregations
  print('--------------- AVERAGES OVER ITERATIONS')
  print('selectivity=1/100 took: {}s on average'.format(sum(selectivity_100_results) / len(selectivity_100_results)))
  print('selectivity=1/50 took: {}s on average'.format(sum(selectivity_50_results) / len(selectivity_50_results)))
  print('selectivity=1/25 took: {}s on average'.format(sum(selectivity_25_results) / len(selectivity_25_results)))
  print('selectivity=1/12.5 took: {}s on average'.format(sum(selectivity_12_5_results) / len(selectivity_12_5_results)))
  if selectivity_1:
    print('selectivity=1/1 took: {}s on average'.format(sum(selectivity_1_results) / len(selectivity_1_results)))

  print('\n\n')


# MAIN
# experiments to test relationship between overall time and scale factor
"""
(pp, msk) = ipe.setup(3+IN_CLAUSE_MAX_SIZE+1)
experiment_1(pp, msk, "0.01", 20)
experiment_1(pp, msk, "0.02", 20)
experiment_1(pp, msk, "0.03", 20)
experiment_1(pp, msk, "0.04", 20)
experiment_1(pp, msk, "0.05", 20)
experiment_1(pp, msk, "0.06", 20)
experiment_1(pp, msk, "0.07", 20)
experiment_1(pp, msk, "0.08", 20)
experiment_1(pp, msk, "0.09", 20)
experiment_1(pp, msk, "0.1", 20)
"""

# experiments to test relationship between overall time and IN_CLAUSE_MAX_SIZE
"""
experiment_2(1, 20)
experiment_2(2, 20)
experiment_2(3, 20)
experiment_2(5, 20)
experiment_2(5, 20)
experiment_2(6, 20)
experiment_2(7, 20)
experiment_2(8, 20)
experiment_2(9, 20)
experiment_2(10, 20)
"""
