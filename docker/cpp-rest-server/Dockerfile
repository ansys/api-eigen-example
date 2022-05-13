# First select the image on top of which we want to create our server
FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive

# Next in line, we will install the heavy reqs... Hopefully this does not change much
# This stage takes a lot of time
RUN apt-get update -y && apt-get install cmake pip -y

# Now, let us create our work directory where we will import our server requirements, files etc.
WORKDIR /server
ADD src/ansys/eigen/cpp/rest/server /server/project

# Next in line, we will build our server (lib installation is not required)
RUN pip install conan
WORKDIR /server/project/build
RUN conan install ..
RUN cmake ..
RUN cmake --build .

# Define the necessary env variables and exposed port for accesssing the server
EXPOSE 18080

# Define our container entry command - Basically run the server
WORKDIR /server/project/build/bin
CMD ["./cpp_rest_server"]
