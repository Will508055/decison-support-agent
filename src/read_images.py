import os
import math
from PIL import Image
import matplotlib.pyplot as plt


def read_image_choice() -> bytes:
    files_list = []

    for root, _, files in os.walk('images'):
        for file in files:
            files_list.append(os.path.join(root, file))
    
    fig, ax = plt.subplots(nrows=math.ceil(len(files_list)/4),
                           ncols=4,
                           figsize=(8, math.ceil(len(files_list)/4) * 2))
    
    for i, path in enumerate(files_list):
        img = Image.open(path).resize((200, 200))
        ax.flat[i].imshow(img)
        ax.flat[i].set_title(str(i + 1))
        ax.flat[i].axis('off')
    
    plt.tight_layout()
    plt.ion()
    plt.show()
    
    while True:
        try:
            choice = int(input(f'Select an image by entering a number (1-{len(files_list)}): '))
            if 1 <= choice <= len(files_list):
                plt.close(fig)
                path = files_list[choice - 1]
                with open(path, 'rb') as img_file:
                    return img_file.read()
            else:
                print(f'Please enter a number between 1 and {len(files_list)}.')
        except ValueError:
            print('Invalid input. Please enter a valid number.')