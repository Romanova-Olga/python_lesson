from smartphone import Smartphone

catalog = [
    Smartphone(brand="Samsung",model="Galaxy",number="+79228873911"),
    Smartphone(brand="Honor",model="s12",number="+79228873911"),
    Smartphone(brand="Xiaomi ",model="red",number="+79228873911"),
    Smartphone(brand="Apple",model="pro",number="+79228873911"),
    Smartphone(brand="LG",model="A15",number="+79228873911"),
]
for smartphone in catalog:
    print(f"{smartphone.brand} - {smartphone.model} - {smartphone.number}")