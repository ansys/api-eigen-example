# First select the image on top of which we want to create our client
FROM ubuntu:22.04

# Now, let us create our work directory where we will import our client requirements
WORKDIR /client
ADD requirements /client/requirements

# Next in line, we will install our requirements
RUN apt-get update -y && apt-get install pip curl -y
RUN sed -e '/demo_eigen_wrapper/ s/^#*/#/' -i /client/requirements/requirements_build.txt
RUN pip install -r requirements/requirements_build.txt
RUN pip install ipykernel jupyterlab notebook

# Add the needed folders for acting as a client (and the demo!)
ADD python /client/python
ADD docker/python-rest-client/demo.ipynb /client/demo.ipynb

# Expose our port for accessing the Jupyter Notebook
EXPOSE 8888

# Define our container entry command - Basically run the Jupyter Notebook
CMD ["jupyter-lab", "--ip", "0.0.0.0", "--allow-root"]
