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
extern "C"{
#include <pbc.h>
#include <functional>
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
int* gen_polynomial(int hash){

}
bool check_init(UDF_INIT *initid, UDF_ARGS *args, char *message){
	//assume args[0] is table name. args[1] is search value, args[2] is search row
	pairing_t pairing;
	char init[]="type d\nq 625852803282871856053922297323874661378036491717\nn 625852803282871856053923088432465995634661283063\nh 3\nr 208617601094290618684641029477488665211553761021\na 581595782028432961150765424293919699975513269268\nb 517921465817243828776542439081147840953753552322\nk 6\nnk 60094290356408407130984161127310078516360031868417968262992864809623507269833854678414046779817844853757026858774966331434198257512457993293271849043664655146443229029069463392046837830267994222789160047337432075266619082657640364986415435746294498140589844832666082434658532589211525696\nhk 1380801711862212484403205699005242141541629761433899149236405232528956996854655261075303661691995273080620762287276051361446528504633283152278831183711301329765591450680250000592437612973269056\ncoeff0 472731500571015189154958232321864199355792223347\ncoeff1 352243926696145937581894994871017455453604730246\ncoeff2 289113341693870057212775990719504267185772707305\nnqr 431211441436589568382088865288592347194866189652";
	pairing_init_set_str(pairing, init);
	std::hash<std::string> str_hash;

}
void check_deinit(UDF_INIT *initid){

}
long long check(UDF_INIT *initid, UDF_ARGS *args,char *is_null, char *error){

}
}
#endif /* HAVE_DLOPEN */
