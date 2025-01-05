import multiprocessing

bind = "0.0.0.0:3100"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "aiohttp.GunicornWebWorker"
worker_connections = 1000
timeout = 30
keepalive = 2

accesslog = "-"
errorlog = "-"
loglevel = "info"
