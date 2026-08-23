from typing import TypedDict

class Person(TypedDict):
    name : str
    age : int 


new_person = Person(name='zaid',age=10)

print(new_person)