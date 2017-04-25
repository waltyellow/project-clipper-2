gunicorn -w 4 --certfile=/etc/letsencrypt/live/cl1.zhenglinhuang.com/cert.pem --keyfile=/etc/letsencrypt/live/cl1.zhenglinhuang.com/privkey.pem -b cl1.zhenglinhuang.com:5000 app:server

