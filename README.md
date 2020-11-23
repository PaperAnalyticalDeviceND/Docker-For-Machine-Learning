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
To access the container through a bash terminal run
```
docker exec -it padnn1 /bin/bash
```

The container loads the MSH training/test images to folder ```/working/msh_msh_tanzania_data/```. The ```pad_caffenet_train.py``` script will train the NN using these images,
```
python3 pad_caffenet_train.py
```
The checkpointed weight files can be found in ```tmp/caffenet_pad_msh_tanzania.ckpt``` which can be loaded as follows (given that the checkpoint is ```model_checkpoint```),
```
#create session
with tf.Session() as sess:
    new_saver = tf.train.import_meta_graph(model_checkpoint+'.meta')
    new_saver.restore(sess, model_checkpoint)
    #load in the saved weights
    saver.restore(sess, model_checkpoint)
    ...
```

For generating different image partitions the container loads all of the MSH images to ```/var/www/html/joomla/images/padimages/msh/processed```, the images can be located in the SQL database to obtain full metadata.

All provided images are cropped to ```(71, 359, 71+636, 359+490)``` and resized to ```(227,227)``` for training. Full sized images sets are available at ```http://www.crc.nd.edu/~csweet1/padimages/```, for example ```msh.tar```.

To crop and resize full size images modify the ```resize_images_bundle.py``` script to point to the selected folders and run,
```
python3 resize_images_bundle.py
```

To predict the catagory for an image, given a set of trained weights,
```
python3 predict.py -n msh_tanzania_3k_12.nnet -i /var/www/html/joomla/images/padimages/processed/Acetaminophen-12LanePADKenya2015-1-58861.processed.png
```
The nnet file contains,
```
DRUGS,Paracetamol Starch,Penicillin Procaine,Starch,Lactose,Amoxicillin,Cellulose,Vitamin C,Quinine,Benzyl Penicillin,Paracetamol
LANES,
WEIGHTS,tf_checkpoints/caffenet_pad_msh_tanzania.ckpt
TYPE,tensorflow
DESCRIPTION,MSH Tanzania data: 10 drug NN, 3k images (Tensorflow version), image brightness set to 165.5.
TEST,12LanePADKenya2015
```
which describes the network parameters.
