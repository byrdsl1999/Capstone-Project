# sudo service nginx restart
# uwsgi --socket 127.0.0.1:8080 -w run:app --master --processes 4 --threads 2  --daemonize log/uWSGI.log
import sys

sys.path.append('./')

from app import app


if __name__ == "__main__":
    app.run()
