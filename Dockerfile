FROM qgis/qgis3-build-deps:latest

WORKDIR /usr/src

RUN git clone https://github.com/qgis/qgis

WORKDIR /usr/src/qgis/build

RUN git checkout release-3_8

ENV CC=/usr/lib/ccache/clang
ENV CXX=/usr/lib/ccache/clang++
ENV QT_SELECT=5
ENV LANG=C.UTF-8

RUN cmake \
 -GNinja \
 -DCMAKE_INSTALL_PREFIX=/usr \
 -DBINDINGS_GLOBAL_INSTALL=ON \
 -DWITH_STAGED_PLUGINS=ON \
 -DWITH_GRASS=ON \
 -DSUPPRESS_QT_WARNINGS=ON \
 -DENABLE_TESTS=OFF \
 -DWITH_QSPATIALITE=ON \
 -DWITH_QWTPOLAR=OFF \
 -DWITH_APIDOC=OFF \
 -DWITH_ASTYLE=OFF \
 -DWITH_DESKTOP=ON \
 -DWITH_BINDINGS=ON \
 -DDISABLE_DEPRECATED=ON \
 .. \
 && ninja install \
 && rm -rf /usr/src/QGIS  

WORKDIR /opt/src

RUN pip3 install pysftp

RUN apt-get update && apt-get -y install cron

COPY ./cron /etc/cron.d/cronfile

RUN chmod 0644 /etc/cron.d/cronfile

RUN crontab /etc/cron.d/cronfile

RUN mkdir -p /opt/tiles && mkdir -p /root/.ssh

# I know this isn't secure, but this is not really sensitive to MITM
RUN ssh-keyscan -p 2222 th.frb-data.dk > /root/.ssh/known_hosts && \
    chmod 644 /root/.ssh/known_hosts && \
    chmod 700 /root/.ssh

COPY ./entrypoint.sh /opt/entrypoint.sh

# RUN chmod +x /opt/entrypoint.sh

ENTRYPOINT [ "/opt/entrypoint.sh" ]
