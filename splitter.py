import numpy as np
from pathlib import Path
import random
import json

if __name__=='__main__':

    config = json.load(open('config.json', 'r'))   
    file_type = config['file_type'].lower()
    window_size = config['window_size']
    val_split_pct = config['val_split_pct']
    test_split_pct = config['test_split_pct']
    random.seed(config['seed'])
    np.random.seed(config['seed'])

    path = Path("./BeamHAR-SVR-Data/scenarios")
    
    train = Path("./BeamHAR-SVR-Data/train")
    train.mkdir(exist_ok=True)
    print(f"Train folder created: ok")

    val = Path("./BeamHAR-SVR-Data/val")
    val.mkdir(exist_ok=True)
    print(f"Validation folder created: ok")

    test = Path("./BeamHAR-SVR-Data/test")
    test.mkdir(exist_ok=True)
    print(f"Test folder created: ok")

    files = path.rglob(f"*_{file_type}.npy")
    labels = [file.name.split("_")[0] for file in files]
    labels = list(set(labels))
    labels = sorted(labels)

    for label in labels:
        Path(f"./BeamHAR-SVR-Data/train/{label}").mkdir(exist_ok=True)
        Path(f"./BeamHAR-SVR-Data/val/{label}").mkdir(exist_ok=True)
        Path(f"./BeamHAR-SVR-Data/test/{label}").mkdir(exist_ok=True)
    print(f"Label folders created: ok")

    label_dict = {}
    for i, label in enumerate(labels):
        label_dict[label] = i
    with open('label_dict.json', 'w') as f:
        json.dump(label_dict, f, indent=4)
    print(f"Label dict created: ok")

    files = path.rglob(f"*_{file_type}.npy")
    for i, file in enumerate(files):
        print(f"Processing file {i}", end="\r")
        x = np.load(file, 'r')
        n_windows = int(x.shape[0] // window_size)
        for j in range(n_windows):
            if file_type == 'bfa':
                y = x[j*window_size:(j+1)*window_size, :, :]
            elif file_type == 'v':
                y = x[j*window_size:(j+1)*window_size, :, :, :]
            label = file.name.split("_")[0]
            file_name = file.name.split("/")[-1].split(".")[0]+"_"+str(j).zfill(6)+".npy"
            if random.uniform(0, 1) <= test_split_pct:
                p = Path("./BeamHAR-SVR-Data/test/") / label / file_name
                np.save(p, y)
            else:
                if random.uniform(0, 1) <= val_split_pct:
                    p = Path("./BeamHAR-SVR-Data/val/") / label / file_name
                    np.save(p, y)
                else:
                    p = Path("./BeamHAR-SVR-Data/train/") / label / file_name
                    np.save(p, y)
    print("Files processing: ok")