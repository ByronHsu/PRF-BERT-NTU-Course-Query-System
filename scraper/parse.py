from bs4 import BeautifulSoup
import pickle

data = open('./all.html', mode='r')
data = data.read()
soup = BeautifulSoup(data, 'html.parser')

_dict = {}

tr_tags = soup.find_all("tr", align="center")

def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

for tr in tr_tags[1:]:
    x, y = tr.find_all('td'), tr.find_all('a')
    has_img = tr.find_all("img", src="images/cancel.gif")
    if len(x) > 2 and len(y) > 0:
        if not len(has_img):
            _id = str(x[2].string)
            name = str(y[0].string)
        else:
            _id = str(x[4].contents[0][1:])
            name = str(y[0].string)
    print(name, _id)
    _dict[name] = _id
        # input()

ret_dict = {x:i for i,x in _dict.items()}

save_obj(ret_dict, 'course')

