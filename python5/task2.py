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


# Example usage
e1 = Employee("Nikhil", 25, "Male", "Ranchi", 30000)
e2 = Employee("Riya", 28, "Female", "Delhi", 40000)

print(e1)
print(e1.employee_id)
print(e2.employee_id)

print("Employee count:", e1.employee_count)

print("Salary:", e1.salary)

e1.increase_salary(5000)
print("After increase:", e1.salary)

e1.decrease_salary(2000)
print("After decrease:", e1.salary)

e1.salary = 35000
print("After setting salary:", e1.salary)

e1.introduce()