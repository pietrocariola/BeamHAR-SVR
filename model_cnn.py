from keras import layers, models

KERNEL_SIZE = (3, 3)

def getModel(window_size=10, classes=7):
    model = models.Sequential()
    model.add(
        layers.Conv2D(
            128,
            KERNEL_SIZE,
            activation="relu",
            padding="same",
            input_shape=(window_size, 234, 6),
        )
    )
    model.add(layers.Conv2D(128, KERNEL_SIZE, activation="relu", padding="same"))
    model.add(layers.BatchNormalization())
    model.add(layers.Activation("relu"))

    model.add(layers.Conv2D(64, KERNEL_SIZE, activation="relu", padding="same"))
    model.add(layers.Conv2D(64, KERNEL_SIZE, activation="relu", padding="same"))
    model.add(layers.BatchNormalization())
    model.add(layers.Activation("relu"))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(layers.Conv2D(32, KERNEL_SIZE, activation="relu", padding="same"))
    model.add(layers.Conv2D(32, KERNEL_SIZE, activation="relu", padding="same"))
    model.add(layers.BatchNormalization())
    model.add(layers.Activation("relu"))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(layers.Flatten())
    model.add(layers.Dense(classes, activation="softmax"))
    
    model.summary()
    return model