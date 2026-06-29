def is_year_leap(year):

    if year % 4 == 0:
        return True

    else:
        return False









num = int(input("Введите год: "))
result = is_year_leap(num)
print(f"год {num}: {result}")