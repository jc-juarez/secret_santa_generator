# *************************************
# Secret Santa Generator
# 'secret_santa_person.py'
# Author: jcjuarez
# *************************************

class SecretSantaPerson:

    def __init__(self, name: str, phone_number: str):
        self.name = name
        self.phone_number = phone_number

    def to_string(self):
        return f'[Name: {self.name}, Number: {self.phone_number}]'