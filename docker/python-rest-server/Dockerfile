# First select the image on top of which we want to create our server
FROM ubuntu:22.04

# Now, let us create our work directory where we will import our server requirements, files etc.
WORKDIR /server
ADD requirements /server/requirements
ADD python /server/python
RUN mkdir /server/instance

# Next in line, we will install our requirements
RUN apt-get update -y && apt-get install cmake libeigen3-dev pip -y
RUN pip install -r requirements/requirements_eigen_wrapper.txt
RUN pip install python/eigen-wrapper
RUN pip install -r requirements/requirements_build.txt

# Define the necessary env variables and exposed port for accesssing the server
ENV FLASK_APP=python/rest/server.py
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000

# Define our container entry command - Basically run the server
CMD ["flask", "run"]
