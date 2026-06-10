from tensorflow import keras
from pathlib import Path
import numpy as np
import json

DATA_PATH = "./BeamHAR-SVR-Data/"

class MyDataset(keras.utils.Sequence):
    def __init__(self, file_type, station, ds_split, batch_size=32):
        super().__init__()
        self.paths = list(Path(DATA_PATH+ds_split).rglob(f"*{station}*{file_type}*.npy"))
        print(f"File count for {ds_split} split: {len(self.paths)}")
        self.batch_size = batch_size
        self.label_dict = json.load(open('label_dict', 'r'))

    def __getitem__(self, idx):
        x = []
        labels = []
        a = idx*self.batch_size
        b = a + self.batch_size
        files = self.paths[a:b]
        for file in files:
            z = np.load(file, 'r')
            x.append(z)
            label = str(file).split("/")[-1].split("_")[0]
            label = self.label_dict[label]
            labels.append([label])
        x = np.vstack([x])
        labels = np.array(labels)
        labels = keras.utils.to_categorical(labels, num_classes=7)
        return x, labels

    def __len__(self):
        return len(self.paths) // self.batch_size