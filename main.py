import tensorflow as tf
import numpy as np
from matplotlib import pyplot as plt
import sys
import urllib
from bottle import route, run, template, static_file, get, post, request
from preprocess import draw_base64
import base64
import random

image = ""
images = []


def initWeight(shape):
    weights = tf.truncated_normal(shape,stddev=0.1)
    return tf.Variable(weights)

def initBias(shape):
    bias = tf.constant(0.1,shape=shape)
    return tf.Variable(bias)

def conv2d(x,W):
    return tf.nn.conv2d(x,W,strides=[1,1,1,1],padding="SAME")

def maxPool2d(x):
    return tf.nn.max_pool(x,ksize=[1,2,2,1],strides=[1,2,2,1],padding="SAME")

sess = tf.InteractiveSession()


# NOW FOR THE GRAPH BUILDING
x = tf.placeholder("float", shape=[None, 12288])
y_ = tf.placeholder("float", shape=[None, 3])

# turn the pixels into the a matrix
xImage = tf.reshape(x,[-1,64,64,3])
# xImage = x;

# conv layer 1
wConv1 = initWeight([5,5,3,64])
bConv1 = initBias([64])
# turns to 16x16 b/c pooling
hConv1 = tf.nn.relu(conv2d(xImage,wConv1) + bConv1)
hPool1 = maxPool2d(hConv1)

# conv layer 2
wConv2 = initWeight([5,5,64,256])
bConv2 = initBias([256])
# turns to 8x8 b/c pooling
hConv2 = tf.nn.relu(conv2d(hPool1,wConv2) + bConv2)
hPool2 = maxPool2d(hConv2)

# fully connected layer
W_fc1 = initWeight([16 * 16 * 256, 12288])
b_fc1 = initBias([12288])

# resize the 7x7x64 into a 1-D array so we can matmul it.
h_pool2_flat = tf.reshape(hPool2, [-1, 16*16*256])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

# dropout for the FC layer.
keep_prob = tf.placeholder("float")
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

# weights to turn to softmax classify
W_fc2 = initWeight([12288, 3])
b_fc2 = initBias([3])
y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)
y_conv_reshape = tf.reshape(y_conv, [-1, 3])

cross_entropy = -tf.reduce_sum(y_*tf.log(y_conv  + 1e-9))
train_step = tf.train.AdamOptimizer(1e-8).minimize(cross_entropy)

var1 = tf.argmax(y_conv_reshape,1)
var2 = tf.argmax(y_,1)
correct_prediction = tf.equal(var1, var2)
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))


sess.run(tf.initialize_all_variables())

si = 3
sl = ["c", "j", "k"]
sn = ["Carleton","Juyeong","Kevin"]

batch_size = 6
batches = 6

batch = np.zeros((batches, batch_size, 12288))
labels = np.zeros((batches, batch_size,si))
saver = tf.train.Saver()


if sys.argv[1] == "train":
    ###MAKE IT INTO ONE BIG LINE
    images_list = []
    labels_list = []
    for id in range(3):
        same = sl[id]
        for image_index in range(0,12):
            loc = "data/%s%d.jpg"%(same,image_index)
            images_list.append(plt.imread(loc).flatten())

            l = np.zeros(3)
            l[id] = 1
            labels_list.append(l)

    c = list(zip(images_list, labels_list))
    random.shuffle(c)
    images_list, labels_list = zip(*c)


    for i in range(6):
        batch[i] = images_list[i:len(images_list):6]
        labels[i] = labels_list[i:len(labels_list):6]

    batch = batch/255
    for i in range(20000):
        for j in range(batches):
            if j%1 == 0:
                v1 = y_conv_reshape.eval(feed_dict={x:batch[j], y_: labels[j], keep_prob: 1.0})
                # v2 = var1.eval(feed_dict={x:batch[j], y_: labels[j], keep_prob: 1.0})
                v3 = h_fc1.eval(feed_dict={x:batch[j], y_: labels[j], keep_prob: 1.0})
                print (v1, v3, batch[j], labels[j])
                train_accuracy = accuracy.eval(feed_dict={x:batch[j], y_: labels[j], keep_prob: 1.0})
                print("step %d, batch %d, training accuracy %.10f"%(i, j, train_accuracy))
            train_step.run(feed_dict={x:batch[j], y_: labels[j], keep_prob: 0.5})
        if i%5 == 0 and i != 0:
            saver.save(sess, "models/training.ckpt", global_step=i)

elif sys.argv[1] == "server":
    print("server")
else:
    saver.restore(sess, tf.train.latest_checkpoint("/Users/kevin/Desktop/slohacks2019/models/"))
    batch = np.zeros((1,1024))
    batch[0] = plt.imread(sys.argv[1]).flatten()
    print(y_conv.eval(feed_dict={x: batch, y_: labels, keep_prob: 1.0}))


def save_base64(base64_string, out_file):
    fh = open(out_file, "wb")
    fh.write(base64_string.decode('base64'))
    fh.close()

@route('/')
def index():
    return "same"

@post('/post_video')
def post_video():
    global image
    global images
    base64_string = request.params['image']
    image = base64_string

    image_file = "image%d.png"%count
    images.append(image_file)
    save_base64(image_file, base64_string)
    return "same"

@get('/get_video')
def get_video():
    global image
    return image

@post('/authenticate')
def authenticate():
    global images

    flattened_images = [misc.imread(x).flatten() for x in images]
    saver.restore(sess, tf.train.latest_checkpoint("models/"))
    batch = flattened_images
    pr = y_conv.eval(feed_dict={x: batch, y_: labels, keep_prob: 1.0})

    return max(pr)



run(host='localhost', port=8000)
