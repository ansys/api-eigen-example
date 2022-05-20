# First select the image on top of which we want to create our client
FROM continuumio/miniconda3:latest

# Next in line, we will install the heavy reqs... Hopefully this does not change much
# This stage takes a lot of time
RUN apt-get update -y && apt-get install build-essential cmake -y

# Now, let us create our work directory where we will import our client
WORKDIR /client
ADD src/ansys/eigen/cpp/grpc/client /client/project/cpp/grpc/client
ADD src/ansys/eigen/protos /client/project/protos

# Next in line, we will build our client (lib installation is not required)
RUN cd /client/project/cpp/grpc/client && make compile && make install && ./deploy_dependencies.sh && ldconfig && cd -

# And add the demo! And some fun dependencies :)
RUN conda install -c conda-forge jupyterlab
RUN conda install -c conda-forge xeus-cling
ADD docker/cpp-grpc-client/demo.ipynb /client/demo.ipynb

# Expose our port for accessing the Jupyter Notebook
EXPOSE 8888

# Define our container entry command - Basically run the Jupyter Notebook
CMD ["jupyter-lab", "--ip", "0.0.0.0", "--allow-root"]