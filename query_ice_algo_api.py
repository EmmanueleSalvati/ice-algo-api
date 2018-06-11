from requests import post


g = post('http://localhost:5000/',
         data={
            'ship_n': '3384',
            'dep_zip': 90003,  # 12345,
            'dest_zip': 11201,
            'dep_date': '06-11-2018',
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
