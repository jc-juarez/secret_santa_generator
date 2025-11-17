import os
import random
import smtplib
import pywhatkit
from dotenv import load_dotenv
from secret_santa_node import SecretSantaNode
from secret_santa_person import SecretSantaPerson

class SecretSantaService:

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
        load_dotenv("../.env")
        email_message = 'Subject: {}\n\n{}'.format("[PRUEBA] Secret Santa Results Backup 2025", assignments_message)
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(os.environ.get("EMAIL_USERNAME"), os.environ.get("EMAIL_PASSWORD"))
            smtp.sendmail(os.environ.get("EMAIL_USERNAME"), os.environ.get("EMAIL_USERNAME"), email_message)

    @staticmethod
    def send_whatsapp_messages(coordinated_ring) -> None:
        for node in coordinated_ring:
            formatted_message = (
                f"[PRUEBA, NO ES OFICIAL] *[Intercambio de Regalos 2025]* "
                f"Hola *{node.present_giver.name}*! "
                f"La persona a la que le vas a regalar es *{node.present_receiver.name}*. "
                f"El costo del regalo tiene que ser mínimo de $300. "
                f"Nadie sabe quien le va a regalar a quien, ni siquiera yo porque este mensaje "
                f"se encuentra automatizado.")
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
            # At this point, the coordinated ring follows a model of
            # [(PersonA -> PersonB), (PersonB -> PersonC), (PersonC -> PersonD)],
            # implying that the order of the whatsapp messages sent is the order
            # on which the gifts are assigned. Given that each individual node already
            # has all the necessary information for each person, shuffle the coordinated
            # ring for the whatsapp messages phase one last time before sending the messages.
            # This ensures that the order on which the messages were sent does not reveal the
            # order of the gifts to be given by each person.
            random.shuffle(coordinated_ring)
            SecretSantaService.send_whatsapp_messages(coordinated_ring) 