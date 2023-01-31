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

size_t write_protected_file(char *data) {
    SGX_FILE *file = sgx_fopen_auto_key("Usage_Policies.txt", "a+");
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
}

bool enforce_temporal(char *usage_policy) {
    ocall_print("============Temporal=============");
    int pos = 4;
    char *u_p = strndup(usage_policy, strlen(usage_policy));

    char *constraint_temporal = get_policy_value(u_p, pos);

    char string_now[128];
    int now;
    get_time(&now, sizeof(now));
    //snprintf(string_now,128,"%d",now); to converto the timestamp to a string format for printing
    //*+parse the usage policy and get the country constraint here.
    //ocall_print_int(&now);

    int retrieval_timestamp = 0;
    int max_duration = 0;

    //return retrieval_timestamp + max_duration > now;
    return true;
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

void remove_file(char *filename){

}

SGX_FILE *access_protected_resource(const char *pub_k, const char *encr_pubk, int *id_res, char *mode, char *id_resource) {
    char *policies = get_policy(id_resource);

    ocall_print(policies);
    //ocall_print(mode);
    //ocall_print(id_resource);


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
    write_log(log);

    char *res = read_protected_file("Logs.txt");
    ocall_print(res);

    //count_log_access("4");

    //delete_file("Logs.txt");



    //=================ENFORCEMENT=================

    if (enforce_geographical(policies)) {
        ocall_print("Geographical rule fulfilled");
        if (enforce_domain(policies, app_purpose)) {
            ocall_print("Domain rule fulfilled");
        } else {
            ocall_print("Domain rule not fulfilled");
        }
    } else {
        ocall_print("Geographical rule not fulfilled");
    }


    if (enforce_access_counter(policies, id_resource)) {
        ocall_print("Access Counter rule fulfilled");
        if (enforce_temporal(policies)) {
            ocall_print("Temporal rule fulfilled");
        } else {
//            remove_file();
            ocall_print("Temporal rule not fulfilled");
        }
    } else {
//        remove_file();
        ocall_print("Access Counter rule not fulfilled");
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

char *last_id(char *policies) {
    char *end_str;
    char *token = strtok_r(policies, "\n", &end_str);
    int c = 0;
    int max = 0;
    while (token != NULL) {
        char *end_token;
        char *token2 = strtok_r(token, ",", &end_token);
        while (token2 != NULL) {
            int number = atoi(token2);
            if (c == 0) {
                max = number;
            }
            if (max < number) {
                max = number;
            }
            c++;
            break;
        }
        token = strtok_r(NULL, "\n", &end_str);
    }
    static char numb[64];
    snprintf(numb, 64, "%d", max + 1);
    return numb;
}

void del() {
    delete_file("Usage_Policies.txt");
    delete_file("new_file.txt");
    delete_file("second_file.txt");
    delete_file("third_file.txt");
    delete_file("thir4d_file.txt");
    delete_file("Usage_Logs.txt");
    delete_file("Logs.txt");
}

void new_protected_resource(const char *name_file, const char *file_content, const char *policy) {
    write_new_file(name_file, "w+", file_content);
    //char *res = read_protected_file(name_file);
    //ocall_print(res);

    char *policies = get_policies();

    ocall_print(policies);

    char *l = last_id(policies);
//    ocall_print(l);

    size_t len2 = strlen(name_file);
    size_t len3 = strlen(policy);

    strncat(l, ",", 1);
    strncat(l, name_file, len2);
    strncat(l, ",", 1);
    strncat(l, policy, len3);

    write_protected_file(l);

    char *policies2 = get_policies();
//    ocall_print(policies2);

}