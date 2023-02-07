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

/**
 * get_policy_value
 * ----------------
 * Function that retrieves a value in an entry
 * @param token entry with information split by ','
 * @param i position of the information within the entry
 * @return value of the information
 */
char *get_policy_value(char *token, int i) {
    char *end_token;
    char *token2 = strtok_r(token, ",", &end_token);
    int ii = 0;
    while (token2 != NULL) {
        if (ii == i) {;
            return token2;
        }
        ii++;
        token2 = strtok_r(NULL, ",", &end_token);
    }
    return NULL;
}

/**
 * read_protected_file
 * -------------------
 * Function that returns the contents of the
 * @param filename name of file to be read
 * @return content of the file
 */
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

/**
 * authenticate_application
 * ------------------------
 * Function used to authenticate applications requesting the information
 * @param pub_k Application public key
 * @param encr_pubk Encrypted public key
 * @return true if the application is authenticate
 */
bool authenticate_application(const char *pub_k, const char *encr_pubk) {
    return true;
}

/**
 * get_policies
 * ------------
 * Function that reads the content of policies
 * @return the contents of the Usage_policy file
 */
char *get_policies() {
    return read_protected_file("Usage_Policies.txt");
}

/**
 * search_id
 * ---------
 * Function that checks if a string starts with the required id
 * @param id to be searched at the beginning of the string
 * @param str string in which to search for the id
 * @return true if the string start with the id, false otherwise
 */
bool search_id(const char *id, const char *str) {
    return strncmp(id, str, strlen(id)) == 0;
}

/**
 * search_line
 * -----------
 * Function that splits file lines by \n and searches for the line and that starts with correct id
 * @param str string in which to search for the id
 * @param id id to search
 * @return the correct string related to the id
 */
char *search_line(char *str, char *id) {
    char *end_str;
    char *token = strtok_r(str, "\n", &end_str);

    while (token != NULL) {
        if (search_id(id, token)) {
            return token;
        }
        token = strtok_r(NULL, "\n", &end_str);
    }
    return NULL;
}

/**
 * get_policy
 * ----------
 * Retrieves the usage policies of a file stored in the enclave
 * @param id id of the file to be searched
 * @return the policy of the file
 */
char *get_policy(char *id) {
    char *policies = get_policies();
    char *policy = search_line(policies, id);
    return policy;
}

/**
 * get_usage_log
 * -------------
 * Function that reads the content of the log file
 * @return content of the log file
 */
char *get_usage_log() {
    return read_protected_file("Logs.txt");
}

/**
 * write_protected_file_gen
 * ------------------------
 * Function used for write a data on a file
 * @param filename name of the file to be written
 * @param mode how to open the file (w, w+, a, a+)
 * @param data data to be written in the file
 * @return the size of the data written
 */
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

/**
 * get_application_name
 * --------------------
 * Function that return the name of the application by the public key
 * @param pubk public key of the application
 * @return the application name
 */
char *get_application_name(const char *pubk) {
    return (char *) pubk;
}

/**
 * concatenate
 * -----------
 * Function that concatenate the string for create the log entry
 * @param id id of the file to track in the log
 * @param action execute on the resource
 * @param time of expiration of the file
 * @param app application that require the action
 * @param geo device geographical position
 * @return the entry to write in the log file
 */
char *concatenate(const char *id, const char *action, const char *time, const char *app, const char *geo) {
    char *result;
    size_t len1 = strlen(id);
    size_t len2 = strlen(action);
    size_t len3 = strlen(time);
    size_t len4 = strlen(app);
    size_t len5 = strlen(geo);
    result = (char *) malloc(len1 + len2 + len3 + len4 + len5 + 1);
    strlcpy(result, ",", 1);
    strncat(result, id, len1);
    strncat(result, ",", 1);
    strncat(result, action, len2);
    strncat(result, ",", 1);
    strncat(result, time, len3);
    strncat(result, ",", 1);
    strncat(result, app, len4);
    strncat(result, ",", 1);
    strncat(result, geo, len5);
    strncat(result, "\n", 2);
    return result;
}

