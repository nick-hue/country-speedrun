import controller

countries = controller.get_countries()

guess = "A"

filtered_countries = [country for country in countries if country.startswith("A")]

print(filtered_countries)