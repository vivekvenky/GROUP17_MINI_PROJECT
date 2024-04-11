from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os

class Model:
    def __init__(self):              
        loaded_model = load_model('fetal_brain_model_two.h5')       
        files = os.listdir('uploads')
        print(files, files[0])
        path_of_image = rf'uploads\{files[0]}'        
        test_image_path = path_of_image
        processed_image = self.preprocess_image(test_image_path)
        prediction = loaded_model.predict(processed_image)
        prediction_class = 1 if prediction > 0.5 else 0
        self.prediction_result = self.predict_img(prediction_class,path_of_image)  
        print(self.prediction_result)   
           

    def predict_img(self,prediction_class,path_of_image):

       # print("Predicted Class:", prediction_class)
        if prediction_class == 0:
            return "Unhealthy" 
        else:
            return "Healthy"
            os.remove(path_of_image)

    def preprocess_image(self, image_path):
        img = image.load_img(image_path, target_size=(150, 150))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        return img_array

    