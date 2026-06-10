from torch.utils.data import Dataset, DataLoader
from pathlib import Path
import numpy as np
import torch.nn as nn
from torch.optim import Adam
import torch
from tqdm import tqdm

DATA_PATH = "./BeamHAR-SVR-Data/"

label_dict = {
    "walking": 0,
    "standing up (from floor)": 1,
    "lying down falling": 2,
    "sitting down": 3,
    "standing up (from chair)": 4,
    "lying down": 5,
    "sitting": 6
}

class MyDataset(Dataset):
    def __init__(self, file_type, station, ds_split):
        super().__init__()
        self.paths = list(Path(DATA_PATH+ds_split).rglob(f"*{station}*{file_type}*.npy"))

    def __getitem__(self, idx):
        x = np.load(self.paths[idx], 'r')
        x = torch.tensor(x, dtype=torch.float32)
        x = x.permute(2, 0, 1)
        label = str(self.paths[idx]).split("/")[-1].split("_")[0]
        label = label_dict[label]
        return x, label

    def __len__(self):
        return len(self.paths)
    
class MyModel(nn.Module):
    def __init__(self, in_channels, window_size, n_classes=7):
        super().__init__()
        self.model = nn.Sequential(
            # 1st block
            nn.Conv2d(in_channels=in_channels, out_channels=128, kernel_size=3, padding="same"),
            nn.ReLU(),
            nn.Conv2d(in_channels=128, out_channels=128, kernel_size=3, padding="same"),
            nn.ReLU(),
            nn.BatchNorm2d(num_features=128),
            nn.ReLU(),
            # 2nd block
            nn.Conv2d(in_channels=128, out_channels=64, kernel_size=3, padding="same"),
            nn.ReLU(),
            nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, padding="same"),
            nn.ReLU(),
            nn.BatchNorm2d(num_features=64),
            nn.ReLU(),
            # 3rd block
            nn.MaxPool2d(kernel_size=(2, 1)),
            nn.Conv2d(in_channels=64, out_channels=32, kernel_size=3, padding="same"),
            nn.ReLU(),
            nn.Conv2d(in_channels=32, out_channels=32, kernel_size=3, padding="same"),
            nn.ReLU(),
            nn.BatchNorm2d(num_features=32),
            nn.ReLU(),
            # 4th block
            nn.MaxPool2d(kernel_size=(2, 1)),
            nn.Flatten(),
            nn.Linear(in_features=32*(window_size//4)*234, out_features=n_classes),
            nn.Softmax(dim=1)
        )

    def forward(self, x):
        return self.model(x)

if __name__=="__main__":

    # configs
    batch_size = 32
    in_channels = 6
    window_size = 10
    n_classes = 7
    station = 'sta03'
    print("Configs: ok")

    # datasets
    ds_test = MyDataset("bfa", station, "test")
    print("Datasets: ok")

    # dataloaders
    dl_test = DataLoader(ds_test, batch_size)
    print("Dataloaders: ok")

    model = MyModel(in_channels, window_size, n_classes)
    # model.load_state_dict(torch.load('model.pth'))
    model.eval()
    print("Training setup configured: ok")    
    
    test_hits = 0
    with torch.no_grad():
        print("Starting testing...")
        for (x, label) in tqdm(dl_test):
            pred = model(x)
            test_hits += (pred.argmax(1) == label).type(torch.float).sum()
    test_acc = test_hits / len(ds_test)
    print(f"Test acc: {test_acc}")
    
def test_keras():
    model = load_model('./keras_model.keras')
    test_gen = KerasDataset(file_type='bfa', station='sta03', ds_split='test')
    final_loss, final_accuracy = model.evaluate(test_gen)
    print("Final Loss: {}, Final Accuracy: {}".format(final_loss, final_accuracy))