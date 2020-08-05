import sys, os
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(1, os.path.abspath('..'))

from fhipe import ipe
import encrypt_functions as encrypt;
import multiThreaded_nested_loop_join as join;
opt = sys.argv
if(len(opt) != 3):
	print("Expecting 2 input tables")
	exit(-1)
indicies = [1]
target_values = [str(3)]

(pp,sk, k) = ipe.setup(len(target_values)+4);

(table_1_enc, table_1_pt) = encrypt.encrypt_table(len(target_values) , open(opt[1]),[],[], sk, k)
(table_2_enc, table_2_pt) = encrypt.encrypt_table(len(target_values) , open(opt[2]),target_values,indicies, sk, k)

join.inner_join(table_1_enc,table_1_pt,table_2_enc,table_2_pt, pp, target_values, indicies)