# Using the Docker containers

## API REST using Python
For this case scenario, there are 2 Docker containers, which have to be built the following way:
* **python-rest-client**: Docker container with the needed packages for running the implemented client (i.e. ```from ansys.rest.client import DemoRESTClient```).
* **python-rest-server**: Docker container with the needed packages for running the server with the Eigen library solver.

In order to build them, run from the root directory of the repository the following command:
```
docker image build -t python-rest-client:latest -f docker/python-rest-client/Dockerfile .
docker image build -t python-rest-server:latest -f docker/python-rest-server/Dockerfile .
```

In case you wanted to access the Docker-compose demo, please do as follows:
```
cd docker/python-rest
docker-compose up -d && docker-compose logs

# You will see some information regarding the Jupyter Notebook server deployed, and the token
# required to access it. Something like...
#
# http://127.0.0.1:8888/?token=d4d38b9197aebd2adb6b69ded0f79346c5809eddc593e366
#
# Access it with your desired web-browser
firefox http://127.0.0.1:8888/?token=...
```

Feel free to play around with the ```demo.ipynb``` Jupyter Notebook =)
