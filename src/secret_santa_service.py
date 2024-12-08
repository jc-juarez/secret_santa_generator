import os
import random
import smtplib
import pywhatkit
from secret_santa_node import SecretSantaNode
from secret_santa_person import SecretSantaPerson

class SecretSantaService:

    # Secret santa names list file name.
    # Defaults to one directory above the secret santa tool source code.
    PARTICIPANTS_FILE_PATH = '../participants_list.txt'

    def __init__(self, participants_file_path: str) -> None:
        people_key_value_pairs = SecretSantaService.read_key_value_pairs(participants_file_path)
        secret_santa_people = []
        for name, phone_number in people_key_value_pairs.items():
            secret_santa_people.append(SecretSantaPerson(name, phone_number))
        self.secret_santa_people = secret_santa_people

        print("\nParsed secret santa information:")
        for person in self.secret_santa_people:
            print(person.to_string())
        print("")

    @staticmethod
    def read_key_value_pairs(participants_file_path: str) -> dict:
        key_value_pairs = {}
        with open(participants_file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    key, value = line.split('=', 1)
                    key_value_pairs[key.strip()] = value.strip()
        return key_value_pairs

    @staticmethod
    def send_email_backup(assignments_message: str) -> None:
        email_message = 'Subject: {}\n\n{}'.format("[Test] Secret Santa Results Backup", assignments_message)
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(os.environ.get("EMAIL_USERNAME"), os.environ.get("EMAIL_PASSWORD"))
            smtp.sendmail(os.environ.get("EMAIL_USERNAME"), os.environ.get("EMAIL_USERNAME"), email_message)

    @staticmethod
    def send_whatsapp_messages(coordinated_ring) -> None:
        for node in coordinated_ring:
            formatted_message = f'[PRUEBA] *[Intercambio de Regalos 2024]* Hola *{node.present_giver.name}*! La persona a la que le vas a regalar es *{node.present_receiver.name}*. El costo del regalo tiene que ser de $200. Nadie sabe quien le va a regalar a quien, ni siquiera yo porque este mensaje se encuentra automatizado.'
            pywhatkit.sendwhatmsg_instantly(node.present_giver.phone_number, formatted_message, 8, True)

    def process_secret_santa_arrangement(self,
        send_backup_email_flag: bool,
        debug_results_flag: bool,
        send_whatsapp_messages_flag: bool) -> None:
        # Shuffle the list of secret santa people
        # in order to create a ring of coordinated assignments.
        random.shuffle(self.secret_santa_people)

        # Create the coordinated ring by assigning a giver-receiver
        # model in a ['n' to 'n+1'] model.
        coordinated_ring = []
        for index in range(len(self.secret_santa_people) - 1):
            coordinated_ring.append(SecretSantaNode(self.secret_santa_people[index], self.secret_santa_people[index+1]))

        # Finally, assign the remaining coordination as ['list_size' to 0].
        coordinated_ring.append(SecretSantaNode(self.secret_santa_people[len(self.secret_santa_people) - 1], self.secret_santa_people[0]))

        assignments_message = ""
        for node in coordinated_ring:
            assignments_message += node.to_string() + "\n"

        if debug_results_flag:
            print("Generated random assignments:")
            print(assignments_message)

        if send_backup_email_flag:
            SecretSantaService.send_email_backup(assignments_message)

        if send_whatsapp_messages_flag:
            SecretSantaService.send_whatsapp_messages(coordinated_ring) 