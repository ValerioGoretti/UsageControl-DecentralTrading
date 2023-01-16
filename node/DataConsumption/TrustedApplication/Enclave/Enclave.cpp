#include "Enclave_t.h"
#include "stdio.h"  
#include <sgx_tprotected_fs.h>
#include <sgx_tseal.h>
#include <sgx_utils.h>
#include <string.h>
#include "sgx_tprotected_fs.h"



bool authenticate_application(const char* pub_k, const char* encr_pubk){

	return true;
}

bool enforce_geographical(const char* usage_policy){
	//*+parse the usage policy and get the country constraint here.
	char* country_constraint="IT";
    char geo_location[128];
    size_t length;
    get_geo_location(geo_location, sizeof(geo_location));
	return strcmp(geo_location,country_constraint)==0;
}


bool enforce_domain(const char* usage_policy,const char* pub_k){
	//*+retrieve the domain of the application here using the public key
	char* application_domain="Medical";
	//*+retrieve the domain of the constraint here from the usage policy
	char* constraint_domain="Medical";
    return strcmp(application_domain,constraint_domain)==0;
}


bool enforce_access_counter(const char* usage_policy){
	//*+retrieve the access counter of the application from the usage policy
	int constraint_access_counter=1;
	//*+retrieve the access counter from the usage log
	int access_counter=1;

	return access_counter+1<constraint_access_counter;

}


bool enforce_temporal(char* usage_policy){
    char string_now[128];
	int now;
    get_time(&now, sizeof(now));
	//snprintf(string_now,128,"%d",now); to converto the timestamp to a string format for printing
	//*+parse the usage policy and get the country constraint here.
	int retrieval_timestamp=0;
	//*+parse the usage policy and get the country constraint here.
	int max_duration=0;
	return retrieval_timestamp+max_duration>now;
}



char* read_protected_file(const char* filename){
	SGX_FILE* file=sgx_fopen_auto_key(filename,"r+");
	char buffer[100];
	if (file == NULL) {
	ocall_print("Error opening file.\n");
	}
	size_t size = sgx_fread(buffer, 1, sizeof(buffer), file);
    if (size == 0) {
        ocall_print("Error reading file.\n");  
    }
	ocall_print(buffer);
	char *result =(char* ) malloc (size);
  	strncpy (result, buffer, 100);
	sgx_fclose(file);
	return result;
}



char* get_policy(){
	return read_protected_file("Usage_Policies.txt");
}





SGX_FILE* access_protected_resource(const char* pub_k, const char* encr_pubk,int* id_res){

	authenticate_application(pub_k, encr_pubk);
	char* usage_policy=get_policy();
	ocall_print(usage_policy);
	//size_t size2 = sgx_fwrite(content, 1, sizeof(content), usage_policies);

	if(!enforce_geographical(usage_policy)) {ocall_print("Geographical rule not fulfilled.");}
	enforce_domain(usage_policy,pub_k);
	enforce_access_counter(usage_policy);
	if(!enforce_temporal(usage_policy)) {ocall_print("Temporal rule not fulfilled.");}

	//enforce_domain();
	//enforce_access_counter();

	return NULL;

}