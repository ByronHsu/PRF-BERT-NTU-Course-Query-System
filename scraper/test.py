import pickle
import re

def load_obj(name ):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

_dict = load_obj('course')

p = re.compile(r'([^\d]+)')
_dict = load_obj('course')
dep_dict = {}

for (key, value) in _dict.items():
    dep = p.search(key)
    if dep != None:
        dep = dep.group(1)
        if dep not in dep_dict:
            dep_dict[dep] = 0
        else:
            dep_dict[dep] += 1

filt_dep_dict = { k: v for k, v in dep_dict.items() if v > 50}
print(filt_dep_dict)
print(len(filt_dep_dict))