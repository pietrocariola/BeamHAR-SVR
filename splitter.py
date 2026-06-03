import numpy as np
from pathlib import Path
import random

TEST_SPLIT = 0.10
WINDOW_SIZE = 4
SEED = 0

if __name__=='__main__':

    random.seed(SEED)

    path = Path("./BeamHAR-SVR-Data/scenarios")
    
    train = Path("./BeamHAR-SVR-Data/train")
    train.mkdir(exist_ok=True)
    print(f"Train folder created: ok")

    test = Path("./BeamHAR-SVR-Data/test")
    test.mkdir(exist_ok=True)
    print(f"Test folder created: ok")

    files = path.rglob("*_v.npy")
    labels = [file.name.split("_")[0] for file in files]
    labels = list(set(labels))

    for label in labels:
        Path(f"./BeamHAR-SVR-Data/train/{label}").mkdir(exist_ok=True)
        Path(f"./BeamHAR-SVR-Data/test/{label}").mkdir(exist_ok=True)
    print(f"Label folders created: ok")

    files = path.rglob("*_v.npy")
    for i, file in enumerate(files):
        print(f"Processing file {i}", end="\r")
        x = np.load(file, 'r')
        n_windows = x.shape[0] // WINDOW_SIZE
        for j in range(n_windows):
            x = x[j*WINDOW_SIZE:(j+1)*WINDOW_SIZE, :, :, :]
            label = file.name.split("_")[0]
            file_name = file.name.split("/")[-1].split(".")[0]+"_"+str(j).zfill(6)+".npy"
            if random.uniform(0, 1) <= TEST_SPLIT:
                p = Path("./BeamHAR-SVR-Data/test/") / label / file_name
                np.save(p, x)
            else:
                p = Path("./BeamHAR-SVR-Data/train/") / label / file_name
                np.save(p, x)
    print("Files processing: ok")