from django.conf import settings
from django.shortcuts import render, redirect
import os
from PIL import Image


# Create your views here.
def home(request):
    return render(request, 'home.html')


def encryption(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        message = request.POST.get('message')
        image_file = request.FILES.get('image')

        # Ensure all required data is present
        if not (password and message and image_file):
            return render(request, 'encryption.html', {'error': 'Please fill in all fields.'})

        # Validate password length and characters (similar as before)
        if len(password) != 3 or not all(32 <= ord(char) <= 126 for char in password):
            raise ValueError('Key must be exactly 3 printable ASCII characters.')

        # Encode message length as a 7-bit binary string
        message_length = len(message)
        if message_length > 127:
            raise ValueError('Message is too long. Maximum length is 127 characters.')
        binary_message_length = bin(message_length)[2:].zfill(7)

        # Encrypt message using XOR
        x = ord(password[0]) ^ ord(password[1])
        y = ord(password[2]) ^ x
        encrypted_message = [format(ord(char) ^ y, '08b') for char in message]
        encrypt_message = ''.join(encrypted_message)

        # Embed binary_message_length and encrypted_message into the image
        img = Image.open(image_file)
        pixels = list(img.getdata())

        # Embed message length into first 7 pixels
        for i in range(7):
            pixel = pixels[i]
            if pixel[0] % 2 == 0 and binary_message_length[i] == '0':
                continue
            elif pixel[0] % 2 == 1 and binary_message_length[i] == '1':
                continue
            else:
                new_pixel = (pixel[0] + 1, pixel[1], pixel[2])
                pixels[i] = new_pixel

        # Embed encrypted message into subsequent pixels
        for i in range(7, 7 + len(encrypt_message)):
            pixel_index = i % len(pixels)
            pixel = pixels[pixel_index]
            if pixel[0] % 2 != int(encrypt_message[i - 7]):
                new_pixel = (pixel[0] + 1, pixel[1], pixel[2])
                pixels[pixel_index] = new_pixel

        img.putdata(pixels)

        # Save the modified image to a temporary file
        output_path = os.path.join('media', 'encrypted_image.png')
        img.save(output_path)

        # Redirect to the success page with image path
        return redirect('encryption_success', image_path='encrypted_image.png')

    else:
        return render(request, 'encryption.html')


def encryption_success(request, image_path):
    context = {
        'image_path': image_path,
    }
    return render(request, 'encryption_success.html', context)


def decryption(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        image_file = request.FILES.get('image')

        # Ensure all required data is present
        if not (password and image_file):
            return render(request, 'decryption.html', {'error': 'Please fill in all fields.'})

        # Validate password length and characters (similar as before)
        if len(password) != 3 or not all(32 <= ord(char) <= 126 for char in password):
            raise ValueError('Key must be exactly 3 printable ASCII characters.')

        # Open image in read mode
        image = Image.open(image_file, 'r')

        # Read LSBs of the first 7 pixels to get decrypted message length
        message_length_string_list = []
        for i in range(7):
            pixel = image.getpixel((i, 0))
            message_length_string_list.append(str(pixel[0] % 2))

        message_length_bin = ''.join(message_length_string_list)
        message_len_int = int(message_length_bin, 2)

        # Read LSBs of subsequent pixels to reconstruct the encrypted message
        message_string = []
        for i in range(7, 7 + message_len_int * 8):
            pixel = image.getpixel((i, 0))
            message_string.append(str(pixel[0] % 2))

        message_bin = ''.join(message_string)

        # Derive y from the key
        x = ord(password[0]) ^ ord(password[1])
        y = ord(password[2]) ^ x
        # Decrypt the message using y
        char_list = []
        for i in range(0, len(message_bin), 8):
            single_extracted_char = message_bin[i:i + 8]
            decrypted_char = chr(int(single_extracted_char, 2) ^ y)
            char_list.append(decrypted_char)

        received_message = ''.join(char_list)
        print(received_message)

        # Redirect to decryption_success view with the decrypted message as parameter
        return redirect('decryption_success', received_message=received_message)

    else:
        return render(request, 'decryption.html')


def decryption_success(request, received_message):
    context = {
        'message': received_message,
    }
    return render(request, 'decryption_success.html', context)
