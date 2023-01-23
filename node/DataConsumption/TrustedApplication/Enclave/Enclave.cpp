#include "Enclave_t.h"
#include "stdio.h"
#include <sgx_tprotected_fs.h>
#include <sgx_tseal.h>
#include <sgx_utils.h>
#include <string.h>
#include "sgx_tprotected_fs.h"

bool authenticate_application(const char *pub_k, const char *encr_pubk) {
    return true;
}

char *get_policy_value(char *token, int i) {
    char *end_token;
    ocall_print(token);
    char *token2 = strtok_r(token, ",", &end_token);
    int ii = 0;
    while (token2 != NULL) {
        if (ii == i) {
            ocall_print(token2);
            return token2;
        }
        ii++;
        token2 = strtok_r(NULL, ",", &end_token);
    }
    return NULL;
}


bool enforce_geographical(char *usage_policy) {
    char *dest = strndup(usage_policy, strlen(usage_policy));
    ocall_print("============GEO=============");
    //*+parse the usage policy and get the country constraint here.
    int pos = 2;
    char *country_constraint = get_policy_value(dest, pos);
    //ocall_print(value);
    char geo_location[128];
    size_t length;
    get_geo_location(geo_location, sizeof(geo_location));
    return strcmp(geo_location, country_constraint) == 0;
}

bool enforce_domain(char *usage_policy, const char *pub_k) {
    int pos = 5;
    //*+retrieve the domain of the application here using the public key
    char *application_domain = "Medical";
    //*+retrieve the domain of the constraint here from the usage policy
    char *constraint_domain = "Medical";
    return strcmp(application_domain, constraint_domain) == 0;
}

bool enforce_access_counter(char *usage_policy) {
    ocall_print("============Access Counter=============");
    char *dest = strndup(usage_policy, strlen(usage_policy));
    int pos = 3;
    //*+retrieve the access counter of the application from the usage policy
    char *constraint_access_counter = get_policy_value(dest, pos);

    int ac = atoi(constraint_access_counter);
    //snprintf(constraint_access_counter,128,"%d",ac);
    //*+retrieve the access counter from the usage log
    return true;
}

bool enforce_temporal(char *usage_policy) {
    int pos = 4;
    char string_now[128];
    int now;
    get_time(&now, sizeof(now));
    //snprintf(string_now,128,"%d",now); to converto the timestamp to a string format for printing
    //*+parse the usage policy and get the country constraint here.
    int retrieval_timestamp = 0;
    //*+parse the usage policy and get the country constraint here.
    int max_duration = 0;
    return retrieval_timestamp + max_duration > now;
}

char *read_protected_file(const char *filename) {
    SGX_FILE *file = sgx_fopen_auto_key(filename, "r");
    char buffer[1024];
    if (file == NULL) {
        ocall_print("Error opening file.\n");
    }
    size_t size = sgx_fread(buffer, 1, sizeof(buffer), file);
    if (size == 0) {
        ocall_print("Error reading file.\n");
    }
    char *result = (char *) malloc(size);
    strncpy(result, buffer, size);
    sgx_fclose(file);
    return result;
}

char *get_policies() {
    return read_protected_file("Usage_Policies.txt");
}

bool search_id(const char *pre, const char *str) {
    return strncmp(pre, str, strlen(pre)) == 0;
}

char *search_policy(char *policies, char *id) {
    char *end_str;
    char *token = strtok_r(policies, "\n", &end_str);

    while (token != NULL) {
        if (search_id(id, token)) {
            //ocall_print(token);
            return token;
            //get_policy_value(token,1);
        }
        token = strtok_r(NULL, "\n", &end_str);
    }
    return NULL;
}

char *get_policy(char *id) {
    char *policies = get_policies();
    char *policy = search_policy(policies, id);
    return policy;
}

char *get_usage_log() {
    return read_protected_file("Usage_Logs.txt");
}

size_t write_protected_file(const char *filename, char *data) {
    SGX_FILE *file = sgx_fopen_auto_key(filename, "a+");
    size_t len = strlen(data);
    if (file == NULL) {
        ocall_print("Error opening usage policy file.\n");
    }

    size_t sizeofWrite = sgx_fwrite(data, sizeof(char), len, file);

    if (sizeofWrite == 0) {
        ocall_print("Error writing file.\n");
    }

    sgx_fclose(file);
    return sizeofWrite;
}

SGX_FILE *access_protected_resource(const char *pub_k, const char *encr_pubk, int *id_res) {

    //if(!enforce_geographical()) {ocall_print("Geographical rule not fulfilled.");}
    //if(!enforce_temporal()) {ocall_print("Temporal rule not fulfilled.");}
    //enforce_domain();
    //enforce_access_counter();
    //char content[] = "4,b.txt,FR,15,15,Social\n";
    char *policies = get_policy("3");

    //ocall_print(policies);

    if(enforce_geographical(policies)){
        ocall_print("Geographical rule fulfilled");
    } else{
        ocall_print("Geographical rule not fulfilled");
    }

    if(enforce_access_counter(policies)){
        ocall_print("Access Counter rule fulfilled");
    } else{
        ocall_print("Access Counter rule not fulfilled");
    }


    //size_t a=write_protected_file("Usage_Policies.txt", content);
    //read_line(value);

    // Check if the file was opened successfully
    // Read the contents of the file into a buffer
    // size_t size = sgx_fread(buffer, 1, sizeof(buffer), usage_policies);
    //  if (size == 0) {
    //      ocall_print("Error reading file.\n");
    //      return NULL;
    // }

    // Print the contents of the buffer
    //ocall_print(value);
    return NULL;
}