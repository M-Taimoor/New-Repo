import sys
import io
from docx import Document
import PyPDF2

# Dictionary mapping characters to their Braille equivalents
braille_dict = {
    'A': [1, 0, 0, 0],
    'B': [1, 1, 0, 0],
    'C': [1, 0, 1, 0],
    'D': [1, 0, 1, 1],
    'E': [1, 0, 0, 1],
    'F': [1, 1, 1, 0],
    'G': [1, 1, 1, 1],
    'H': [1, 1, 0, 1],
    'I': [0, 1, 1, 0],
    'J': [0, 1, 1, 1],
    'K': [1, 0, 0, 0],
    'L': [1, 1, 0, 0],
    'M': [1, 0, 1, 0],
    'N': [1, 0, 1, 1],
    'O': [1, 0, 0, 1],
    'P': [1, 1, 1, 0],
    'Q': [1, 1, 1, 1],
    'R': [1, 1, 0, 1],
    'S': [0, 1, 1, 0],
    'T': [0, 1, 1, 1],
    'U': [1, 0, 0, 0],
    'V': [1, 1, 0, 0],
    'W': [0, 1, 1, 1],
    'X': [1, 0, 1, 0],
    'Y': [1, 0, 1, 1],
    'Z': [1, 0, 0, 1],
    '0': [0, 0, 1, 1],
    '1': [1, 0, 0, 0],
    '2': [1, 1, 0, 0],
    '3': [1, 0, 1, 0],
    '4': [1, 0, 1, 1],
    '5': [1, 0, 0, 1],
    '6': [1, 1, 1, 0],
    '7': [1, 1, 1, 1],
    '8': [1, 1, 0, 1],
    '9': [0, 1, 1, 0],
    '.': [1, 1, 1, 0],
    ',': [1, 0, 1, 1],
    '!': [1, 0, 0, 0],
    '?': [0, 1, 0, 0],
    ' ': [0, 0, 0, 0]  # Space handling
}

# Unicode Braille patterns for visual representation
unicode_braille_patterns = {
    1: '⠁',  # Dot 1
    2: '⠃',  # Dot 2
    4: '⠉',  # Dot 3
    8: '⠙',  # Dot 4
    16: '⠑',  # Dot 5
    32: '⠋',  # Dot 6
    64: '⠛',  # Dot 7
    128: '⠓',  # Dot 8
    0: '⠿'  # No dots (for unsupported characters)
}


def translate_to_braille(text):
    """Translates a given text to Braille."""
    try:
        braille_output = []
        for char in text:
            # Check if the character is in the Braille dictionary
            if char.upper() in braille_dict:
                braille_output.append(braille_dict[char.upper()])
            else:
                braille_output.append([0, 0, 0, 0])  # Placeholder for unsupported characters
        return braille_output
    except Exception as e:
        print(f"An error occurred during translation: {e}")
        return None


def process_text_file(file_path):
    """Processes a text file and prints its Braille translation."""
    try:
        if file_path.endswith('.docx'):
            document = Document(file_path)
            text = '\n'.join(paragraph.text for paragraph in document.paragraphs)
        elif file_path.endswith('.pdf'):
            with open(file_path, 'rb') as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                text = '\n'.join(page.extract_text() for page in reader.pages)
        else:
            raise ValueError(f"Unsupported file format: {file_path}")

        braille_output = translate_to_braille(text)
        if braille_output:
            print("Braille Output:")
            for line in braille_output:
                print(' '.join(unicode_braille_patterns[dot] for dot in line))
        else:
            print("Translation failed.")
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    """Main function to handle command-line arguments and process input text or files."""
    if len(sys.argv) < 2:
        print("Please provide input text or a file path.")
        return

    input_text = sys.argv[1]
    if input_text.endswith(('.txt', '.docx', '.pdf')):
        process_text_file(input_text)
    else:
        braille_output = translate_to_braille(input_text)
        if braille_output:
            print("Braille Output:")
            for line in braille_output:
                print(' '.join(unicode_braille_patterns[dot] for dot in line))
        else:
            print("Translation failed.")


if __name__ == "__main__":
    main()