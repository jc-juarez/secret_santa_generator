# *************************************
# Secret Santa Generator
# 'secret_santa_node.py'
# Author: jcjuarez
# *************************************

class SecretSantaNode:

    def __init__(self, present_giver, present_receiver):
        self.present_giver = present_giver
        self.present_receiver = present_receiver

    def to_string(self):
        return f'Present Giver: {self.present_giver.to_string()} -> Present Receiver: {self.present_receiver.to_string()}'