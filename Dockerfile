# Start from ubuntu
FROM ubuntu
USER root
# Move to working directory
WORKDIR /home/fconlon
# Copy relevant files
COPY ./*.zip ./
COPY ./*.tar.gz ./
# Update and upgrade os to be able to install packages
RUN apt update
RUN apt upgrade -y
# Install needed packages
RUN apt install -y nginx unzip python3 python3-pip python3-dev build-essential 
# Decompress zip/tar files
RUN unzip portfolio-master.zip
RUN unzip django-stable-2.2.x.zip
RUN tar -xzvf uwsgi-2.0.18.tar.gz
# Set up nginx
RUN mv portfolio-master portfolio
RUN rm /etc/nginx/sites-available/default
RUN ln -s /etc/nginx/nginx.conf /etc/nginx/sites-available/default
RUN cp /home/fconlon/portfolio/conf/nginx.conf /etc/nginx/nginx.conf
# Set up uwsgi
WORKDIR /home/fconlon/uwsgi-2.0.18
RUN python3 uwsgiconfig.py --build core
RUN python3 uwsgiconfig.py --plugin plugins/python core
# Set up django
WORKDIR /home/fconlon
RUN pip3 install -e django-stable-2.2.x
RUN /etc/init.d/nginx start
#CMD [ "uwsgi-2.0.18/uwsgi", "--plugin", "uwsgi-2.0.18/python_plugin.so", "--socket", "localhost:3031", "--chdir", "/home/fconlon/portfolio", "--wsgi-file", "portfolio/wsgi.py"]
RUN uwsgi-2.0.18/uwsgi --plugin uwsgi-2.0.18/python_plugin.so --socket localhost:3031 --chdir /home/fconlon/portfolio --wsgi-file portfolio/wsgi.py
