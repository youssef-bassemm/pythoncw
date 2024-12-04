def message_to_binary(message):
    """Convert a string message to binary format."""
    return ''.join(format(ord(char), '08b') for char in message)

def binary_to_message(binary_data):
    """Convert binary data back to a string."""
    chars = [binary_data[i:i + 8] for i in range(0, len(binary_data), 8)]
    return ''.join(chr(int(char, 2)) for char in chars)

def hide_message_rgb(input_image, output_image, secret_message):
    """Hide a message in the RGB channels of a BMP image."""
    with open(input_image, 'rb') as img:
        data = bytearray(img.read())

    # BMP header is 54 bytes; pixel data starts from byte 54
    binary_message = message_to_binary(secret_message) + '1111111111111110'  # End delimiter
    binary_index = 0
    pixel_index = 54  # Start after header

    while binary_index < len(binary_message) and pixel_index + 2 < len(data):
        # Modify RGB channels
        for channel in range(3):  # Red, Green, Blue
            if binary_index < len(binary_message):
                data[pixel_index] = (data[pixel_index] & 254) | int(binary_message[binary_index])
                binary_index += 1
            pixel_index += 1  # Move to next channel or pixel

    if binary_index < len(binary_message):
        raise ValueError("Message too long for the provided image.")

    with open(output_image, 'wb') as img:
        img.write(data)

    print(f"Message hidden in {output_image}.")

def extract_message_rgb(stego_image):
    """Extract a hidden message from the RGB channels of a BMP image."""
    with open(stego_image, 'rb') as img:
        data = bytearray(img.read())

    binary_message = ''
    pixel_index = 54  # Start after BMP header

    while pixel_index + 2 < len(data):
        for channel in range(3):  # Red, Green, Blue
            binary_message += str(data[pixel_index] & 1)
            if binary_message[-16:] == '1111111111111110':  # End delimiter
                binary_message = binary_message[:-16]
                return binary_to_message(binary_message)
            pixel_index += 1

    raise ValueError("No hidden message found or file is corrupted.")

# Main execution
if __name__ == "__main__":
    print("1: Hide a message in an image")
    print("2: Extract a message from an image")
    choice = input("Enter your choice (1/2): ")

    if choice == '1':
        input_image = input("Enter the input BMP image file name (e.g., input.bmp): ")
        output_image = input("Enter the output BMP image file name (e.g., output.bmp): ")
        secret_message = input("Enter the secret message: ")
        try:
            hide_message_rgb(input_image, output_image, secret_message)
        except Exception as e:
            print(f"Error: {e}")
    elif choice == '2':
        stego_image = input("Enter the stego BMP image file name (e.g., output.bmp): ")
        try:
            extracted_message = extract_message_rgb(stego_image)
            print(f"Extracted message: {extracted_message}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Invalid choice.")


