# Image Steganography – Hide and Extract Text in an Image
# Language: Python

from PIL import Image

# Convert text to binary
def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)

# Convert binary to text
def binary_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(char, 2)) for char in chars)

# Hide message in image
def encode_image(image_path, message, output_path):
    img = Image.open(image_path)
    pixels = list(img.getdata())

    message += "#####"
    binary_msg = text_to_binary(message)
    msg_index = 0

    new_pixels = []
    for pixel in pixels:
        r, g, b = pixel
        if msg_index < len(binary_msg):
            r = (r & ~1) | int(binary_msg[msg_index])
            msg_index += 1
        if msg_index < len(binary_msg):
            g = (g & ~1) | int(binary_msg[msg_index])
            msg_index += 1
        if msg_index < len(binary_msg):
            b = (b & ~1) | int(binary_msg[msg_index])
            msg_index += 1
        new_pixels.append((r, g, b))

    img.putdata(new_pixels)
    img.save(output_path)
    print("Message encoded successfully.")

# Extract message from image
def decode_image(image_path):
    img = Image.open(image_path)
    pixels = list(img.getdata())

    binary_msg = ""
    for pixel in pixels:
        for color in pixel:
            binary_msg += str(color & 1)

    message = binary_to_text(binary_msg)
    return message.split("#####")[0]

# -------- MAIN --------
if __name__ == "__main__":
    print("1. Encode Message")
    print("2. Decode Message")
    choice = int(input("Enter choice: "))

    if choice == 1:
        img_path = input("Enter image path: ")
        secret = input("Enter secret message: ")
        out_path = input("Enter output image path: ")
        encode_image(img_path, secret, out_path)

    elif choice == 2:
        img_path = input("Enter image path: ")
        hidden_msg = decode_image(img_path)
        print("Hidden Message:", hidden_msg)
