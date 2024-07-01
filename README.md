# Cryptography and Steganography Project

This project combines the concepts of Cryptography and Steganography to securely encrypt and hide messages within digital images. Cryptography is used to encrypt the message using XOR operations with a key derived from a user-provided password. Steganography hides the encrypted message within the pixels of a carrier image using the Least Significant Bit (LSB) technique.

Features
    Encryption: Encrypts the user-provided message using a password-generated key.
    Steganography: Embeds the encrypted message into a selected image using LSB technique.
    Decryption: Extracts and decrypts the hidden message from the modified image using the correct password.
Usage
    Encryption and Embedding
    1.Input Password:
        Enter a 3-character password which will be used for key generation.

    2.Key Generation:
        Convert each character of the password into a 7-bit ASCII binary.
        Perform XOR operations among these binaries to generate a 7-bit key.
    
    3.Input Message:
        Provide the message to be encrypted and embedded. Ensure the message does not exceed 177 characters.

    4.Encrypting Message:
        Convert each character of the message into a 7-bit ASCII binary.
        XOR each binary character with the generated key to produce the encrypted binary message.

    5.Select Image:
        Choose a carrier image (.png or .jpg) into which the message will be embedded.

    6.Embedding Process:
        Convert the image into a matrix of pixel values.
        Embed the binary length of the message into the first 7 rows, 1st column using LSB.
        Embed the encrypted message into subsequent rows, 1st column using LSB.
        Save the modified image.

    Decryption and Extraction
    1.Input Password:
        Enter the same 3-character password used during encryption.

    2.Key Generation:
        Convert each character of the password into a 7-bit ASCII binary.
        Perform XOR operations among these binaries to generate the same 7-bit key used for encryption.
    
    3.Select Image:
        Choose the modified image (.png or .jpg) containing the hidden message.

    4.Extracting Process:
        Convert the image into a matrix of pixel values.
        Extract the binary length of the message from the first 7 rows, 1st column using LSB.
        Extract the encrypted message from subsequent rows, 1st column using LSB.

    5.Decrypting Message:
        XOR each 7-bit encrypted binary with the key to recover the original plaintext message.

        
