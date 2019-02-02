from bottle import route, run, template, static_file, get, post, request
from preprocess import draw_base64
import base64

# ios posts front end every 0.1 seconds
# web gets image every 0.1 seconds, keeping a counter
# when the counter reaches 6, web sends request for authenticate and resets the counter it has
image = ""
images = []

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
    "run the nn shit on all of images and append to result"

    return "argmax of images"



run(host='localhost', port=8000)
