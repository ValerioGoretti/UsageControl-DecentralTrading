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

int enforce_geographical(){
    char loc[128];
    size_t length;

    get_geo_location(loc, sizeof(loc));
    return 0;
}

int enforce_domain(){
    return 0;
}

int enforce_access_counter(){
    return 0;
}

int enforce_temporal(){
    char tm[128];
    size_t length;

    get_time(tm, sizeof(tm));
    return 0;
}

SGX_FILE* access_protected_resource(const char* pub_k, const char* encr_pubk,int* id_res){
    ocall_print("----");
    ocall_print("ciao");
    ocall_print("----");
	const char* filename = "SGX_File_Protection_System.txt";
	const char* mode = "w+";
	SGX_FILE* a = sgx_fopen_auto_key(filename, mode);
    return a;
}


