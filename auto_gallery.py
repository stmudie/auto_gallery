from flask import Flask
from PIL import Image

app = Flask(__name__)

path = '/home/mudies/Documents/scope.png'

@app.route('/image')
def image():
    Image(path)
    

if __name__ == '__main__':
    app.run()
