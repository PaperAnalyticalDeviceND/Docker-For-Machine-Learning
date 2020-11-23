# PAD Neural Network training
#
# Chris's fifth Dockerfile

FROM ubuntu:18.04

# mysql setup
# environment
ENV MYSQL_USER=mysql \
    MYSQL_VERSION=5.7.32 \
    MYSQL_DATA_DIR=/var/lib/mysql \
    MYSQL_RUN_DIR=/run/mysqld \
    MYSQL_LOG_DIR=/var/log/mysql \
    DB_NAME=pad \
    DB_USER=pad_user \
    DB_PASS=R#s1sWe#EW8 \
    DB_SQL=/working/pad-database.sql

# updates
RUN apt-get update \
 && apt-get install zip -y \
 && apt-get install -y python3-pip \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y mysql-server=${MYSQL_VERSION}* \
 && rm -rf ${MYSQL_DATA_DIR} \
 && rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh /sbin/entrypoint.sh

RUN chmod 755 /sbin/entrypoint.sh

EXPOSE 3306/tcp

# copy SQL into PAD database
WORKDIR /working
COPY database/pad-database.sql /working/pad-database.sql
COPY scripts/* /working/

# get images
ADD http://www.crc.nd.edu/~csweet1/padimages/msh_tanzania_blank_data_227.zip /working
RUN unzip /working/msh_tanzania_blank_data_227.zip
RUN rm /working/msh_tanzania_blank_data_227.zip

# load tensorflow
RUN pip3 install tensorflow
RUN pip3 install Pillow

# load msh images
ADD http://www.crc.nd.edu/~csweet1/padimages/msh_227.zip /working
RUN unzip /working/msh_227.zip
RUN mkdir -p /var/www/html/joomla/images/padimages/
RUN mv msh /var/www/html/joomla/images/padimages/
RUN rm /working/msh_227.zip

ENTRYPOINT ["/sbin/entrypoint.sh"]

CMD ["/usr/bin/mysqld_safe"]
