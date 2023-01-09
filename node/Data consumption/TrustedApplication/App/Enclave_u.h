#ifndef ENCLAVE_U_H__
#define ENCLAVE_U_H__

#include <stdint.h>
#include <wchar.h>
#include <stddef.h>
#include <string.h>
#include "sgx_edger8r.h" /* for sgx_status_t etc. */

#include "sgx_tprotected_fs.h"
#include "sgx_tseal.h"

#include <stdlib.h> /* for size_t */

#define SGX_CAST(type, item) ((type)(item))

#ifdef __cplusplus
extern "C" {
#endif

#ifndef OCALL_PRINT_DEFINED__
#define OCALL_PRINT_DEFINED__
void SGX_UBRIDGE(SGX_NOCONVENTION, ocall_print, (const char* str));
#endif
#ifndef GET_GEO_LOCATION_DEFINED__
#define GET_GEO_LOCATION_DEFINED__
void SGX_UBRIDGE(SGX_NOCONVENTION, get_geo_location, (char* str, size_t length));
#endif
#ifndef GET_TIME_DEFINED__
#define GET_TIME_DEFINED__
void SGX_UBRIDGE(SGX_NOCONVENTION, get_time, (char* time, size_t length));
#endif
#ifndef U_SGXPROTECTEDFS_EXCLUSIVE_FILE_OPEN_DEFINED__
#define U_SGXPROTECTEDFS_EXCLUSIVE_FILE_OPEN_DEFINED__
void* SGX_UBRIDGE(SGX_NOCONVENTION, u_sgxprotectedfs_exclusive_file_open, (const char* filename, uint8_t read_only, int64_t* file_size, int32_t* error_code));
#endif
#ifndef U_SGXPROTECTEDFS_CHECK_IF_FILE_EXISTS_DEFINED__
#define U_SGXPROTECTEDFS_CHECK_IF_FILE_EXISTS_DEFINED__
uint8_t SGX_UBRIDGE(SGX_NOCONVENTION, u_sgxprotectedfs_check_if_file_exists, (const char* filename));
#endif
#ifndef U_SGXPROTECTEDFS_FREAD_NODE_DEFINED__
#define U_SGXPROTECTEDFS_FREAD_NODE_DEFINED__
int32_t SGX_UBRIDGE(SGX_NOCONVENTION, u_sgxprotectedfs_fread_node, (void* f, uint64_t node_number, uint8_t* buffer, uint32_t node_size));
#endif
#ifndef U_SGXPROTECTEDFS_FWRITE_NODE_DEFINED__
#define U_SGXPROTECTEDFS_FWRITE_NODE_DEFINED__
int32_t SGX_UBRIDGE(SGX_NOCONVENTION, u_sgxprotectedfs_fwrite_node, (void* f, uint64_t node_number, uint8_t* buffer, uint32_t node_size));
#endif
#ifndef U_SGXPROTECTEDFS_FCLOSE_DEFINED__
#define U_SGXPROTECTEDFS_FCLOSE_DEFINED__
int32_t SGX_UBRIDGE(SGX_NOCONVENTION, u_sgxprotectedfs_fclose, (void* f));
#endif
#ifndef U_SGXPROTECTEDFS_FFLUSH_DEFINED__
#define U_SGXPROTECTEDFS_FFLUSH_DEFINED__
uint8_t SGX_UBRIDGE(SGX_NOCONVENTION, u_sgxprotectedfs_fflush, (void* f));
#endif
#ifndef U_SGXPROTECTEDFS_REMOVE_DEFINED__
#define U_SGXPROTECTEDFS_REMOVE_DEFINED__
int32_t SGX_UBRIDGE(SGX_NOCONVENTION, u_sgxprotectedfs_remove, (const char* filename));
#endif
#ifndef U_SGXPROTECTEDFS_RECOVERY_FILE_OPEN_DEFINED__
#define U_SGXPROTECTEDFS_RECOVERY_FILE_OPEN_DEFINED__
void* SGX_UBRIDGE(SGX_NOCONVENTION, u_sgxprotectedfs_recovery_file_open, (const char* filename));
#endif
#ifndef U_SGXPROTECTEDFS_FWRITE_RECOVERY_NODE_DEFINED__
#define U_SGXPROTECTEDFS_FWRITE_RECOVERY_NODE_DEFINED__
uint8_t SGX_UBRIDGE(SGX_NOCONVENTION, u_sgxprotectedfs_fwrite_recovery_node, (void* f, uint8_t* data, uint32_t data_length));
#endif
#ifndef U_SGXPROTECTEDFS_DO_FILE_RECOVERY_DEFINED__
#define U_SGXPROTECTEDFS_DO_FILE_RECOVERY_DEFINED__
int32_t SGX_UBRIDGE(SGX_NOCONVENTION, u_sgxprotectedfs_do_file_recovery, (const char* filename, const char* recovery_filename, uint32_t node_size));
#endif
#ifndef SGX_OC_CPUIDEX_DEFINED__
#define SGX_OC_CPUIDEX_DEFINED__
void SGX_UBRIDGE(SGX_CDECL, sgx_oc_cpuidex, (int cpuinfo[4], int leaf, int subleaf));
#endif
#ifndef SGX_THREAD_WAIT_UNTRUSTED_EVENT_OCALL_DEFINED__
#define SGX_THREAD_WAIT_UNTRUSTED_EVENT_OCALL_DEFINED__
int SGX_UBRIDGE(SGX_CDECL, sgx_thread_wait_untrusted_event_ocall, (const void* self));
#endif
#ifndef SGX_THREAD_SET_UNTRUSTED_EVENT_OCALL_DEFINED__
#define SGX_THREAD_SET_UNTRUSTED_EVENT_OCALL_DEFINED__
int SGX_UBRIDGE(SGX_CDECL, sgx_thread_set_untrusted_event_ocall, (const void* waiter));
#endif
#ifndef SGX_THREAD_SETWAIT_UNTRUSTED_EVENTS_OCALL_DEFINED__
#define SGX_THREAD_SETWAIT_UNTRUSTED_EVENTS_OCALL_DEFINED__
int SGX_UBRIDGE(SGX_CDECL, sgx_thread_setwait_untrusted_events_ocall, (const void* waiter, const void* self));
#endif
#ifndef SGX_THREAD_SET_MULTIPLE_UNTRUSTED_EVENTS_OCALL_DEFINED__
#define SGX_THREAD_SET_MULTIPLE_UNTRUSTED_EVENTS_OCALL_DEFINED__
int SGX_UBRIDGE(SGX_CDECL, sgx_thread_set_multiple_untrusted_events_ocall, (const void** waiters, size_t total));
#endif

sgx_status_t access_protected_resource(sgx_enclave_id_t eid, SGX_FILE** retval, const char* pub_k, const char* encr_pubk, int* id_res);
sgx_status_t seal(sgx_enclave_id_t eid, sgx_status_t* retval, uint8_t* plaintext, size_t plaintext_len, sgx_sealed_data_t* sealed_data, size_t sealed_size);
sgx_status_t unseal(sgx_enclave_id_t eid, sgx_status_t* retval, sgx_sealed_data_t* sealed_data, size_t sealed_size, uint8_t* plaintext, uint32_t plaintext_len);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif
