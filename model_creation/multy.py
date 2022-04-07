import tensorflow as tf
from tensorflow.python.keras.engine.base_layer import Layer
class processing(Layer):


    def __init__(self, x, **kwargs):
        super(processing, self).__init__(**kwargs)
        self.x = x


    def call(self, inputs):
        return tf.multiply(inputs,self.x)


    def compute_output_shape(self, input_shape):
        return self.x.shape

 
