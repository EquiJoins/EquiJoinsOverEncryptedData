from fhipe import ipe
from timeit import default_timer as timer
import multiprocessing,resource
import sys
#Query being run is
# SELECT * FROM a, b WHERE b.x = 3
def join_b_thread(pp, tag2, ct2, b_pt_attributes, b_enc_attributes, q, count):
	for y in range(0,len(b_pt_attributes)):
			if((b_pt_attributes[y])[0] == str(3)):
				(tag1, ct1) = b_enc_attributes[y];
				if(ipe.decrypt(pp, tag2, ct2) == ipe.decrypt(pp, tag1, ct1)):
					q.put(count);
	q.put(-1);
def inner_join(a_enc_attributes,a_pt_attributes,b_enc_attributes,b_pt_attributes,pp):
	ret = []
	threads = [];
	queues = [];

	#This is the actual join code
	for x in range(0,len(a_pt_attributes)):
		(tag2, ct2) = a_enc_attributes[x];
		q = multiprocessing.Queue()
		threads.append(
			multiprocessing.Process(
				target=join_b_thread,args=(pp, tag2, ct2,b_pt_attributes,b_enc_attributes,q,x)));
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