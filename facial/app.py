import os
import tensorflow as tf
import numpy as np
from tensorflow import keras
from skimage import io
from tensorflow.keras.preprocessing import image
from db_connector import Auth,DBRegister

# Flask utils
from flask import Flask, redirect, url_for, request, render_template,session
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = '6qSe4jVkmGmurU66qSe4jVkmGmurU6'

# Model saved with Keras model.save()

# You can also use pretrained model from Keras
# Check https://keras.io/applications/

model =tf.keras.models.load_model('model_filter.h5',compile=True)
print('Model loaded. Check http://127.0.0.1:5000/')


def model_predict(img_path, model):
    img = image.load_img(img_path, grayscale=True, target_size=(48, 48))
    show_img = image.load_img(img_path, grayscale=False, target_size=(200, 200))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis = 0)
    x /= 255
    # x = image.img_to_array(img)
    # x = np.expand_dims(x, axis=0)
    # x = np.array(x, 'float32')
    # x /= 255
    preds = model.predict(x)
    return preds



@app.route('/', methods=['GET'])
def index():
    # Main page
    if session.get('loggedin', False):
        return render_template('index.html')
    else:
        return redirect('/login')

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if session.get('loggedin', False):
        if request.method == 'POST':
            # Get the file from post request
            f = request.files['file']

            # Save the file to ./uploads
            basepath = os.path.dirname(__file__)
            file_path = os.path.join(
                basepath, 'uploads', secure_filename(f.filename))
            f.save(file_path)

            # Make prediction
            preds = model_predict(file_path, model)
            print(preds[0])

            # x = x.reshape([64, 64]);
            disease_class = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
            a = preds[0]
            m=0.000000000000000000001
            for i in range(0,len(a)):
                if a[i]>m:
                    m=a[i]
                    ind=i
            # ind=np.argmax(a)
            print('Prediction:', disease_class[ind])
            result= 'Emotion is'+'  '+disease_class[ind]
            return result
        return None
    else:
        return redirect('/login')

@app.route('/logout')
def logout():
    session['loggedin'] = False
    session['username'] = None
    return redirect('/login')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.form.get('username') is None:
        return render_template('login.html')
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        if Auth(username,password):
            session['username'] = username
            session['loggedin'] = True
            return redirect('/')
        else:
            return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.form.get('username') is None:
        return render_template('register.html')
    else:
        username = request.form.get("username")
        email = request.form.get("email")
        password2 = request.form.get("password2")
        password1 = request.form.get("password1")
        if password1 == password2:
            DBRegister(username,email,password1)
            return redirect('/login')
        else:
            return render_template('register.html')






if __name__ == '__main__':
    app.run(debug=True,threaded = False)
