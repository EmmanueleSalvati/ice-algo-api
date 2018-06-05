from requests import get, post


g = post('http://localhost:5000/',
    data={
        'ship_n': '3384',
        'dep_zip': 12345,
        'dest_zip': 22345,
        'dep_date': '06-06-2018',
        'f_weight': 4.5}).json()
print(g)

# t = post('http://localhost:5000/',
#     data={
#         'ship_n': None,
#         'dep_zip': None,
#         'dest_zip': None,
#         'dep_date': None,
#         'f_weight': None})  #.json()

# print(t)