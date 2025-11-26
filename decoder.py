from PIL import Image as PIL_Image

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
