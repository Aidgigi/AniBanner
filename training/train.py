import tensorflow as tf
import numpy as np

from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

from tensorflow.python.compiler.mlcompute import mlcompute
from tensorflow.python.training.tracking import base

mlcompute.set_mlc_device(device_name = "gpu")

image_size = (224, 224)
b_size = 32

tds = tf.keras.preprocessing.image_dataset_from_directory(
    shuffle = True,
    directory = "set",
    validation_split = 0.2,
    subset = "training",
    seed = 123,
    image_size = image_size,
    batch_size = b_size
)

vds = tf.keras.preprocessing.image_dataset_from_directory(
    shuffle = True,
    directory = "set",
    validation_split = 0.2,
    subset = "validation",
    seed = 123,
    image_size = image_size,
    batch_size = b_size
)

data_augmentation = tf.keras.Sequential([
  tf.keras.layers.experimental.preprocessing.RandomFlip('horizontal'),
  tf.keras.layers.experimental.preprocessing.RandomRotation(0.2),
])


preprocess_input = tf.keras.applications.mobilenet_v2.preprocess_input
rescale = tf.keras.layers.experimental.preprocessing.Rescaling(1./127.5, offset= -1)

image_shape = image_size + (3, )
base_model = tf.keras.applications.MobileNetV2(
    input_shape = image_shape,
    include_top = False,
    weights = 'imagenet'
)

image_batch, label_batch = next(iter(tds))
feature_batch = base_model(image_batch)

base_model.trainable = False

global_average_layer = tf.keras.layers.GlobalAveragePooling2D()
feature_batch_average = global_average_layer(feature_batch)

prediction_layer = tf.keras.layers.Dense(1)
prediction_batch = prediction_layer(feature_batch_average)


inputs = tf.keras.Input(shape = (224, 224, 3))
x = data_augmentation(inputs)
x = preprocess_input(x)
x = base_model(x, training = False)
x = global_average_layer(x)
x = tf.keras.layers.Dropout(0.2)(x)
outputs = prediction_layer(x)
model = tf.keras.Model(inputs, outputs)

base_learning_rate = 0.0001

model.compile(
    optimizer = tf.keras.optimizers.Adam(lr=base_learning_rate),
    loss = tf.keras.losses.BinaryCrossentropy(from_logits=True),
    metrics = ['accuracy']
)

epochs = 10

history = model.fit(
    tds,
    epochs = epochs,
    validation_data = vds
)

model.save("trained_model")