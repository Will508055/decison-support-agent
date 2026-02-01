import os

def read_image_choice() -> bytes:
    files_list = []

    for root, _, files in os.walk('images'):
        for file in files:
            print(str(len(files_list) + 1) + ': ' + file)
            files_list.append(os.path.join(root, file))
    
    while True:
        try:
            choice = int(input(f'Select an image by entering a number (1-{len(files_list)}): '))
            if 1 <= choice <= len(files_list):
                path = files_list[choice - 1]
                with open(path, 'rb') as img_file:
                    return img_file.read()
            else:
                print(f'Please enter a number between 1 and {len(files_list)}.')
        except ValueError:
            print('Invalid input. Please enter a valid number.')