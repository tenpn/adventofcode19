import math

with open('day1.txt') as f:
    masses = f.read().splitlines()
print("got", len(masses), "masses")
    
def find_fuel(mass):
    fuel = math.floor(mass/3)-2
    return max(fuel, 0)

def find_fuel_fuel(fuel):
    new_fuel = find_fuel(fuel)
    if new_fuel == 0:
        return 0
    else:
        return new_fuel + find_fuel_fuel(new_fuel)

print("mass", 12, "gives", find_fuel(12))
print("mass", 14, "gives", find_fuel(14))
print("mass", 1969, "gives", find_fuel(1969))
print("mass", 100756, "gives", find_fuel(100756))

total_fuel = 0
for mass in masses:
    module_fuel = find_fuel(int(mass))
    fuel_fuel = find_fuel_fuel(module_fuel)
    total_fuel = total_fuel + module_fuel + fuel_fuel
    
print("total fuel", total_fuel)
