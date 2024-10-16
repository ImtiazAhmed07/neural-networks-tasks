# -*- coding: utf-8 -*-
"""Neural with tensorflow

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1xqMgF8FAmgN_7dhJ_2hlZNzX8bLPchMC
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import tensorflow as tf
from tensorflow.keras.layers import Conv2D, Conv2DTranspose, Reshape, Flatten, Input, UpSampling2D
from tensorflow.keras.models import Model
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.optimizers import Adam

# Display image function
def display_image(image_data, title="Image"):
    plt.imshow(image_data)
    plt.title(title)
    plt.axis('off')
    plt.show()

# Load images from directory
def load_images(directory, image_size=(128, 128)):
    images = []
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            img = Image.open(os.path.join(directory, filename))
            img = img.resize(image_size)  # Resize to desired pixels
            img = np.array(img)
            if len(img.shape) == 2:
                img = np.expand_dims(img, axis=-1)  # Add channel dimension if grayscale
                img = np.repeat(img, 3, axis=-1)  # Convert grayscale to RGB
            images.append(img)
    return np.array(images)

# Define the network architecture using Keras
input_shape = (128, 128, 3)  # Input size for RGB images

input_img = Input(shape=input_shape)
x = Conv2D(64, (3, 3), activation='relu', padding='same')(input_img)
x = Conv2D(128, (3, 3), activation='relu', padding='same', strides=(2, 2))(x)
x = Conv2D(256, (3, 3), activation='relu', padding='same', strides=(2, 2))(x)
x = Flatten()(x)
encoded = Reshape((32, 32, 256))(x)

x = Conv2DTranspose(256, (3, 3), activation='relu', padding='same', strides=(2, 2))(encoded)
x = Conv2DTranspose(128, (3, 3), activation='relu', padding='same', strides=(2, 2))(x)
x = Conv2DTranspose(64, (3, 3), activation='relu', padding='same')(x)
decoded = Conv2D(3, (3, 3), activation='sigmoid', padding='same')(x)

autoencoder = Model(input_img, decoded)
autoencoder.compile(optimizer=Adam(), loss=MeanSquaredError())

# Training function
def train_network(train_data, epochs, batch_size):
    autoencoder.fit(train_data, train_data, epochs=epochs, batch_size=batch_size, shuffle=True)

# Visualize results
def visualize_results(train_data):
    for img in train_data[:5]:
        img = img.reshape(128, 128, 3)
        colorized_output = autoencoder.predict(img.reshape(1, 128, 128, 3))
        colorized_output = (colorized_output[0] * 255).astype(np.uint8)

        plt.figure(figsize=(12, 4))
        plt.subplot(1, 3, 1)
        display_image(img, title="Original")
        plt.subplot(1, 3, 2)
        display_image(colorized_output, title="Colorized Output")
        plt.subplot(1, 3, 3)
        display_image(img, title="Original")  # Show original again for comparison
        plt.show()

# Save the model
def save_model():
    autoencoder.save_weights("autoencoder_weights.h5")

# Load the model
def load_model():
    autoencoder.load_weights("autoencoder_weights.h5")

# Evaluate the network on test data
def evaluate_network(test_data):
    total_loss = 0
    for img in test_data:
        img = img.reshape(1, 128, 128, 3)
        output_data = autoencoder.predict(img)
        total_loss += np.mean((output_data - img) ** 2)

    avg_loss = total_loss / len(test_data)
    print(f"Test Loss: {avg_loss}")

if __name__ == "__main__":
    # Example usage

    # Load images from a directory
    train_data = load_images(r"/content/pics")

    # Normalize data
    train_data = train_data.astype(np.float32) / 255.0

    # Train the network
    train_network(train_data, epochs=50, batch_size=16)

    # Visualize some results
    visualize_results(train_data)

    # Save the model
    save_model()

    # Load the model (for testing purposes)
    load_model()

    # Evaluate on test data (using training data for simplicity)
    evaluate_network(train_data)