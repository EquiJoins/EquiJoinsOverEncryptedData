import sys, os
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(1, os.path.abspath('..'))

from fhipe import ipe
from timeit import default_timer as timer

#Query being run is
# SELECT * FROM a, b WHERE b.x = 3

def inner_join(a_table,b_table):
	ret = ''
	count = 0;
	a_enc_attributes = [];
	b_enc_attributes = [];
	a_pt_attributes = [];
	b_pt_attributes = [];
	(pp,sk, k) = ipe.setup(7);

	b_row = b_table.readline().rstrip()
	while(b_row != ''):
		b_values = b_row.split(',');

		(ct2,tag2) = ipe.generateVectorY(b_values[0].rstrip().encode(), b_values[1].rstrip(), str(3), k, sk)

		b_enc_attributes.append((tag2,ct2))
		b_pt_attributes.append(b_values);

		b_row = b_table.readline().rstrip()

	a_row = a_table.readline().rstrip()
	while(a_row != ''):
		a_values = a_row.split(',');
		(ct1,tag1) = ipe.generateVectorX(a_values[0].rstrip().encode(), 3, k, sk)
		a_pt_attributes.append(a_values);
		a_enc_attributes.append((ct1,tag1))
		a_row = a_table.readline().rstrip()

	start = timer()

	for x in range(0,len(a_pt_attributes)):
		(tag2, ct2) = a_enc_attributes[x];
		for y in range(0,len(b_pt_attributes)):
			(tag1, ct1) = b_enc_attributes[y];
			if(ipe.decrypt(pp, tag2, ct2) == ipe.decrypt(pp, tag1, ct1)):
				count=count+1;
	end = timer();
	print(count)
	print(str(end - start)+"\n")

opt = sys.argv
if(len(opt) != 3):
	print("Expecting 2 input tables")
	exit(-1)

inner_join(open(opt[1]),open(opt[2]))