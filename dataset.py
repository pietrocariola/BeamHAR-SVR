import keras
from pathlib import Path
import numpy as np
import json
import random

DATA_PATH = "./BeamHAR-SVR-Data/"

class MyDataset(keras.utils.Sequence):
    def __init__(self, file_type, station, ds_split, batch_size=4):
        super().__init__()
        with open('label_dict.json', 'r') as f:
            self.label_dict = json.load(f)
        self.paths = []
        for k, _ in self.label_dict.items():
            self.paths += list(Path(DATA_PATH+ds_split).rglob(f"{k}_*{station}*{file_type}*.npy"))
        print(f"File count for {ds_split} split: {len(self.paths)}")
        random.shuffle(self.paths)
        self.batch_size = batch_size        
        
    def get_weights(self):
        weights = {}
        for k, v in self.label_dict.items():
            count = 0
            for file in self.paths:
                if str(file).split("/")[-1].split("_")[0] == k:
                    count += 1
            weights[v] = 1/count if count != 0 else 0
        total = sum(weights.values())
        for k, v in weights.items():
            weights[k] = v / total
        return weights

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
        labels = keras.utils.to_categorical(labels, num_classes=len(self.label_dict))
        # x = np.transpose(x, axes=(0, 1, 3, 2))
        return x, labels

    def __len__(self):
        return len(self.paths) // self.batch_size
    
    def class_limiter(self, limit=0):
        class_files = {}
        for k, v in self.label_dict.items():
            class_files[k] = []

        for file in self.paths:
            label = str(file).split("/")[-1].split("_")[0]
            class_files[label].append(file)

        if limit == 0:
            class_count = []
            for k, v in class_files.items():
                class_count.append(len(v))

        limit = min(class_count) if limit == 0 else limit

        self.paths = []
        for k, v in class_files.items():
            for _ in range(limit):
                self.paths.append(random.choice(v))

        random.shuffle(self.paths)

