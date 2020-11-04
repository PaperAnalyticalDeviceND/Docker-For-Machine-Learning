# Introduction

Dockerfile to build a MySQL container image which can be used for PAD machine learning activities.

# Installation

Build the container,
```
docker build --tag pad_nn_training:1.0 .
```

Run the container. Note ports only required for external mysql access,
```
docker run -p 3306:3306 -dit  --name padnn1 pad_nn_training:1.0
```

View logs,
```
docker logs padnn1
```
you should see something like,
```
Installing database...
Starting MySQL server...
Waiting for database server to accept connections.
Creating debian-sys-maint user...
Creating database "pad"...
Granting access to database "pad" for user "pad_user"...
Loading SQL file "/working/pad-database.sql"...
```

Run bash inside container,
```
docker exec -it padnn1 /bin/bash
```

Remove the container when you are finished.
```
docker rm --force padnn1
```

# Use
