import tensorflow as tf
import numpy as np
from matplotlib import pyplot as plt
import sys
import urllib
from bottle import route, run, template, static_file, get, post, request
from preprocess import draw_base64
import base64

# ios posts front end every 0.1 seconds
# web gets image every 0.1 seconds, keeping a counter
# when the counter reaches 6, web sends request for authenticate and resets the counter it has
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
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

var1 = tf.argmax(y_conv_reshape,1)
var2 = tf.argmax(y_,1)
correct_prediction = tf.equal(var1, var2)
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))


sess.run(tf.initialize_all_variables())

si = 3
sl = ["c", "j", "k"]
sn = ["Carleton","Juyeong","Kevin"]

batch = np.zeros((si*6,12288))
labels = np.zeros((si*6,si))

saver = tf.train.Saver()

if sys.argv[1] == "train":
    ti = 0
    for siii in range(si):
        for sxxx in range(6):
            labels[ti] = np.zeros([si])
            labels[ti][siii] = 1

            loc = "IMG_1502.jpg"
            batch[ti] = plt.imread(loc).flatten()
            ti += 1
    batch = batch/225.0

    for i in range(20000):
        if i%10 == 0:
            print("hi")
            train_accuracy = accuracy.eval(feed_dict={x:batch, y_: labels, keep_prob: 1.0})
            print("step %d, training accuracy %g"%(i, train_accuracy))
            # result = y_conv.eval(feed_dict={x: batch, y_: labels, keep_prob: 1.0})
            # for k in range(18):
            #     print "lmao %d %s" % (k, np.array_str(result[k]))
        if i%50 == 0:
            saver.save(sess, "models/training.ckpt", global_step=i)

        train_step.run(feed_dict={x: batch, y_: labels, keep_prob: 0.5})
elif sys.argv[1] == "server":
    print("server")
else:
    saver.restore(sess, tf.train.latest_checkpoint("/Users/kevin/Documents/Python/facial-detection/"))
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
    print(pr)

    return "argmax of images"



run(host='localhost', port=8000)
