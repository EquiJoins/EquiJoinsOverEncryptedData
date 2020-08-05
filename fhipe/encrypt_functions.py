import ipe
#Encrypt row function
# Takes in the matrix length, an array of target values, a secret key, the attributes in a row, 
#  a random value used for generating the join tag, the actual join attribute of the row

# outputs a ciphertext and tag pair
def encrypt_row(matrix_len, target_values, sk, row_values, k, join_val):
	assert(len(target_values) == len(row_values))
	padding = []
	for i in range(len(target_values), matrix_len):
		padding.append(0)
	padding.append(0)

	if(len(target_values) == 0):
		(ct1,tag1) = ipe.generateVectorX(join_val, 0, k, sk, padding)
		return (ct1,tag1)
	else:
		(ct2,tag2) = ipe.generateVectorY(join_val, 
			row_values, target_values, k, sk)
		return (ct2,tag2)
#Encrypt row function
# Takes in the matrix length, the 2d array that represents a table, an array of target value
# an array of indicies corresponding to the attributes of the tables that the target values are from,
# a secret key, a random value for generating the join tag

# outputs a pair of lists, one is a list of pairs of ciphertext and tag pairs, the other is an array of
# the plaintext attributes in the table
def encrypt_table(matrix_len, table, target_values, indicies, sk, k):
	enc_attributes = [];
	pt_attributes = [];
	table_row = table.readline().rstrip()

	while(table_row != ''):
		table_values = table_row.split(',');
		row_attributes = []
		if(len(target_values) > 0):
			row_attributes = [table_values[i].rstrip() for i in indicies]

		(tag,ct) = encrypt_row(matrix_len, target_values, sk, row_attributes, k, table_values[0].rstrip().encode())

		enc_attributes.append((tag,ct))
		pt_attributes.append(row_attributes);

		table_row = table.readline().rstrip()
	return (enc_attributes,pt_attributes)