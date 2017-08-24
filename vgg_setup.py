import numpy as np

from keras.layers import Convolution2D
from keras.layers import ZeroPadding2D
from keras.layers import MaxPooling2D
from keras.models import Sequential
from keras.layers import Lambda
from keras.layers import Flatten
from keras.layers import Dense, Dropout
from keras.utils.data_utils import get_file

def ConvBlock(layers, model, filters):
  # I don't know what all of these separate componenets do but together
  # they constitute a convolutional layer in a deep nn
  for i in range(layers):
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(filters, 3, 3, activation='relu'))
  model.add(MaxPooling2D((2, 2), strides=(2, 2)))
    
def DenseBlock(model):
  # this is pretty standard
  # i expect that there will be a final dense output layer with dimension num_classes
  model.add(Dense(4096, activation='relu'))
  model.add(Dropout(0.5))
    
VGG_MEAN = np.array([123.68, 116.779, 103.939]).reshape((3, 1, 1))
def vgg_preprocess(x):
  x = x - VGG_MEAN
  return x[:, ::-1]

def _make_architecture():
  model = Sequential()
  model.add(Lambda(vgg_preprocess, input_shape=(3, 224, 224)))
  
  ConvBlock(2, model, 64)
  ConvBlock(2, model, 128)
  ConvBlock(3, model, 256)
  ConvBlock(3, model, 512)
  ConvBlock(3, model, 512)
  
  model.add(Flatten())
  DenseBlock(model)
  DenseBlock(model)
  model.add(Dense(1000, activation='softmax'))
  return model


def _initialize_model_weights(model):    
  fpath = get_file('vgg16.h5', 'http://files.fast.ai/models/vgg16.h5', cache_subdir='models')
  model.load_weights(fpath)
    
def make_vgg():
  model = _make_architecture()
  _initialize_model_weights(model)
  return model