/**
 * delete_file
 * -----------
 * Function that delete a file
 * @param filename name of the file to be deleted
 * @return the resoult of the removal
 */
int32_t delete_file(char *filename) {
    int32_t a;
    a = sgx_remove(filename);
    return a;
}

/**
 * count_log_access
 * ----------------
 * Function that counts the amount of accesses of a resource within the log
 * @param id_res id of the resource to be searched in the log file
 * @return the number of access
 */
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
    return c;
}

/**
 * retrieve_log_timestamp
 * ----------------------
 * Function that retrieve the retrieval timestamp of the file
 * @param id_res id of the resource to be searched in the log file
 * @return the time of the retrivial of the resource
 */
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

/**
 * enforce_geographical
 * --------------------
 * Geographical enforcment function
 * @param usage_policy requested file policy
 * @return true if is fulfil, false otherwise
 */
bool enforce_geographical(char *usage_policy) {
    ocall_print("============GEO============= ✓");
    int pos = 2;
    char *u_p = strndup(usage_policy, strlen(usage_policy));

    char *country_constraint = get_policy_value(u_p, pos);
    char geo_location[128];
    size_t length;
    get_geo_location(geo_location, sizeof(geo_location));
    return strcmp(geo_location, country_constraint) == 0;
}

/**
 * enforce_domain
 * --------------
 * Domain enforcment function
 * @param usage_policy requested file policy
 * @param purpose domain of the application requesting the resource
 * @return true if is fulfil, false otherwise
 */
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

/**
 * enforce_access_counter
 * ----------------------
 * access counter enforcment function
 * @param usage_policy requFunction allowing access to a resource within the enclave by performing all necessary checks for usage policiesested file policy
 * @param id_res id of the resource involved
 * @return true if is fulfil, false otherwise
 */
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

/**
 * search_application
 * ------------------
 * Function used for retrieve the information about the application that require the resource
 * @param id_app public key of the application that require a resource
 * @return the information about the application
 */
char *search_application(char *id_app) {
    char *apps = read_protected_file("Application.txt");
    char *app = search_line(apps, id_app);
    return app;
}

/**
 * get_application_name
 * --------------------
 * Function that retrieve the name of the application that request a resource
 * @param app app information
 * @return the name of the application
 */
char *get_application_name(char *app) {
    int pos = 1;
    char *app_name = strndup(app, strlen(app));
    char *name = get_policy_value(app_name, pos);
    return name;
}

/**
 * get_application_purpose
 * -----------------------
 * Function that retrieve the purpose of the application that request a resource
 * @param app app information
 * @return the purpose of the application
 */
char *get_application_purpose(char *app) {
    int pos = 2;
    char *app_purpose = strndup(app, strlen(app));
    char *purpose = get_policy_value(app_purpose, pos);
    return purpose;
}

/**
 * remove_policy
 * -------------
 * Function that removes the policy entry relating to a file
 * @param id id of the resource involved
 */
