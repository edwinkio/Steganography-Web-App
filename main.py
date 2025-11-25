from dataclasses import dataclass
from PIL import Image as PIL_Image

from drafter import *

def even_or_odd_bit(num: int) -> str:
    """
    Consumes an integer and returns a '1' or '0', deprending on the parity of the number

    Args: 
        num (int): A passed integer

    Returns:
        str: Either a '0' (even) or '1' (odd)
    """
    if num % 2 == 0:
        return '0'
    return '1'

def decode_single_char(intensities: list[int]) -> str:
    """
    Consumes a list of eight integers containing color intensities and returns the ASCII character represented by the intensities

    Args:
        intensites (list[int]): A list of integers representing color intensities

    Returns:
        str: ASCII character represented by the intensities
    """
    binary = ''

    if not intensities or len(intensities) < 8:
        return binary
    
    for number in intensities:
        binary = binary + even_or_odd_bit(number)

    #Converts the binary value to ASCII (the 2 means Base 2 (binary))
    ascii = int(binary, 2)

    return chr(ascii)

def decode_chars(intensities: list[int], characters: int) ->str:
    """
    Consumes a list integers representing color intensities and an integer representing the number of characters
    to decode. It returns a string representing the decoded characters
    
    Args:
        intensites (list[int]): A list of integers representing color intensities
        characters (int): An integer representing the number of characters to decode
    
    Returns:
        str: A string representing the decoded message with a certain amount of characters
    """
    
    #check if it's possible to decode a certain amount of characters
    if len(intensities) != characters * 8:
        return None
    
    message = ''
    modified_intensities = []
    for index in (range(len(intensities) // 8)):

        #decomposes the list of intensities into a list of lists made up of eight element lists
        first_index = index * 8
        last_index = (index *8) + 8
        modified_intensities.append(intensities[first_index:last_index])

    for intensity in modified_intensities:
        message = message + decode_single_char(intensity)
    
    return message

def get_message_length(intensities: list[int], header: int) ->int:
    """
    Consumes a list integers representing color intensities and an integer representing how many
    characters are in the header. It returns a integer representing the how many characters are in the message

    Args:
        intensites (list[int]): A list of integers representing color intensities
        header (int): An integer representing how many characters are in the header
    
    Returns:
        int: An integer representing the how many characters are in the message
    """

    if not header or len(intensities) != header * 8:
        return 0
    
    return(int(decode_chars(intensities, header)))

def get_encoded_message(intensities: list[int]) -> str:
    """
    Consumes a list of color intensities and returns the hidden message. The header will
    always be 3, so the message length will always be less than or equal to 999

    Args:
        intensites (list[int]): A list of integers representing color intensities

    Returns:
        str: The encoded message
    """

    msg_length = get_message_length(intensities[:24], 3)

    #gets the last index at which the message stops
    last_index = (msg_length * 8) + 24
    return decode_chars(intensities[24:last_index], msg_length)

def get_color_values(image: PIL_Image, channel_index: int) -> list[int]:
    """
    Consumes a Pillow Image and an integer representing the channel index of the color values. 
    (0:red, 1:green, 2:blue) 
    and returns a list of integers containing the color intensity values for the specified channel.

    Args:
        image (PIL_Image): A Pillow Image
        channel_index (int): An integer representing which channel to choose from
    
    Returns:
        list[int]: A list of integers containing the color intensity values for the specified channel
    """

    #image.size returns a tuple
    width, length = image.size
    intensities = []

    for w in range(width):
        for l in range(length):
            #getpixel returns a tuple representing RGB values, so the channel index specifies which color to get
            intensities.append(image.getpixel((w, l))[channel_index])

    return intensities

def get_message(characters: int) -> str:
    message = input("Please enter your secret message. \n")

    while len(message) > characters:
        message = input("The message can only be " + str(characters) + " long!")

    return message

def prepend_header(message: str) -> str:
    """
    Consumes a message and returns the header of the message
    
    Args:
        message (str): An ASCII message to be encoded
    
    Returns:
        str: The header of the message
    """

    if not message:
        return '000'
    
    #returns a three digit integer
    return format(len(message), '03d') + message

def message_to_binary(message: str) -> str:
    """
    Consumes a message of ASCII characters and returns the binary 
    representation of the characters
    
    Args:
        message (str): A message of ASCII characters
        
    Returns:
        str: The binary value of the message
    """
    
    binary = ''

    for char in message:
        #Format with the parameter '08b' returns the ordinal value as a binary string with 8 digits
        binary = binary + format(ord(char), '08b')

    return binary

def new_color_value(intensity: int, hidden_bit: str) -> int:
    """
    Consumes two values: an integer representing the original Base 10 color intensity value 
    and a string containing the single bit that is to be hidden. It returns a new intensity
    value based on which kind of bit is to be hidden (an even or odd bit)
    
    Args:
        intensity (int): An integer representing the color intensity
        hidden_bit (str): Either a 0 or 1
        
    Returns:
        int: A new intensity value based on the hidden bit"""
    
    if hidden_bit == '1':
        if intensity % 2 == 0:
            intensity += 1
            return intensity
        return intensity
    
    if intensity % 2 == 0:
        return intensity
    return intensity - 1

def hide_bits(image: PIL_Image, binary: str) -> PIL_Image:
    """
    Consumes a Pillow Image and the binary string containing the bits that should be hidden in the 
    image and returns a Pillow Image with the hidden message.
    
    Args:
        image (PIL_Image): A Pillow image
        binary (str): The binary representation of the message to be encoded
        
    Returns:
        PIL_Image: A new Pillow image with the hidden bits encoded
    """

    width, length = image.size
    current_bit = 0

    for w in range(width):
        for l in range(length):
            red, green,blue = image.getpixel((w,l))
            #Checks if the current bit isn't going over the length of the message
            if (current_bit < len(binary)):
                image.putpixel((w,l), (red, new_color_value(green, binary[current_bit]), blue))
            current_bit += 1

    return image

def flip_horizontal(image: PIL_Image) -> PIL_Image:

    width, length = image.size

    for w in range(width):
        for l in range(length):
            red,green,blue = image.getpixel((w,l))
            if l < (length // 2):
                image.putpixel((w, length - l - 1), (red, green, blue))

    return image

def flip_vertical(image: PIL_Image) -> PIL_Image:

    width, length = image.size

    for w in range(width):
        for l in range(length):
            red,green,blue = image.getpixel((w,l))
            image.putpixel((width - w - 1, l), (red, green, blue))

    return image

@dataclass
class State:
    image: PIL_Image
    file_name: str = None
    display_message: str = None
    current_message: str = None
    pixel_data: list[int] = None

@route
def index(state: State) -> Page:
    raw_data = FileUpload("encoded_file", accept="image/png")

    return Page(state, ["Please select a 'png' file to get started!.", raw_data, Button("Display", display_image)])

@route
def display_image(state : State, encoded_file: bytes) -> Page:
    state.image = PIL_Image.open(io.BytesIO(encoded_file)).convert('RGB')
    
    return Page(state, ["Here is your image! Would you like to encode a message, or decode one from the image, or flip the image?", Image(state.image), LineBreak(),
                        Row(Button("Back", index), LineBreak(), Button("Decode message", decode), Button("Encode a message", encode), LineBreak(), 
                        Button("flip horizontal", flip_h), Button("flip_vertical", flip_v))])

@route
def encode(state: State) -> Page:
    return Page(state, [Image(state.image), "Please type the message you would like to encode below. ", TextBox("message", "Start typing to get started!"), 
                Button("Encode", encode_message)])

@route
def encode_message(state: State, message: str):
    state.current_message = message
    users_message = state.current_message 
    message_with_header = prepend_header(users_message)
    binary_string = message_to_binary(message_with_header)  # convert the full message to a binary string    
    state.image = hide_bits(state.image, binary_string) # encode the message into the image
    
    return Page(state, ["Would you like to save your file?", Button("Save", save_message), Button("Home Page", index)])

@route
def save_message(state: State):
    
    # save the updated image with a new file name
    new_file_name = "1_" + state.file_name  + ".png" # format of 1 + old filename (1 represents green channel)  
    
    return Page(state, ["Your file has been saved!", Download("download", new_file_name, state.image, "image/png") , "Would you like to encode enother message?", Button("Encode", encode), Button("Home Page", index)])

@route
def decode(state: State) -> Page:
    display_image = state.image
    state.pixel_data = get_color_values(display_image, 1)

    return Page(state, ["Your file has the message: ", get_encoded_message(state.pixel_data), Button("Return to home page", index)])

@route
def flip_h(state: State) -> Page:
    state.image = flip_horizontal(state.image)

    return Page(state, ["Your file has been flipped!", Image(state.image), Button("Return to home page", index)])

@route
def flip_v(state: State) -> Page:
    state.image = flip_vertical(state.image)

    return Page(state, ["Your file has been flipped!", Image(state.image), Button("Return to home page", index)])

set_site_information(
    author="edwinko@udel.edu",
    description= "A website that lets you encode and decode messages from an image",
    sources=["Google Gemini was used for help on getting an image's name and saving said image"],
    planning=["website_design.jpg"],
    links=["https://github.com/edwinko-alt/Steganography-Web-App"]
)
set_website_title("Steganography")
set_website_framed(False)

start_server(State(None, None, "Hello, and welcome to my steganography site! Would you like to upload an image?", None, []))