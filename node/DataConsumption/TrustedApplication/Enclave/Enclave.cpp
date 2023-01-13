#include "Enclave_t.h"
#include "stdio.h"  
#include <sgx_tprotected_fs.h>
#include <sgx_tseal.h>
#include <sgx_utils.h>
#include <string.h>
#include "sgx_tprotected_fs.h"

/*
===================== FILE MANAGEMENT =====================
Leggere bene https://www.intel.com/content/www/us/en/developer/articles/technical/overview-of-intel-protected-file-system-library-using-software-guard-extensions.html 
per importare INTEL SGX protected file system


SGX_FILE* ecall_file_open(const char* filename, const char* mode)
{
	SGX_FILE* a;
	a = sgx_fopen_auto_key(filename, mode);
	return a;
}

size_t ecall_file_write(SGX_FILE* fp, char *data)
{
	size_t sizeofWrite;
	size_t len = strlen(data);
	sizeofWrite = sgx_fwrite(data, sizeof(char), len, fp);

	for (int i = 0; i < 5; i++)
	{
		char buffer[] = { 'x' , 'c' };
		sizeofWrite += sgx_fwrite(buffer, sizeof(char), sizeof(buffer), fp);
	}

	return sizeofWrite;
}

size_t ecall_file_read(SGX_FILE* fp, char* readData)
{
	char* data;
	uint64_t startN = 1;
	sgx_fseek(fp, 0, SEEK_END);
	uint64_t finalN = sgx_ftell(fp);
	sgx_fseek(fp, 0, SEEK_SET);

	data = (char*)malloc(sizeof(char) * finalN);
	memset(data, 0, sizeof(char) * finalN);

	size_t sizeofRead = sgx_fread(data, startN, finalN, fp);
	int len = strlen(data);
	memcpy(readData, data, sizeofRead);
	return sizeofRead;
}

int32_t ecall_file_close(SGX_FILE* fp)
{
	int32_t a;
	a = sgx_fclose(fp);
	return a;
}

int32_t ecall_file_delete(char* filename)
{
	int32_t a;
	a = sgx_remove(filename);
	return a;
}
*/

/*
===================== ENFORCEMENT =====================
*/


bool enforce_geographical(){
    char loc[128];
    size_t length;
    get_geo_location(loc, sizeof(loc));
	char* country_constraint="IT";
	return strcmp(loc,country_constraint)==0;
}


int enforce_domain(){
    return 0;
}


int enforce_access_counter(){
    return 0;
}


bool enforce_temporal(){
    char tm[128];
	int a;
    get_time(&a, sizeof(a));
	snprintf(tm,128,"%d",a);
	ocall_print(tm);


	int retrieval_timestamp=0;
	int max_duration=0;
	return retrieval_timestamp+max_duration>a;
}

SGX_FILE* access_protected_resource(const char* pub_k, const char* encr_pubk,int* id_res){


	const char* usage_policies_filename = "Usage_Policies.txt";
	const char* usage_logs_filename = "Usage_Logs.txt";
	const char* mode = "w+";
	SGX_FILE*  usage_policies =sgx_fopen_auto_key(usage_policies_filename, mode);
	SGX_FILE* usage_logs =sgx_fopen_auto_key(usage_logs_filename, mode);

	if(!enforce_geographical()) {ocall_print("Geographical rule not fulfilled.");return NULL;}
	if(!enforce_temporal()) {ocall_print("Temporal rule not fulfilled.");return NULL;}
	//enforce_domain();
	//enforce_access_counter();



	return usage_policies;
}