void remove_policy(const char *id) {
    char *res = read_protected_file("Usage_Policies.txt");

    char *end_str;
    char *token = strtok_r(res, "\n", &end_str);

    while (token != NULL) {
        if (!search_id(id, token)) {
            char *tok = (char *) malloc(strlen(token) + strlen("\n") + 1);
            tok = strndup(token, strlen(token));
            strncat(tok, "\n", strlen("\n"));
            write_protected_file_gen("Usage_Policies_temp.txt", "a+", tok);
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
        token_temp = strtok_r(NULL, "\n", &end_str_temp);
    }

    delete_file("Usage_Policies_temp.txt");
}

/**
 * write_log_entry
 * ---------------
 * Function that writes an entry to the log file
 * @param id_resource id of the file involved
 * @param mode action performed on the file
 * @param app_purpose domain of the application that required the resource
 */
void write_log_entry(const char *id_resource, const char *mode, const char *app_purpose) {
    char string_now[128];
    int now;
    get_time(&now, sizeof(now));
    snprintf(string_now, 128, "%d", now);

    char geo_location[128];
    size_t length;
    get_geo_location(geo_location, sizeof(geo_location));

    char *log = concatenate(id_resource, mode, string_now, app_purpose, geo_location);
    write_protected_file_gen("Logs.txt", "a+",log);
}

/**
 * remove_file
 * -----------
 * Function to remove a file and its policies
 * @param id id of the resource involved
 */
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

/**
 * check_temporal
 * --------------
 * Function used to check if the resource is expired
 * @param usage_policy  requested file policy
 * @param id_res id of te resource involved
 * @return true if is not expired, false otherwise
 */
bool check_temporal(char *usage_policy, char *id_res) {
    int pos = 4;
    char *u_p = strndup(usage_policy, strlen(usage_policy));
    char *constraint_temporal = get_policy_value(u_p, pos);
    int max_duration = atoi(constraint_temporal);
    int now;
    get_time(&now, sizeof(now));
    char *r_t = retrieve_log_timestamp(id_res);
    int retrieval_timestamp = atoi(r_t);
    return retrieval_timestamp + max_duration > now;
}

/**
 * enforce_temporal
 * ----------------
 * Ecall that start the temporal enforcment
 */
void enforce_temporal() {
    char *policies = get_policies();
    char *end_str;
    char *token = strtok_r(policies, "\n", &end_str);

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

/**
 * addApplication
 * --------------
 * Function used to add an application to the list of known applications
 * @param app app information
 */
void addApplication(char * app){
    //char * data="abc,Facebook,Social\nefg,HealthCare,Medical\ncde,Zooresearch,Research";
    write_protected_file_gen("Application.txt", "a+",app);
    char* r_app=read_protected_file("Application.txt");
    ocall_print(r_app);
}

/**
 * access_protected_resource
 * -------------------------
 * Function allowing access to a resource within the enclave by performing all necessary checks for usage policies
 * @param pub_k public key of the application that require a resource
 * @param encr_pubk  encripted public key
 * @param mode action required on the resource
 * @param id_resource id of the resource requested
 * @return the resource requested
 */
SGX_FILE *
access_protected_resource(const char *pub_k, const char *encr_pubk, char *mode, char *id_resource) {
    char *policies = get_policy(id_resource);

    //=====================Application Recognized=====================
    char *pub_key = (char *) pub_k;
    char *app = search_application(pub_key);
    char *app_name = get_application_name(app);
    char *app_purpose = get_application_purpose(app);

    //=====================LOG=====================
    char string_now[128];
    int now;
    get_time(&now, sizeof(now));
    snprintf(string_now, 128, "%d", now);

    char geo_location[128];
    size_t length;
    get_geo_location(geo_location, sizeof(geo_location));

    char *log = concatenate(id_resource, mode, string_now, app_purpose, geo_location);

    //=================ENFORCEMENT=================
    if (enforce_geographical(policies)) {
        ocall_print("Geographical rule fulfilled");
        if (enforce_domain(policies, app_purpose)) {
            ocall_print("Domain rule fulfilled");
            if (enforce_access_counter(policies, id_resource)) {
                ocall_print("Access Counter rule fulfilled");
                write_protected_file_gen("Logs.txt", "a+",log);
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

/**
 * write_new_file
 * --------------
 *
 * @param filename name of the file for store a resource
 * @param mode how to open the file (w, w+, a, a+)
 * @param data data to be written in the file
 * @return the size of the data written
 */
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

/**
 * new_protected_resource
 * ----------------------
 * Function that stores a new resource in the enclave
 * @param id_file id of the new resource
 * @param file_content content of the resource
 * @param policy resource policy
 */
void new_protected_resource(const char *id_file, const char *file_content, const char *policy) {
    size_t len = strlen(id_file);
    const char *ext = ".txt";
    size_t len_ext = strlen(ext);
    char *name_file = (char *) malloc(len + len_ext + 1);
    strncat(name_file, id_file, len);
    strncat(name_file, ext, len_ext);

//  Create new resource
    write_new_file(name_file, "w+", file_content);
    char *res = read_protected_file(name_file);
    size_t len2 = strlen(name_file);
    size_t len3 = strlen(policy);

//  Update usage policy
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

//  Store action in usage Log
    write_log_entry(id_file, "retrieval", "NONE");
}