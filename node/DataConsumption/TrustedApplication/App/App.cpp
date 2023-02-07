#include <stdio.h>
#include <iostream>
#include <dirent.h>
#include "Enclave_u.h"
#include "sgx_urts.h"
#include "sgx_utils/sgx_utils.h"
#include "Server.cpp"
#include "time.h"
#include <curl/curl.h>

/* Global EID shared by multiple threads */
sgx_enclave_id_t global_eid = 0;

/**
 * ocall_print
 * -----------
 * Ocall function use to print element in the enclave
 * @param str
 */
void ocall_print(const char *str) {
    printf("OCALL_PRINT: %s\n", str);
}

/**
 * WriteCallback
 * -------------
 * Function used to execute the device position retrieval API
 */
size_t WriteCallback(void *contents, size_t size, size_t nmemb, void *userp) {
    size_t realsize = size * nmemb;
    char **response = (char **) userp;

    /* allocate memory for the response */
    *response = (char *) realloc(*response, realsize + 1);
    if (*response == NULL) {
        /* out of memory */
        printf("not enough memory (realloc returned NULL)\n");
        return 0;
    }
    /* copy the response */
    memcpy(*response, contents, realsize);
    (*response)[realsize] = 0;
    return realsize;
}

/**
 * get_geo_location
 * -----------
 * Ocall function that retrieve the device location
 * @param str output space
 * @param length length of the output
 */
void get_geo_location(char *str, size_t length) {
    CURL *curl;
    CURLcode res;
    void *response = NULL;
    json_object *parsed_json;
    json_object *loc;
    const char *country = NULL;
    curl = curl_easy_init();
    if (curl) {
        char url[] = "http://ip-api.com/json";
        curl_easy_setopt(curl, CURLOPT_URL, url);
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response);

        /* Perform the request, res will get the return code */
        res = curl_easy_perform(curl);
        /* Check for errors */
        if (res != CURLE_OK)
            fprintf(stderr, "curl_easy_perform() failed: %s\n",
                    curl_easy_strerror(res));
        else {
            parsed_json = json_tokener_parse((char *) response);
            //json_object_object_get_ex(parsed_json, "country_name", &loc);
            json_object *countryCode = json_object_object_get(parsed_json, "countryCode");
            country = json_object_get_string(countryCode);
        }
        /* always cleanup */
        curl_easy_cleanup(curl);

        strncpy(str, country, length);
    }
}

/**
 * get_time
 * -----------
 * OCall function to get the current time
 * @param t output variable
 * @param length length of the output
 */
void get_time(int *t, size_t length) {
    time_t seconds;
    time(&seconds);
    int l = static_cast<int>(time(NULL));
    memcpy(t, &l, length);
}

/**
 * main
 * ----
 * Main function that handles all requests and works with the enclave
 */
int main(int argc, char const *argv[]) {

    //Enclave initialization
    if (initialize_enclave(&global_eid, "enclave.token", "enclave.signed.so") < 0) {
        std::cout << "Fail to initialize enclave." << std::endl;
        return 1;
    }

    //Functions for use the Trusted App
    std::cout << "Disconnessione" << std::endl;
    DIR *d;
    struct dirent *dir;

    return 0;
}
