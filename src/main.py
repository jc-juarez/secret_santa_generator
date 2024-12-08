import argparse
from secret_santa_service import SecretSantaService

# Usage example: python main.py -send_backup_email true -debug_results true -send_whatsapp_messages true
def main():
    # Parse command-line arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-send_backup_email", 
        type=lambda x: x.lower() == 'true',
        default=True,
        help="Set this flag to true to send a backup email with the generated arrangement.")
    parser.add_argument(
        "-debug_results", 
        type=lambda x: x.lower() == 'true',
        default=True,
        help="Set this flag to true to print to the console the generated arrangement.")
    parser.add_argument(
        "-send_whatsapp_messages", 
        type=lambda x: x.lower() == 'true',
        default=True,
        help="Set this flag to true to send whatsapp messages to present givers.")
    args = parser.parse_args()
    send_backup_email = args.send_backup_email
    debug_results = args.debug_results
    send_whatsapp_messages = args.send_whatsapp_messages

    # Process secret santa arrangement.
    secret_santa_service = SecretSantaService(SecretSantaService.PARTICIPANTS_FILE_PATH)
    secret_santa_service.process_secret_santa_arrangement(
        send_backup_email,
        debug_results,
        send_whatsapp_messages)

if __name__ == '__main__':
    main()