class Bank():
    name = ''
    city = ''
    zone = ''
    street = ''
    id = 0
    def __init__(self,name,city,zone,street,id):
        self.id = id
        self.name = name
        self.city = city
        self.zone = zone
        self.street = street
