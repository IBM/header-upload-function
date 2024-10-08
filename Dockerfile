FROM registry.access.redhat.com/ubi8/python-39

# Add application sources with correct permissions for OpenShift
USER 0
ADD app-src .
RUN chown -R 1001:0 ./
USER 1001

WORKDIR /app

COPY ./requirements.txt .

RUN pip install -U "pip>=19.3.1"
RUN pip3 install -r requirements.txt
RUN pip3 install apispec
RUN pip3 install apispec_webframeworks
RUN pip3 install marshmallow
RUN pip3 install werkzeug

COPY . .
ENV FLASK_APP=app
EXPOSE 3003

CMD python app.py runserver 0.0.0.0:3003