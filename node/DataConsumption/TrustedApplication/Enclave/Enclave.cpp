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

char* read_protected_file(const char* filename, char* content){

	SGX_FILE* file=sgx_fopen_auto_key(filename,"r+");
	char buffer[100];
	if (file == NULL) {
	ocall_print("Error opening file.\n");
	}
	size_t size = sgx_fread(buffer, 1, sizeof(buffer), file);
    if (size == 0) {
        ocall_print("Error reading file.\n");
        
    }
	sgx_fclose(file);
	strncpy (content, buffer, 100);
	ocall_print(buffer);
	return content;
}

SGX_FILE* access_protected_resource(const char* pub_k, const char* encr_pubk,int* id_res){

	if(!enforce_geographical()) {ocall_print("Geographical rule not fulfilled.");}
	if(!enforce_temporal()) {ocall_print("Temporal rule not fulfilled.");}
	//enforce_domain();
	//enforce_access_counter();

	char buffer;
	char* value=read_protected_file("Usage_Policies.txt",&buffer);
	//char content[]="Hello, world!";
//	size_t size2 = sgx_fwrite(content, 1, sizeof(content), usage_policies);

    // Check if the file was opened successfully
    // Read the contents of the file into a buffer
   // size_t size = sgx_fread(buffer, 1, sizeof(buffer), usage_policies);
  //  if (size == 0) {
  //      ocall_print("Error reading file.\n");
  //      return NULL;
   // }

    // Print the contents of the buffer
    ocall_print(value);
	return NULL;
}