web: gunicorn fincom.wsgi --log-file -
test: gunicorn fincom.wsgi --log-file - --keyfile server.key --certfile server.crt --bind 0.0.0.0:5100
