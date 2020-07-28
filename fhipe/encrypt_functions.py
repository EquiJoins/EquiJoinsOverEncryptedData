def encrypt_row(vec_size, target_values, sk, row_values, k, join_val):
	assert(len(target_values) == len(row_values))
	padding = []
	for i in target_values:
		padding.append(0)
	padding.append(0)

	(pp,sk, k) = ipe.setup(len(target_values)+4);

	if(len(target_values) == 0):
		(ct1,tag1) = ipe.generateVectorX(a_values[0].rstrip().encode(), 3, k, sk, padding)
		return (ct1,tag1)

	b_row = b_table.readline().rstrip()
	while(b_row != ''):
		b_values = b_row.split(',');

		(ct2,tag2) = ipe.generateVectorY(b_values[0].rstrip().encode(), 
			[b_values[1].rstrip(),str(4),str(1)], target_values, k, sk)

		b_enc_attributes.append((tag2,ct2))
		b_pt_attributes.append(b_values);

		b_row = b_table.readline().rstrip()

	a_row = a_table.readline().rstrip()
	while(a_row != ''):
		a_values = a_row.split(',');
		(ct1,tag1) = ipe.generateVectorX(a_values[0].rstrip().encode(), 3, k, sk, padding)
		a_pt_attributes.append(a_values);
		a_enc_attributes.append((ct1,tag1))
		a_row = a_table.readline().rstrip()
def encrypt_table(table, target_values, indicies):
	