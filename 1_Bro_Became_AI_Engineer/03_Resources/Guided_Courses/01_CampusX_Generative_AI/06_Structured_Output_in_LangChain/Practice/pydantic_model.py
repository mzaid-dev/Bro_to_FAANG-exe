from pydantic import BaseModel, EmailStr, Field
from typing import Optional
class Student(BaseModel):
    name : str
    age : Optional[int] = None
    email : EmailStr
    cgpa : float = Field(gt=0,lt=10, description="A decimal represent the cgpa of the studnet.")

new_student = {"name":"zaid", "email" : "abc@gmail.com" ,"cgpa" : 5}

student = Student(**new_student)


# print(type(student))
# print(student)
# print(student.name)

student_dict = dict(student)
print(student_dict)
print(type(student_dict))
