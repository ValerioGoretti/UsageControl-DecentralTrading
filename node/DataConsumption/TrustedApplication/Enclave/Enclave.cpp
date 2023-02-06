#include "Enclave_t.h"
#include "stdio.h"
#include <stdlib.h>
#include <sgx_tprotected_fs.h>
#include <sgx_tseal.h>
#include <sgx_utils.h>
#include <string.h>
#include "sgx_tprotected_fs.h"

#include <sgx_urts.h>
#include <sgx_uae_service.h>


bool authenticate_application(const char *pub_k, const char *encr_pubk) {
    return true;
}

char *get_policy_value(char *token, int i) {
    char *end_token;
    //ocall_print(token);
    char *token2 = strtok_r(token, ",", &end_token);
    int ii = 0;
    while (token2 != NULL) {
        if (ii == i) {
            //ocall_print(token2);
            return token2;
        }
        ii++;
        token2 = strtok_r(NULL, ",", &end_token);
    }
    return NULL;
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

char *search_line(char *policies, char *id) {
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
    char *policy = search_line(policies, id);
    return policy;
}

char *get_usage_log() {
    return read_protected_file("Logs.txt");
}

size_t write_protected_file_gen(const char *filename, char *mode, char *data) {
    char *d = strndup(data, strlen(data));
    SGX_FILE *file = sgx_fopen_auto_key(filename, mode);
    size_t len = strlen(d);
    if (file == NULL) {
        ocall_print("Error opening usage policy file.\n");
    }


    size_t sizeofWrite = sgx_fwrite(d, sizeof(char), len, file);

    if (sizeofWrite == 0) {
        ocall_print("Error writing file.\n");
    }

    sgx_fclose(file);
    return sizeofWrite;
}

size_t write_protected_file(char *data) {
    char *d = strndup(data, strlen(data));
    SGX_FILE *file = sgx_fopen_auto_key("Usage_Policies.txt", "a+");
    size_t len = strlen(d);
    if (file == NULL) {
        ocall_print("Error opening usage policy file.\n");
    }

    size_t sizeofWrite = sgx_fwrite(d, sizeof(char), len, file);

    if (sizeofWrite == 0) {
        ocall_print("Error writing file.\n");
    }

    sgx_fclose(file);
    return sizeofWrite;
}

size_t write_log(char *data) {
    SGX_FILE *file = sgx_fopen_auto_key("Logs.txt", "a+");
    size_t len = strlen(data);
    if (file == NULL) {
        ocall_print("Error opening Logs file.\n");
    }

    size_t sizeofWrite = sgx_fwrite(data, sizeof(char), len, file);

    if (sizeofWrite == 0) {
        ocall_print("Error writing file.\n");
    }

    sgx_fclose(file);
    return sizeofWrite;
}

size_t write_application_file(char *data) {
    SGX_FILE *file = sgx_fopen_auto_key("Application.txt", "a+");
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

char *get_application_name(const char *pubk) {
    return (char *) pubk;
}


char *concatenate(const char *str1, const char *str2, const char *str3, const char *str4, const char *str5) {
    char *result;
    size_t len1 = strlen(str1);
    size_t len2 = strlen(str2);
    size_t len3 = strlen(str3);
    size_t len4 = strlen(str4);
    size_t len5 = strlen(str5);
    result = (char *) malloc(len1 + len2 + len3 + len4 + len5 + 1); /* make space for the new string */

    strlcpy(result, ",", 1); /* copy str1 into the new string */

    strncat(result, str1, len1);
    strncat(result, ",", 1);

    strncat(result, str2, len2);
    strncat(result, ",", 1);

    strncat(result, str3, len3);
    strncat(result, ",", 1);

    strncat(result, str4, len4);
    strncat(result, ",", 1);

    strncat(result, str5, len5);
    strncat(result, "\n", 2);

    return result;
}

int32_t delete_file(char *filename) {
    int32_t a;
    a = sgx_remove(filename);
    return a;
}

int count_log_access(char *id_res) {
    char *res = read_protected_file("Logs.txt");
    //char *policy = search_line(res, id_res);

    char *end_str;
    char *token = strtok_r(res, "\n", &end_str);

    char *result;
    char *mod = "access";
    size_t len1 = strlen(id_res);
    size_t len2 = strlen(mod);
    result = (char *) malloc(len1 + len2 + 1);

    strlcpy(result, ",", 1);
    strncat(result, id_res, len1);
    strncat(result, "access", len2);

    char string_c[128];
    int c = 0;

    while (token != NULL) {
        if (search_id(id_res, token)) {
            c += 1;
        }
        token = strtok_r(NULL, "\n", &end_str);
    }

    snprintf(string_c, 128, "%d", c);
    //ocall_print(string_c);
    return c;
}

char *retrieve_log_timestamp(char *id_res) {
    char *res = read_protected_file("Logs.txt");

    char *end_str;
    char *token = strtok_r(res, "\n", &end_str);

    while (token != NULL) {
        if (search_id(id_res, token)) {
            int pos = 2;
            char *u_p = strndup(token, strlen(token));
            char *temp_constraint = get_policy_value(u_p, pos);
            return temp_constraint;
        }
        token = strtok_r(NULL, "\n", &end_str);
    }

    return NULL;
}

bool enforce_geographical(char *usage_policy) {
    ocall_print("============GEO============= ✓");
    int pos = 2;
    char *u_p = strndup(usage_policy, strlen(usage_policy));

    char *country_constraint = get_policy_value(u_p, pos);
    //ocall_print(value);
    char geo_location[128];
    size_t length;
    get_geo_location(geo_location, sizeof(geo_location));
    return strcmp(geo_location, country_constraint) == 0;
}

bool enforce_domain(char *usage_policy, const char *purpose) {
    ocall_print("============Domain============= ✓");
    int pos = 5;
    char *u_p = strndup(usage_policy, strlen(usage_policy));

    //*+retrieve the domain of the application here using the public key
    //char *application_domain = "Medical";
    //*+retrieve the domain of the constraint here from the usage policy
    char *constraint_domain = get_policy_value(u_p, pos);
    return strcmp(purpose, constraint_domain) == 0;
}

bool enforce_access_counter(char *usage_policy, char *id_res) {
    ocall_print("============Access Counter============= ✓");
    int pos = 3;
    char *u_p = strndup(usage_policy, strlen(usage_policy));

    //*+retrieve the access counter of the application from the usage policy
    char *constraint_access_counter = get_policy_value(u_p, pos);
    int ac = atoi(constraint_access_counter);

    int access = count_log_access(id_res);
    //*+retrieve the number of the access by the log
    return ac >= access;
    ocall_print(" - remove - ");
}

char *search_application(char *id_app) {
    char *apps = read_protected_file("Application.txt");
    char *app = search_line(apps, id_app);
    return app;
}

char *get_application_name(char *app) {
    int pos = 1;
    char *app_name = strndup(app, strlen(app));
    char *name = get_policy_value(app_name, pos);
    return name;
}

char *get_application_purpose(char *app) {
    int pos = 2;
    char *app_purpose = strndup(app, strlen(app));
    char *purpose = get_policy_value(app_purpose, pos);
    return purpose;
}

void remove_policy(const char *id) {
    ocall_print("---------(remove policy)----------");

    char *res = read_protected_file("Usage_Policies.txt");
    ocall_print(res);

    char *end_str;
    char *token = strtok_r(res, "\n", &end_str);

    ocall_print(" - remove - ");

    while (token != NULL) {
        if (!search_id(id, token)) {
            char *tok = (char *) malloc(strlen(token) + strlen("\n") + 1);
            tok = strndup(token, strlen(token));
            strncat(tok, "\n", strlen("\n"));
            write_protected_file_gen("Usage_Policies_temp.txt", "a+", tok);
            ocall_print(token);
        }
        token = strtok_r(NULL, "\n", &end_str);
    }

    delete_file("Usage_Policies.txt");
    char *r = read_protected_file("Usage_Policies_temp.txt");
    char *end_str_temp;
    char *token_temp = strtok_r(r, "\n", &end_str_temp);

    while (token_temp != NULL) {
        char *tok_temp = (char *) malloc(strlen(token_temp) + 1);
        write_protected_file_gen("Usage_Policies.txt", "a+", tok_temp);
        ocall_print(token_temp);
        token_temp = strtok_r(NULL, "\n", &end_str_temp);
    }

    delete_file("Usage_Policies_temp.txt");
}


void write_log_entry(const char *id_resource, const char *mode, const char *app_purpose) {
    char string_now[128];
    int now;
    get_time(&now, sizeof(now));
    snprintf(string_now, 128, "%d", now);

    char geo_location[128];
    size_t length;
    get_geo_location(geo_location, sizeof(geo_location));

    char *log = concatenate(id_resource, mode, string_now, app_purpose, geo_location);
    write_log(log);

    char *res = read_protected_file("Logs.txt");
    ocall_print(res);
}

void remove_file(char *id) {
    size_t len = strlen(id);
    const char *ext = ".txt";
    size_t len_ext = strlen(ext);

    char *name_file = (char *) malloc(len + len_ext + 1);

    strncat(name_file, id, len);
    strncat(name_file, ext, len_ext);

//  delete file
    delete_file(name_file);


//  delete policy
    remove_policy(id);


//  store action in log
    write_log_entry(id, "remove", "NONE");

}

bool check_temporal(char *usage_policy, char *id_res) {
    int pos = 4;

    char *u_p = strndup(usage_policy, strlen(usage_policy));

    char *constraint_temporal = get_policy_value(u_p, pos);

    int max_duration = atoi(constraint_temporal);

    char string_now[128];
    int now;
    get_time(&now, sizeof(now));
    //snprintf(string_now,128,"%d",now); to converto the timestamp to a string format for printing
    //*+parse the usage policy and get the country constraint here.
    //ocall_print_int(&now);

    char *r_t = retrieve_log_timestamp(id_res);

    int retrieval_timestamp = atoi(r_t);

    return retrieval_timestamp + max_duration > now;
}

void enforce_temporal() {
    ocall_print("============Temporal============= ✓");
    char *policies = get_policies();
    ocall_print(policies);

    char *end_str;
    char *token = strtok_r(policies, "\n", &end_str);

    ocall_print(token);

    while (token != NULL) {
        char *tok = strndup(token, strlen(token));
        char *tok_d = strndup(token, strlen(token));
        char *id = get_policy_value(tok, 0);
        if(!check_temporal(tok_d,id)){
            remove_file(id);
        }
        token = strtok_r(NULL, "\n", &end_str);
    }
}


SGX_FILE *
access_protected_resource(const char *pub_k, const char *encr_pubk, char *mode, char *id_resource) {
    char *policies = get_policy(id_resource);
    ocall_print(policies);


    //=====================Application Recognized=====================

    //char * data="abc,Facebook,Social\nefg,HealthCare,Medical\ncde,Zooresearch,Research";

    //write_application_file(data);
    //char* app=read_protected_file("Application.txt");
    //ocall_print(app);

    char *pub_key = (char *) pub_k;
    char *app = search_application(pub_key);
    char *app_name = get_application_name(app);
    char *app_purpose = get_application_purpose(app);

    ocall_print(app_name);
    ocall_print(app_purpose);


    //=====================LOG=====================
    char string_now[128];
    int now;
    get_time(&now, sizeof(now));
    snprintf(string_now, 128, "%d", now);

    char geo_location[128];
    size_t length;
    get_geo_location(geo_location, sizeof(geo_location));

    ocall_print(id_resource);
    ocall_print(mode);
    ocall_print_int(&now);
    ocall_print(get_application_name(pub_k));
    ocall_print(geo_location);


    char *log = concatenate(id_resource, mode, string_now, app_purpose, geo_location);
    //char *log = concatenate("4", "access", "1674662590", "efg", "FR");

    //=================ENFORCEMENT=================

    if (enforce_geographical(policies)) {
        ocall_print("Geographical rule fulfilled");
        if (enforce_domain(policies, app_purpose)) {
            ocall_print("Domain rule fulfilled");
            if (enforce_access_counter(policies, id_resource)) {
                ocall_print("Access Counter rule fulfilled");
                write_log(log);
                char *res = read_protected_file("Logs.txt");
                ocall_print(res);
            } else {
                remove_file(id_resource);
                ocall_print("Access Counter rule not fulfilled");
            }
        } else {
            ocall_print("Domain rule not fulfilled");
        }
    } else {
        ocall_print("Geographical rule not fulfilled");
    }

    return NULL;
}

size_t write_new_file(const char *filename, char *mode, const char *data) {
    SGX_FILE *file = sgx_fopen_auto_key(filename, mode);
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

void del() {
    delete_file("Usage_Policies.txt");
    delete_file("Usage_Policies_temp.txt");
    delete_file("Usage_Logs.txt");
    delete_file("Logs.txt");
    delete_file("1.txt");
    delete_file("2.txt");
}

void new_protected_resource(const char *id_file, const char *file_content, const char *policy) {
    size_t len = strlen(id_file);
    const char *ext = ".txt";
    size_t len_ext = strlen(ext);

    char *name_file = (char *) malloc(len + len_ext + 1);

    strncat(name_file, id_file, len);
    strncat(name_file, ext, len_ext);

//    ocall_print(name_file);

//    Create new resource
    write_new_file(name_file, "w+", file_content);
    char *res = read_protected_file(name_file);
//    ocall_print(res);

    size_t len2 = strlen(name_file);
    size_t len3 = strlen(policy);

//    Update usage policy
    const char *comma = ",";
    const char *newline = "\n";
    size_t len_comma = strlen(comma);
    size_t len_newline = strlen(newline);

    char *l = (char *) malloc(len + len_comma + len2 + len_comma + len3 + len_newline + 1);

    l = strndup(id_file, len);
    strncat(l, comma, len_comma);
    strncat(l, name_file, len2);
    strncat(l, comma, len_comma);
    strncat(l, policy, len3);
    strncat(l, newline, len_newline);

    char *l_w = strndup(l, strlen(l));
    write_protected_file_gen("Usage_Policies.txt", "a+", l_w);

    char *policies2 = get_policies();
    ocall_print(policies2);

//    Store action in usage Log
    write_log_entry(id_file, "retrieval", "NONE");
}