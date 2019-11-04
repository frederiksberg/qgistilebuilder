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

RUN mkdir -p /opt/tiles

RUN touch /var/log/tilebuilder.info && \
    touch /var/log/tilebuilder.err && \
    ln -sf /dev/stdout /var/log/tilebuilder.info && \
    ln -sf /dev/stderr /var/log/tilebuilder.err

CMD python3 run.py --project /opt/projekter/almeneboliger.qgz --minzoom 12 --maxzoom 15 --extend "718098.2892464173,725122.9767535825,6173322.497463259,6179209.47663593 [EPSG:25832]"
