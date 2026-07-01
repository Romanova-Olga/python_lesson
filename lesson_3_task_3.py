from Address import Address
from Mailing import Mailing

to_address = Address(165010, "Калиниград", "Светлая", 15, 5)
from_address= Address(167000, "Сыктывкар", "Петры", 17, 91)
track = "отправление"
cost = 1500

mailing = Mailing(to_address, from_address, cost, track)

print(mailing)