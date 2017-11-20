import os
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)

app.debug = True

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT,'text')
    print "1"
    print target

    if not os.path.isdir(target):
        os.mkdir(target)
    print(request.files.getlist("file"))
    for file in request.files.getlist("file"):
        # print file
        filename = file.filename
        destination = "/".join([target,filename])
        print ("Accept incoming file:", filename)
        print ("Save it to:", destination)
    return render_template("complete.html",file_name = filename)

@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("text", filename)

def display_file(filename):
    target = os.path.join(APP_ROOT,'text')
    destination = "/".join([target, filename])
    file.save(destination)
    s = open(destination, 'r')
    print s.read()
    return render_template("home.html",file_name = filename)


if __name__ == '__main__':
    app.run()