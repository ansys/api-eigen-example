# First select the image on top of which we want to create our client
FROM continuumio/miniconda3:latest

# Next in line, we will install the heavy reqs... Hopefully this does not change much
# This stage takes a lot of time
RUN apt-get update -y && apt-get install build-essential cmake wget git -y

# Now, let us create our work directory where we will import our client
WORKDIR /client
ADD external /client/external
ADD src/ansys/eigen/cpp/rest/client /client/project

# Next in line, we will install our requirements
RUN apt-get install libtool libcurl4-openssl-dev -y && cd external/restclient-cpp-v0.5.2 && ./autogen.sh && ./configure && make install && cd -
RUN cd external/jsoncpp-v1.9.5/build && cmake -DCMAKE_INSTALL_INCLUDEDIR=include/jsoncpp .. && make install && cd - 
RUN cd project/build/ && cmake .. && cmake --build . && make install && cd -
RUN ldconfig -v

# And add the demo! And some fun dependencies :)
RUN conda install -c conda-forge jupyterlab
RUN conda install -c conda-forge xeus-cling
RUN conda install curl
ADD docker/cpp-rest-client/demo.ipynb /client/demo.ipynb

# Expose our port for accessing the Jupyter Notebook
EXPOSE 8888

# Define our container entry command - Basically run the Jupyter Notebook
CMD ["jupyter-lab", "--ip", "0.0.0.0", "--allow-root"]