#importing the needed modules
import unittest
import os

# Function to hide a message inside a text file using zero-width characters
def hide_text_in_file(file_name, message):
    # Convert message to binary (each character into an 8-bit binary string)
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    
    # Replace '0' with zero-width space and '1' with zero-width non-joiner
    hidden_message = binary_message.replace('0', '\u200B').replace('1', '\u200C')

    # Read the existing file content
    with open(file_name, 'r', encoding='utf-8') as file:
        content = file.read()

    # Write back the original content + hidden message
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(content + hidden_message)  # Preserves original content

# Function to extract the hidden message from a text file
def reveal_text_from_file(file_name):
    # Read file content
    with open(file_name, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Extract only the zero-width characters and convert them back to binary
    hidden_binary = ''.join([
        '0' if char == '\u200B' else '1' if char == '\u200C' else ''
        for char in content
    ])
    
    # If no binary message is found, return an empty string
    if not hidden_binary:
        return ""
    
    # Convert binary back to text (8-bit chunks to characters)
    decoded_message = ''.join(
        chr(int(hidden_binary[i:i+8], 2)) 
        for i in range(0, len(hidden_binary), 8)
    )
    
    return decoded_message

# Unit test class for the hide/reveal functions
class TestSteganography(unittest.TestCase):
    def setUp(self):
        """ Set up a test environment with a sample file and message """
        self.test_file = "test_file.txt"
        self.test_message = "Hello, youssef!"
        
        # Create a file with some initial content
        with open(self.test_file, 'w', encoding='utf-8') as file:
            file.write("This is some visible text.")

    def tearDown(self):
        """ Remove the test file after each test """
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_hide_and_reveal_message(self):
        """ Test if a message can be hidden and then correctly retrieved """
        hide_text_in_file(self.test_file, self.test_message)
        revealed_message = reveal_text_from_file(self.test_file)
        self.assertEqual(revealed_message, self.test_message)
    
    def test_no_hidden_message(self):
        """ Test if a file without a hidden message returns an empty string """
        revealed_message = reveal_text_from_file(self.test_file)
        self.assertEqual(revealed_message, "")

    def test_original_content_preserved(self):
        """ Test that original content is not erased when hiding a message """
        with open(self.test_file, 'r', encoding='utf-8') as file:
            original_content = file.read()

        hide_text_in_file(self.test_file, self.test_message)

        with open(self.test_file, 'r', encoding='utf-8') as file:
            new_content = file.read()

        # Ensure the original text is still present in the file
        self.assertTrue(original_content in new_content)

# Main execution: runs hiding, revealing, or unit tests based on user input
if __name__ == "__main__":
    mode = input("Enter mode (hide/reveal/test): ").strip().lower()
    file_name = input("Enter the file name: ").strip()
    
    if mode == "hide":
        message = input("Enter the message to hide: ")
        hide_text_in_file(file_name, message)
        print(f"Message hidden successfully in {file_name}.")
    elif mode == "reveal":
        hidden_message = reveal_text_from_file(file_name)
        if hidden_message:
            print(f"Hidden message revealed: {hidden_message}")
        else:
            print("No hidden message found.")
    elif mode == "test":
        unittest.main()
    else:
        print("Invalid mode! Use 'hide', 'reveal', or 'test'.")
