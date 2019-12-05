#ifdef STANDARD
/* STANDARD is defined, don't use any mysql functions */
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#ifdef __WIN__
typedef unsigned __int64 ulonglong;	/* Microsofts 64 bit types */
typedef __int64 longlong;
#else
typedef unsigned long long ulonglong;
typedef long long longlong;
#endif /*__WIN__*/
#else
#include <my_global.h>
#include <my_sys.h>
#if defined(MYSQL_SERVER)
#include <m_string.h>		/* To get strmov() */
#else
/* when compiled as standalone */
#include <string.h>
#define strmov(a,b) stpcpy(a,b)
#define bzero(a,b) memset(a,0,b)
#endif
#endif
#include <mysql.h>
#include <ctype.h>

#ifdef _WIN32
/* inet_aton needs winsock library */
#pragma comment(lib, "ws2_32")
#endif

#ifdef HAVE_DLOPEN

#if !defined(HAVE_GETHOSTBYADDR_R) || !defined(HAVE_SOLARIS_STYLE_GETHOST)
static pthread_mutex_t LOCK_hostname;
#endif
#include <pbc/pbc.h>
#include <functional>
//OBSOLETE TEST CODE TO ENSURE THAT MY SQL UDF SYSTEM WORKS
/**
my_bool hello_world_init(UDF_INIT *initid, UDF_ARGS *args, char *message);
char* hello_world(UDF_INIT *initid, UDF_ARGS *args,
          char *result, unsigned long *length,
          char *is_null, char *error);


my_bool hello_world_init(UDF_INIT *initid, UDF_ARGS *args, char *message)
{
	return 0;
}

char* hello_world(UDF_INIT *initid, UDF_ARGS *args,
          char *result, unsigned long *length,
          char *is_null, char *error){
		memcpy(result, "result string", 13);
		*length = 13;
		return result;
}
**/
struct data{
	int* beta;
	int target;
};

int* gen_polynomial(int size,int* roots){
	int size = sizeof(roots)/sizeof(int);
	int* ret = new int[size+1];
	for(int i = 0; i< size+1; i++){
		ret[i] = 1;
	}
	ret[1] = roots[0];
	for(int i = 1; i<size; i++){
		for(int a = 0; a<i; i++){
			ret[a+1] += root[i]*ret[a];
		}
	}
	return ret;
}

int innerProd(int* alpha, int* beta){
	int size = sizeof(alpha)/sizeof(int);
	int ret = 0;
	for(int i = 0; i< size; i++){
		ret += alpha[i] * beta[i];
	}
	return ret;
}
void recursive_generation(int* roots, int* results, int count){
	if(count == size(roots)/sizeof(int)) return results;
	if(count > 0){
		for(int i = 0; i< count+1; i++){
			results[count+i]+=results[i]*roots[count];
		}
	}
	else{
		results[0] = 1;
		results[1] = roots[0];
	}
	return recursive_generation(roots,results,count+1);
}
unsigned long hash(unsigned char *str)
{
    unsigned long hash = 5381;
    int c;

    while (c = *str++)
        hash = ((hash << 5) + hash) + c; /* hash * 33 + c */

    return hash;
}
bool check_init(UDF_INIT *initid, UDF_ARGS *args, char *message){
	//assume args[0] is table name. args[1] is search value, args[2] is search row
	pairing_t pairing;
	char init[]="type d\nq 625852803282871856053922297323874661378036491717\nn 625852803282871856053923088432465995634661283063\nh 3\nr 208617601094290618684641029477488665211553761021\na 581595782028432961150765424293919699975513269268\nb 517921465817243828776542439081147840953753552322\nk 6\nnk 60094290356408407130984161127310078516360031868417968262992864809623507269833854678414046779817844853757026858774966331434198257512457993293271849043664655146443229029069463392046837830267994222789160047337432075266619082657640364986415435746294498140589844832666082434658532589211525696\nhk 1380801711862212484403205699005242141541629761433899149236405232528956996854655261075303661691995273080620762287276051361446528504633283152278831183711301329765591450680250000592437612973269056\ncoeff0 472731500571015189154958232321864199355792223347\ncoeff1 352243926696145937581894994871017455453604730246\ncoeff2 289113341693870057212775990719504267185772707305\nnqr 431211441436589568382088865288592347194866189652";
	element_t h;
	pairing_init_set_str(pairing, init);
	int r[20];
	element_from_hash(h,args[0],size(args[0])/sizeof(char));
	int alpha[21];
	alpha[0] = element_to_bytes_x_only(h); // sets element 0 of the alpha vector to H(a)
	element_from_hash(h,args[1],size(args[1])/sizeof(char));
	r[0] = element_to_bytes_x_only(h);
	for(int i = 20; !(i<0); i--){
		element_t temp;
		element_t count;
		mpz_t c;
		element_set_si(count,i);
		element_to_mpz(c,count);
		element_pow_mpz(temp,h,c);
		alpha[i] = element_to_bytes_x_only(temp);
	}
	element_from_hash(h,args[1],size(args[1])/sizeof(char));
	for(int i = 1; i<20; i++){
		element_random(h);
		r[i] = element_to_bytes_x_only(h);
	}
	int* pol = gen_polynomial(r);
	int* beta = new int[21];
	element_random(h);
	beta[0] = element_to_bytes_x_only(h);
	for(int i = 1; i< 21; i++){
		beta[i] = pol[i-1];
	}
	delete pol;

	int target = innerProd(alpha,beta);
	data* data = new data();
	data -> target = target;
	data -> beta = beta;
	initid -> ptr = data;
}
void check_deinit(UDF_INIT *initid){
	delete initid -> ptr -> beta;
	delete initid -> ptr;
}
long long check(UDF_INIT *initid, UDF_ARGS *args,char *is_null, char *error){
	data* internal_args = initid -> ptr; //format of internal args is internal_args[0] = target_inner_prod, internal_args[1] = beta vector
	int* val;
	memset(val, args[2], sizeof(args[2]));
	int target = internal_args -> target;
	int* beta = internal_args -> beta;
	int result = innerProd(beta,val);
	if(result == target) return 1;
	else return 0;
}

#endif /* HAVE_DLOPEN */
