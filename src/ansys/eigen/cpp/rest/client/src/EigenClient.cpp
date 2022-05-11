#include "EigenClient.hpp"

#include <restclient-cpp/restclient.h>
#include <stdio.h>
#include <stdlib.h>

ansys::rest::client::EigenClient::EigenClient() {
    fprintf(stdout, "EigenClient object created.\n");
}

ansys::rest::client::EigenClient::~EigenClient() {
    fprintf(stdout, "EigenClient object destroyed.\n");
}