from abc import ABC, abstractmethod


# Task 1
class Person(ABC):

    def __init__(self, name, age, gender, address):
        self.name = name
        self.age = age
        self.gender = gender
        self.address = address

    def __str__(self):
        return f"Name: {self.name}, Age: {self.age}, Gender: {self.gender}, Address: {self.address}"

    def greet(self, other_person):
        print(f"Hello {other_person.name}! My name is {self.name}.")

    @abstractmethod
    def introduce(self):
        pass

    @staticmethod
    def is_adult(age):
        return age >= 18


# Task 2
class Employee(Person):

    counter = 0

    def __init__(self, name, age, gender, address, salary):
        super().__init__(name, age, gender, address)

        self._salary = salary

        Employee.counter += 1
        self.__employee_id = f"EMP{Employee.counter:02d}"

    def __del__(self):
        Employee.counter -= 1

    @property
    def employee_count(self):
        return Employee.counter

    @property
    def employee_id(self):
        return self.__employee_id

    @property
    def salary(self):
        return self._salary

    @salary.setter
    def salary(self, salary):
        self._salary = salary

    def increase_salary(self, amount):
        self._salary += amount

    def decrease_salary(self, amount):
        self._salary -= amount

    def introduce(self):
        print(f"Hello, my name is {self.name} and I work as an employee.")


# Task 3
class Teacher(Employee):

    counter = 0

    def __init__(self, name, age, gender, address, salary, subjects):
        super().__init__(name, age, gender, address, salary)

        self.subjects = subjects

        Teacher.counter += 1
        self.__teacher_id = f"TEC{Teacher.counter:02d}"

    def __del__(self):
        Teacher.counter -= 1

    @property
    def teacher_count(self):
        return Teacher.counter

    @property
    def teacher_id(self):
        return self.__teacher_id

    def add_subject(self, subject):
        self.subjects.append(subject)

    def remove_subject(self, subject):
        if subject in self.subjects:
            self.subjects.remove(subject)

    def introduce(self):
        return f"My ID is {self.teacher_id} and I teach: {', '.join(self.subjects)}"

    @property
    def employee_id(self):
        raise AttributeError(
            f"{self.__class__.__name__} object has no attribute 'employee_id'"
        )


# Example usage
teacher1 = Teacher(
    "John",
    35,
    "Male",
    "Ranchi",
    50000,
    ["Mathematics", "Physics"]
)

teacher2 = Teacher(
    "Alice",
    30,
    "Female",
    "Delhi",
    45000,
    ["English", "History"]
)

print(teacher1.teacher_id)
print(teacher1.introduce())

teacher1.add_subject("Computer Science")
print(teacher1.introduce())

teacher1.remove_subject("Physics")
print(teacher1.introduce())

print("Teacher count:", teacher1.teacher_count)

# AttributeError
print(teacher1.employee_id)