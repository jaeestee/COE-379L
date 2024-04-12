from flask import Flask, request
import tensorflow as tf
import os
from tensorflow.keras.layers.experimental.preprocessing import Rescaling
import shutil


app = Flask(__name__)

model = tf.keras.models.load_model('models/lenet5.keras')

@app.route('/models/buildings/v1', methods=['GET'])
def model_info():
    return {
        "version": "v1",
        "name": "buildings",
        "description": "Classify images of buildings as containing damage or not containing damage",
        "number_of_parameters": 2499822
    }

def preprocess_input(path, filename):
    """
    Takes a path that the user-inputed and pre-process it so that it can be used with the model.
    This function could raise an exception.
    """

    #removes the directory in case this is called multiple times.
    #It makes sure the data preprocessing happens to the file requested.
    shutil.rmtree('test/test', ignore_errors=True)

    #if the directory doesn't exist, create it
    if not os.path.exists('test/test'):
        os.makedirs('test/test')

    #adding the file to the test directory
    shutil.copyfile(path, './test/test/' + filename)

    path = 'test/'
    img_height = 150
    img_width = 150

    #data preprocessing
    data = tf.keras.utils.image_dataset_from_directory(
        path,
        batch_size = 1,
        seed = 123,
        image_size = (img_height, img_width)
    )

    rescale = Rescaling(scale=1.0/255)

    # then add an extra dimension
    return data.map(lambda image, label:(rescale(image), label))

@app.route('/models/buildings/v1', methods=['POST'])
def classify_buildings_image():
    path = request.json.get('path')
    if not path:
        return {"error": "The `path` field is required"}, 404
    try:
        pathinput = path.split('/')
        filename = pathinput[len(pathinput) - 1]
        
        data = preprocess_input(path, filename)
        results = model.predict(data).tolist()
    except Exception as e:
        return {"error": f"Could not process the `path` field; details: {e}"}, 404
    return { "result": {"image name": filename, "damaged confidence score": results[0][0], 'not damaged confidence score': results[0][1]}}


# start the development server
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
