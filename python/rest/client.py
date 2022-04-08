#
# TESTS performed manually - Still to be implemented via Python scripts and automated
#
# Server deployment
# -----------------
#
# >> From the root/first level of the repository
# $ export FLASK_APP=python/rest/server.py
# $ flask run
#
#
# Vector addition
# ---------------
#
# curl -X POST "0.0.0.0:5000/Vectors" -H "Content-Type: application/json" -d '{"value":[5, 23, 3, 4]}'
# curl -X POST "0.0.0.0:5000/Vectors" -H "Content-Type: application/json" -d '{"value":[1, 2, 3, 4]}'
# curl -X GET  "0.0.0.0:5000/add/Vectors" -H "Content-Type: application/json" -d '{"id1":1, "id2":2}'
#
# >>> Response: {"vector-addition": {"result": "[6.0, 25.0, 6.0, 8.0]"}}
#
# Vector multiplication
# ---------------------
#
# curl -X POST "0.0.0.0:5000/Vectors" -H "Content-Type: application/json" -d '{"value":[5, 23, 3, 4]}'
# curl -X POST "0.0.0.0:5000/Vectors" -H "Content-Type: application/json" -d '{"value":[1, 2, 3, 4]}'
# curl -X GET  "0.0.0.0:5000/multiply/Vectors" -H "Content-Type: application/json" -d '{"id1":1, "id2":2}'
#
# >>> Response: {"vector-multiplication": {"result": "76.0"}}
#
#
#
#
#
# Matrix addition
# ---------------
#
# curl -X POST "0.0.0.0:5000/Matrices" -H "Content-Type: application/json" -d '{"value":[[1, 2], [3, 4]]}'
# curl -X POST "0.0.0.0:5000/Matrices" -H "Content-Type: application/json" -d '{"value":[[5, 4], [2, 0]]}'
# curl -X GET  "0.0.0.0:5000/add/Matrices" -H "Content-Type: application/json" -d '{"id1":1, "id2":2}'
#
# >>> Response: {"matrix-addition": {"result": "[[6.0, 6.0], [5.0, 4.0]]"}}
#
# Matrix multiplication
# ---------------------
#
# curl -X POST "0.0.0.0:5000/Matrices" -H "Content-Type: application/json" -d '{"value":[[1, 2], [3, 4]]}'
# curl -X POST "0.0.0.0:5000/Matrices" -H "Content-Type: application/json" -d '{"value":[[5, 4], [2, 0]]}'
# curl -X GET  "0.0.0.0:5000/add/Matrices" -H "Content-Type: application/json" -d '{"id1":1, "id2":2}'
#
# >>> Response: {"matrix-multiplication": {"result": "[[9.0, 4.0], [23.0, 12.0]]"}}
