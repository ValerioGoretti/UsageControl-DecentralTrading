#include <stdio.h>
#include <iostream>
#include <dirent.h>
#include "Enclave_u.h"
#include "sgx_urts.h"
#include "sgx_utils/sgx_utils.h"
#include "Server.cpp"
#include "time.h"



/* Global EID shared by multiple threads */
sgx_enclave_id_t global_eid = 0;

// OCall implementations
void ocall_print(const char* str) {
    printf("%s\n", str);
}

// OCall implementations
void get_geo_location(char* str, size_t length) {
    strncpy(str, "Italia", length);
}

// OCall implementations
void get_time(char* t, size_t length) {
    time_t current_time = time(NULL);
    char * time_str = ctime(&current_time);
    time_str[strlen(time_str)-1] = '\0';
    strncpy(t, time_str, length);
}


int main(int argc, char const *argv[]) {
    if (initialize_enclave(&global_eid, "enclave.token", "enclave.signed.so") < 0) {
        std::cout << "Fail to initialize enclave." << std::endl;
        return 1;
    }


    SGX_FILE * file;
    const char* a = "abc";
    const char* b = "abc";
    int* prova;
    sgx_status_t status = access_protected_resource(global_eid, &file, a, b, prova);


    

    std::cout << status << std::endl;
    if (status != SGX_SUCCESS) {
        std::cout << "noob" << std::endl;
    }
    
    std::cout << "Disconnessione" << std::endl;
    DIR *d;
    struct dirent *dir;
    //mainListener();
    return 0;     

}
