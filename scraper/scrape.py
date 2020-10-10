import requests

my_params = {
    'current_sem': '107-2',
    'cstype': 1,
    'alltime': 'yes',
    'allproced':'yes',
    'allsel':'yes',
    'startrec': 10000,
    'page_cnt': 2500,
    'Submit22':'%Acd%B8%DF',
}

r = requests.post('http://nol2.aca.ntu.edu.tw/nol/coursesearch/search_result.php', params = my_params)
# print(r.text)
r.encoding = 'Big5'
f = open('3.html', mode='w')
f.write(r.text)