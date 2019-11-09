//SET OF FILES TO SERVE AS COMMON LOGIC FOR THE UDFs
extern "C" {
#include  "../Ext_Files/gen_matrices.h"
#include  "../Ext_Files/cryptorand.c"
}
#include <vector>

long innerProduct(vector<int> x , vector<int> y){
	long sum = 0;
	if(x.size() != y.size()){
		return 1;
	}
	for(int i = 0; i< x-> _elems; i++){
		sum += x[i]*y[i];
	}
	return sum;
}

char * vecToBitStr(vector<int> * vec){
	int bitCount = 0;
	char* out = malloc(size(vec));
	while(bitCount < size(vec)){

	}
}