from secret_santa_service import SecretSantaService

def main():
    secret_santa_service = SecretSantaService(SecretSantaService.SECRET_SANTA_FILE_NAME)
    secret_santa_service.process_secret_santa_arrangement()

if __name__ == '__main__':
    main()