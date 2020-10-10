import pickle
import re
from sklearn.manifold import TSNE
import pandas as pd
import matplotlib.pyplot as plt

def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

_map = {'PE': 80, 'CHIN': 89, 'FL': 118, 'LS': 67, 'Hist': 57, 'ECON': 66, 'Chem': 55, 'Psy': 60, 'LAW': 134, 'PS': 81, 'Med': 100, 'PT': 73, 'CDent': 69, 'CIE': 84, 'CSIE': 56, 'EE': 82}
data = load_obj('embedding_elmo_seg')

p = re.compile(r'([^\d]+)')

# 濾掉太少出現的
label = [p.search(k).group(1) for k, v in data.items() if p.search(k).group(1) in _map]
embed = [v for k, v in data.items() if p.search(k).group(1) in _map]
print(label)

XY = TSNE(n_components=2).fit_transform(embed)
print(XY.shape)
X = XY[:, 0]
Y = XY[:, 1]


df = pd.DataFrame({'c': label, 'x': X, 'y': Y})

df['col'] = df.c.astype('category').cat.codes

cmap = plt.cm.get_cmap('jet', df.c.nunique())
ax = df.plot.scatter(
    x='x',y='y', c='col',
    cmap=cmap
)

plt.show()