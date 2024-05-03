import os

wsgi_app = 'api.main:app'
worker_class = 'uvicorn.workers.UvicornWorker'
bind = os.getenv('BIND', '0.0.0.0:8000');
loglevel = os.getenv('LOG_LEVEL', 'info')
accesslog = '-'
errorlog = '-'

threads = int(os.getenv('THREADS', str(os.cpu_count() + 1)))
workers = int(os.getenv('WORKERS', str(os.cpu_count() + 1)))
graceful_timeout = int(os.getenv('GRACEFUL_TIMEOUT', '120'))
timeout = int(os.getenv('TIMEOUT', '120'))
keepalive = int(os.getenv('KEEP_ALIVE', '5'))

