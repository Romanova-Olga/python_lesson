class Address:
    def __init__(self,index, city, street, home, apartment):
        self.index = index
        self.city = city
        self.street = street
        self.home = home
        self.apartment = apartment

    def __str__(self):
        return f"{self.index}, {self.city}, {self.street}, {self.home}, {self.apartment}"