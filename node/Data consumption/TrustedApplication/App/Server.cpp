#include <stdio.h>
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

void sendToClient(char *msg, int n){
	send(n, msg, strlen(msg), 0);
	bzero(msg, sizeof(msg));
}

char * encript(char *msg){
	return msg;
}

char * decript(char *msg){
	return msg;
}

void acceptDomain(){
	printf("IN ACCEPT DOMAIN");
}


int mainListener(){
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
