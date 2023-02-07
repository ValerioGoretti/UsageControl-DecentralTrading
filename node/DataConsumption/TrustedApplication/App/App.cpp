#include <stdio.h>
#include <iostream>
#include <dirent.h>
#include "Enclave_u.h"
#include "sgx_urts.h"
#include "sgx_utils/sgx_utils.h"
#include "time.h"
#include <curl/curl.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <zmq.h>
#include <json-c/json.h>

#define PORT 4444

/* Global EID shared by multiple threads */
sgx_enclave_id_t global_eid = 0;

/**
 * sendToClient
 * ------------
 * Function that sends messages on the socket
 * @param msg message to be sent
 * @param n socket
 */
void sendToClient(char *msg, int n){
    send(n, msg, strlen(msg), 0);
    bzero(msg, sizeof(msg));
}

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
 * Main function that handles all requests and works with the enclave.
 */
int main(int argc, char const *argv[]) {

    //Enclave initialization
    if (initialize_enclave(&global_eid, "enclave.token", "enclave.signed.so") < 0) {
        std::cout << "Fail to initialize enclave." << std::endl;
        return 1;
    }

    DIR *d;
    struct dirent *dir;

    //Functions for use the Trusted App
    // Parse the JSON data
    json_object *root = json_object_from_file("application_list.json");
    if (!root) {
        fprintf(stderr, "Error parsing JSON file\n");
        return 1;
    }
    // Create a context and a socket
    void *context = zmq_ctx_new();
    void *socket = zmq_socket(context, ZMQ_REP);
    // Bind the socket to a port
    zmq_bind(socket, "tcp://*:5555");
    printf("Start listening \n");
    while(true){

        // Wait for a request
        char buffer[256];
        zmq_recv(socket, buffer, 256, 0);
        // Print the request
        //json_object *parsed_json = json_tokener_parse(json_string);
        printf("Received: %s\n", buffer);
        // Send a response
        json_object *name = json_object_object_get(root, "MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAJ0XmjA7l5NERUWbpqECPK0iM7kxWhdDbiicrrrlUa8cmdfFJw6HZbjUlOulSoLZVIpHu+XyVDM6jrSDWYHYPncCAwEAAQ==");
        const char *response = json_object_get_string(name);
        zmq_send(socket, response, strlen(response), 0);

    }
    zmq_close(socket);
    zmq_ctx_destroy(context);

return 0;
}
