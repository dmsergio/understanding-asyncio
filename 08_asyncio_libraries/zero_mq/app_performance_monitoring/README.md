## How to run the project?

```shell
# run the data collector
$ python metric_server.py
# start up several microservice instances
$ python backend_app.py --color blue & \
  python backend_app.py --color green --leak 10000 & \
  python backend_app.py --color red --leak 100000
```
