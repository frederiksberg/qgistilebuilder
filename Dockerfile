FROM qgis/qgis:latest

WORKDIR /opt/

COPY ./process.py /opt/process.py

CMD tail -f /dev/null