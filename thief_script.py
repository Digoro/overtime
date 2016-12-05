import Theif
from pig import Pig

pig = Pig()
user_list = pig.getConfluenceIDs()
print("Start Theif")
theif = Theif.Thief('d3VyaWhhbg==', 'ZGhkaHJ0bnMy')
theif.run(user_list)
