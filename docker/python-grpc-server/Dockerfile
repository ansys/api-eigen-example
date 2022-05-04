# First select the image on top of which we want to create our server
FROM ubuntu:22.04

# Next in line, we will install the heavy reqs... Hopefully this does not change much
# This stage takes a lot of time
RUN apt-get update -y && apt-get install cmake libeigen3-dev pip -y

# Now, let us create our work directory where we will import our server requirements, files etc.
WORKDIR /server
ADD requirements /server/requirements
ADD src/ansys/eigen/cpp/eigen-wrapper /server/ansys/eigen/cpp/eigen-wrapper
ADD src/ansys/eigen/python /server/ansys/eigen/python
ADD pyproject.toml /server/pyproject.toml
ADD README.md /server/README.md

# Next in line, we will install our requirements
RUN pip install -r requirements/requirements_eigen_wrapper.txt
RUN pip install ansys/eigen/cpp/eigen-wrapper
RUN pip install -r requirements/requirements_build.txt
RUN pip install .

# Define the necessary env variables and exposed port for accesssing the server
EXPOSE 50051

# Define our container entry command - Basically run the server
CMD ["python3", "ansys/eigen/python/grpc/server.py"]
