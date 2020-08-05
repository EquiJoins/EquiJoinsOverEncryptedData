from fhipe import ipe
from timeit import default_timer as timer
import multiprocessing,resource
import sys

#Thread that queries all rows of the B table for a row that meets the join predicate and has the
# matching join attribute
def indexesMatch(target, indicies, row):
	for t in range(0,len(indicies)):
		if(target[t] != row[indicies[t]-1]):
			print(str(target[t])+","+str(row[indicies[t]-1]))
			return False;
	return True;
#Writes to a queue the index of the table with the matching join attribute or -1 otherwise
def join_b_thread(pp, tag2, ct2, b_pt_attributes, b_enc_attributes, q, count, target, indicies):
	for y in range(0,len(b_pt_attributes)):
			if(indexesMatch(target, indicies, b_pt_attributes[y])):
				(tag1, ct1) = b_enc_attributes[y];
				if(ipe.decrypt(pp, tag2, ct2) == ipe.decrypt(pp, tag1, ct1)):
					q.put(count);
	q.put(-1);

# Function that handles the inner join, takes in a vector of encrypted attributes and plaintext 
# attributes
def inner_join(a_enc_attributes,a_pt_attributes,b_enc_attributes,b_pt_attributes,pp, target, indicies):
	ret = []
	threads = [];
	queues = [];

	#This is the actual join code
	for x in range(0,len(a_pt_attributes)):
		(tag2, ct2) = a_enc_attributes[x];
		q = multiprocessing.Queue()
		threads.append(
			multiprocessing.Process(
				target=join_b_thread,args=(pp, tag2, ct2,b_pt_attributes,b_enc_attributes,q,x, target, indicies)));
		queues.append(q);
	start = timer()	
	for t in threads:
		t.start();
	for q in queues:
		ret.append(q.get())
	for t in threads:
		t.join();
	end = timer();
	#print((ret))
	print("Total memory used "+str(sys.getsizeof(a_enc_attributes)+sys.getsizeof(b_enc_attributes)+sys.getsizeof(a_pt_attributes)+sys.getsizeof(b_pt_attributes))+"bytes")
	print("Peak memory usage "+str(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/resource.getpagesize()))
	print(str(end - start)+"\n")
	print(ret)