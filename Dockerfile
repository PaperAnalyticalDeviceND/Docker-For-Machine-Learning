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

# get images
RUN mkdir /working/images
ADD https://pad.crc.nd.edu/images/padimages/results/msh_tanzania_data.zip /working/images
RUN unzip /working/images/msh_tanzania_data.zip -d images
RUN rm /working/images/msh_tanzania_data.zip

# load tensorflow
# load tensorflow
RUN pip3 install tensorflow

ENTRYPOINT ["/sbin/entrypoint.sh"]

CMD ["/usr/bin/mysqld_safe"]
