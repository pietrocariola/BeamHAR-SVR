import numpy as np
import pathlib
import json

def verify_npy_files(window_size: int, directory: str = ".") -> bool:
    npy_files = list(pathlib.Path(directory).rglob("*.npy"))

    if not npy_files:
        print(f"No .npy files found in '{directory}'")
        return False

    all_valid = True
    failed = []

    for path in sorted(npy_files):
        arr = np.load(path, allow_pickle=False)
        if arr.shape[0] != window_size:
            failed.append((path, arr.shape))
            all_valid = False

    print(f"Checked {len(npy_files)} file(s)\n")

    if failed:
        print(f"\n❌ Failed ({len(failed)}):")
        for p, shape in failed:
            print(f"   {p}  →  shape {shape}")
    return all_valid


if __name__ == "__main__":
    config = json.load(open('config.json', 'r'))   
    window_size = config['window_size']
    valid = True
    directories = ["./BeamHAR-SVR-Data/train", "./BeamHAR-SVR-Data/val", "./BeamHAR-SVR-Data/test"]
    for directory in directories:
        ok = verify_npy_files(window_size, directory)
        if not ok:
            valid = False
    print(f"Splits are valid") if valid else print(f"[error] Split are not valid!")