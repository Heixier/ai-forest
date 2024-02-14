import random

cars = {"my car": "toyota",
        "desmond car": "tesla",
        "auntie car": "ferrari"}

# print(cars['my car'])
# print(cars['auntie car'])

class Person():
    def __init__(self):
        name_list = ["Noah", "Jenny", "Tom", "Diana", 'Gay']
        
        self.name = random.choice(name_list)        
        self.alive = True

# guy = Unit("johnny")
# girl = Unit("Danielle")
# robber = Unit("XiJingPing")

# fake_list = []
# fake_list.append(guy)
# fake_list.append(girl)
# fake_list.append(robber)

people = {}
alive_dict = {}

# for number in ["murderer", "sheriff", "innocent"]:
for number in range(3):
    person = Person()
    people[number] = person

# for k, v in people.items():
#     print(f"{k} {v}")

print(f"{people[2].name} Kill {people[1].name}")
people[1].alive = False

for key, person in people.items():
    if person.alive:
        alive_dict[key] = person

for k, v in alive_dict.items():        
    print(k, v)
    
people[1].alive = True

for key, person in people.items():
    if person.alive:
        alive_dict[key] = person
for k, v in alive_dict.items():
    print(k, v)
    
print(f" {people[0].name} Revived {people[1].name}")