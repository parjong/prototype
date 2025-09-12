#!/usr/bin/env -S uv run --python 3.8 --script
#
# /// script
# dependencies = ["tensorflow==2.6.*"]
# ///

# From https://ai.google.dev/edge/litert/models/convert_tf?_gl=1*o0iml7*_up*MQ..*_ga*Mzk5Mjg4NTkxLjE3NTc2Nzg0OTA.*_ga_P1DBVKWT6V*czE3NTc2Nzg0OTAkbzEkZzAkdDE3NTc2Nzg0OTAkajYwJGwwJGgyMjE2MzE2MDg.#convert_a_keras_model_
import tensorflow as tf

print(tf.__version__)

# Create a model using high-level tf.keras.* APIs
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(units=1, input_shape=[1]),
    tf.keras.layers.Dense(units=16, activation='relu'),
    tf.keras.layers.Dense(units=1)
])
model.compile(optimizer='sgd', loss='mean_squared_error') # compile the model
model.fit(x=[-1, 0, 1], y=[-3, -1, 1], epochs=5) # train the model
# (to generate a SavedModel) tf.saved_model.save(model, "saved_model_keras_dir")

# Convert the model.
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save the model.
with open('model.tflite', 'wb') as f:
  f.write(tflite_model)
