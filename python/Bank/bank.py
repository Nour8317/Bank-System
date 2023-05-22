class Bank():
    name = ''
    city = ''
    zone = ''
    street = ''
    id = 0
    branches_count = 0
    def __init__(self,name,city,zone,street,id,branch_count = 0):
        self.id = id
        self.name = name
        self.city = city
        self.zone = zone
        self.street = street
        self.branches_count = branch_count
