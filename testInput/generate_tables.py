import sys, random

string_keys = ['test','jason','asdf','defg','DEADBEEF']
opt = sys.argv

if(len(opt) != 5):
	print("Expecting 4 values - length of a table, length of b table, file for a table and file for b table")
	exit(-1)

# hardcoded values
# we let the probablility attribute b.x is equal to 3 to be 0.4 (arbitraily chosen)


a_len = int(opt[1])
b_len = int(opt[2])
a_file_name = str(opt[3])
b_file_name = str(opt[4])

b_file = open(b_file_name, "w")
a_file = open(a_file_name, "w")

if(b_len % len(string_keys) != 0):
	print("Expected b table length to be divisible by "+str(len(string_keys)))
	exit(-1)

for i in range(0, int(b_len/len(string_keys))):
	for s in string_keys:
		x_val = int(random.random()*10)
		if(x_val < 4):
			x_val = 3
		else:
			x_val -= 4
		b_file.write(s+str(i)+","+str(x_val)+"\n")

for i in range(0, a_len):
	s_ind = int(b_len * random.random())
	key_app  = int(s_ind/len(string_keys))
	key_ind = s_ind % len(string_keys)

	a_file.write(string_keys[key_ind]+str(key_app)+","+str(random.random())+"\n")