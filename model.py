from keras import layers, models

def getModel(window_size=10, classes=7):
    model = models.Sequential()
    model.add(
        layers.Conv2D(
            128,
            (3, 3),
            activation="relu",
            padding="same",
            input_shape=(window_size, 234, 6),
        )
    )
    model.add(layers.Conv2D(128, (3, 3), activation="relu", padding="same"))
    # model.add(layers.BatchNormalization())
    # model.add(layers.Activation("relu"))

    model.add(layers.Conv2D(64, (3, 3), activation="relu", padding="same"))
    model.add(layers.Conv2D(64, (3, 3), activation="relu", padding="same"))
    # model.add(layers.BatchNormalization())
    # model.add(layers.Activation("relu"))
    model.add(layers.MaxPooling2D(pool_size=(2, 4)))

    model.add(layers.Conv2D(32, (3, 3), activation="relu", padding="same"))
    model.add(layers.Conv2D(32, (3, 3), activation="relu", padding="same"))
    # model.add(layers.BatchNormalization())
    # model.add(layers.Activation("relu"))
    model.add(layers.MaxPooling2D(pool_size=(2, 4)))

    model.add(layers.Flatten())
    model.add(layers.Dense(classes, activation="softmax"))
    
    model.summary()
    return model