from requests import post


g = post('http://localhost:5000/',
         data={
            'ship_n': '3384',
            'dep_lat': "33.9657994",  # 12345,
            'dep_long': "-118.27312690000001",
            'dest_lat': "40.698677200000006",
            'dest_long': "-73.98594140000002",
            'dep_date': '07-08-2018',
            'f_weight': 7.5}).json()
print(g)

# t = post('http://localhost:5000/',
#     data={
#         'ship_n': None,
#         'dep_zip': None,
#         'dest_zip': None,
#         'dep_date': None,
#         'f_weight': None})  #.json()

# print(t)
