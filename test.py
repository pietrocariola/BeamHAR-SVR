from dataset import MyDataset
from keras.models import load_model
from sklearn.metrics import confusion_matrix
import numpy as np
import json
import seaborn as sns
import matplotlib.pyplot as plt

def main():
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    file_type = config['file_type']
    station = config['stations'][0]
    model = load_model('./model.keras')
    test_gen = MyDataset(file_type=file_type, station=station, ds_split='test', batch_size=1)
    final_loss, final_accuracy = model.evaluate(test_gen)
    output_dict = {
        'final_loss': final_loss,
        'final_accuracy': final_accuracy
    }

    with open('output.json', 'w') as f:
        json.dump(output_dict, f, indent=4)

    print("Final Loss: {}, Final Accuracy: {}".format(final_loss, final_accuracy))

    with open('label_dict.json', 'r') as f:
        label_dict = json.load(f)

    Y_true = []
    Y_pred = []

    for x, y in test_gen:
        Y_true.append(np.argmax(y, axis=1))
        Y_pred.append(np.argmax(model.predict(x), axis=1))

    Y_true = np.concatenate(Y_true, axis=0)
    Y_pred = np.concatenate(Y_pred, axis=0)

    cm = confusion_matrix(Y_true, Y_pred)

    plt.figure(figsize=(24, 24))
    ax = sns.heatmap(
        cm,
        cmap=plt.cm.Greens,
        annot=True,
        square=True,
        xticklabels=list(label_dict.keys()),
        yticklabels=list(label_dict.keys()),
    )
    ax.set_ylabel("Actual", fontsize=20)
    ax.set_xlabel("Predicted", fontsize=20)
    plt.savefig('./cm.png', dpi=300)

if __name__=="__main__":
    main()