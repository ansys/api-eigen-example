# First select the image on top of which we want to create our server
FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive

# Next in line, we will install the heavy reqs... Hopefully this does not change much
# This stage takes a lot of time
RUN apt-get update -y && apt-get install cmake pip python3.8-venv -y

# Now, let us create our work directory where we will import our server requirements, files etc.
ADD src/ansys/eigen/cpp/grpc/server /server/project/cpp/grpc/server
ADD src/ansys/eigen/protos /server/project/protos

# Next in line, we will build our server (lib installation is not required)
RUN cd /server/project/cpp/grpc/server && make compile && make install && ./deploy_dependencies.sh && ldconfig && cd -

# Define the necessary env variables and exposed port for accesssing the server
EXPOSE 50000

# Define our container entry command - Basically run the server
WORKDIR /server/project/cpp/grpc/server/build/bin
CMD ["./cpp_grpc_server"]
