from dataclasses import dataclass
from drafter import *
from decoder import *
from encoder import *

set_site_information(
    author="edwinko@udel.edu",
    description= "A website that lets you encode and decode messages from an image",
    sources=["Google Gemini was used for help on getting an image's name and saving said image"],
    planning=["website_design.jpg"],
    links=["https://github.com/edwinko-alt/Steganography-Web-App"]
)
hide_debug_information()
set_website_title("Steganography")
set_website_framed(False)

@dataclass
class State:
    image: PIL_Image
    file_name: str
    display_message: str
    current_message: str
    encoded_image: list[int]

@route
def index(state: State) -> Page:
    raw_data = FileUpload("encoded_file", accept="image/png")
    state.file_name = raw_data.name

    return Page(state, ["Please select a 'png' file to get started!.", raw_data, Button("Display", display_image)])

@route
def display_image(state : State, encoded_file: bytes) -> Page:
    state.image = PIL_Image.open(io.BytesIO(encoded_file)).convert('RGB')
    
    return Page(state, ["Here is your image! Would you like to encode a message, or decode one from the image?", Image(state.image), 
                        Button("Back", index), Button("Decode message", decode), Button("Encode a message", encode)])

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
    state.image.save(new_file_name, "PNG") 
    
    return Page(state, ["Your file has been saved!", "Would you like to encode enother message?", Button("Encode", encode), Button("Home Page", index)])

@route
def decode(state: State) -> Page:
    display_image = state.image
    green = get_color_values(display_image, 1)

    return Page(state, ["Your file has the message: ", get_encoded_message(green), Button("Return to home page", index)])

hide_debug_information()

start_server(State(None, None, "Hello, and welcome to my steganography site! Would you like to upload an image?", None, []))
