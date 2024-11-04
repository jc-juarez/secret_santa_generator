import random
from secret_santa_node import SecretSantaNode
from secret_santa_person import SecretSantaPerson

class SecretSantaService:

    # Secret santa names list file name.
    # This file needs to be on the same directory as the secret santa tool.
    SECRET_SANTA_FILE_NAME = 'secret_santa_list.txt'

    def __init__(self, secret_santa_file_name: str) -> None:
        people_key_value_pairs = SecretSantaService.read_key_value_pairs(secret_santa_file_name)
        secret_santa_people = []
        for name, phone_number in people_key_value_pairs.items():
            secret_santa_people.append(SecretSantaPerson(name, phone_number))
        self.secret_santa_people = secret_santa_people

        print("\nParsed secret santa information:")
        for person in self.secret_santa_people:
            print(f'[Name: {person.name} | Phone Number: {person.phone_number}]')
        print("")

    @staticmethod
    def read_key_value_pairs(secret_santa_file_name: str) -> dict:
        key_value_pairs = {}
        with open(secret_santa_file_name, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    key, value = line.split('=', 1)
                    key_value_pairs[key.strip()] = value.strip()
        return key_value_pairs
        
    def process_secret_santa_arrangement(self) -> None:
        # Suffle the list of secret santa people
        # in order to create a ring of coordinated assignments.
        random.shuffle(self.secret_santa_people)

        # Create the coordinated ring by assigning a giver-receiver
        # model in a ['n' to 'n+1'] model.
        coordinated_ring = []
        for index in range(len(self.secret_santa_people) - 1):
            coordinated_ring.append(SecretSantaNode(self.secret_santa_people[index], self.secret_santa_people[index+1]))

        # Finally, assign the remaining coordination as ['list_size' to 0].
        coordinated_ring.append(SecretSantaNode(self.secret_santa_people[len(self.secret_santa_people) - 1], self.secret_santa_people[0]))

        print("Generated random assignments:")
        for node in coordinated_ring:
            print(f'[Present Giver: {node.present_giver.name} | Present Receiver: {node.present_receiver.name}]')
        print("")  