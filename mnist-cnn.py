import keras
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

# Load MNIST dataset -----------------------------------------------------------
(X_train, y_train), (X_test, y_test) = keras.datasets.mnist.load_data()
# Preprocessing ----------------------------------------------------------------
<<<<<<< HEAD
X_train = X_train.reshape(-1, 28, 28, 1).astype('float32') / 255
X_test = X_test.reshape(-1, 28, 28, 1).astype('float32') / 255
=======
X_train = X_train.reshape(-1, 28, 28, 1).astype('float16') / 255
X_test = X_test.reshape(-1, 28, 28, 1).astype('float16') / 255
>>>>>>> 4db03eb418726a86ac56647343ff78ba6625c4ca
# Define the model -------------------------------------------------------------
model = keras.models.Sequential()

model.add(Conv2D(32, (3, 3), activation='relu', input_shape=[28, 28, 1]))
model.add(Conv2D(64, (3, 3), activation='relu'))
#model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(10, activation='softmax'))

print(model.summary())
# Compile model ----------------------------------------------------------------
model.compile(loss='sparse_categorical_crossentropy',
              optimizer='adam', metrics=['accuracy'])
# Fit the model to the training set --------------------------------------------
model.fit(X_train, y_train, batch_size=32, epochs=10, validation_split=0.2)
# Evaluate model performance ---------------------------------------------------
score = model.evaluate(X_test, y_test)
print('Test accuracy:', score[1])
# Save model -------------------------------------------------------------------
model.save('mnist.h5')
