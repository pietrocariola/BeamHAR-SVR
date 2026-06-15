import keras
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from model_cnn import getModel
from dataset import MyDataset
import json

def main():

    with open('config.json', 'r') as f:
        config = json.load(f)

    keras.utils.set_random_seed(config['seed'])
    window_size = config['window_size']
    file_type = config['file_type'].lower()
    station = config['stations'][0].lower()

    with open('label_dict.json', 'r') as f:
        label_dict = json.load(f)

    classes = len(label_dict)

    model = getModel(window_size=window_size, classes=classes)

    train_gen = MyDataset(file_type=file_type, station=station, ds_split='train')
    # train_gen.class_limiter()
    val_gen = MyDataset(file_type=file_type, station=station, ds_split='val')

    learning_rate_reduction = ReduceLROnPlateau(
        monitor="val_loss",
        patience=6,
        verbose=1,
        factor=0.5,
        min_lr=0.00001,
    )

    checkpoint = ModelCheckpoint('./model.keras', verbose=1, save_best_only=True)
    earlystopping = EarlyStopping(monitor="val_loss", min_delta=0.05, patience=10, verbose=1)

    model.compile(
        optimizer=keras.optimizers.Adam(0.0001),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    history = model.fit(
        x=train_gen,
        epochs=100,
        validation_data=val_gen,
        # class_weight=train_gen.get_weights(),
        callbacks=[earlystopping, learning_rate_reduction, checkpoint],
        verbose=1,
    )

    with open('history.json', 'w') as f:
        json.dump(history.history, f, indent=4)

if __name__=="__main__":
    main()