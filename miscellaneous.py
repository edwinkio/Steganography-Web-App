from PIL import Image as PIL_Image

def flip_horizontal(image: PIL_Image) -> PIL_Image:
    """1
    Consumes a Pillow Image and returns an image flipped horizontally
    
    Args:
        image (PIL_Image): A Pillow image
        
    Returns:
        PIL_Image: A new Pillow image that has been flipped horizontally
    """
    width, length = image.size

    for w in range(width):
        for l in range(length):
            red,green,blue = image.getpixel((w,l))

            #ensure that the program isn't reflecting more than half of the image
            if l < (length // 2):
                image.putpixel((w, length - l - 1), (red, green, blue))

    return image

def flip_vertical(image: PIL_Image) -> PIL_Image:
    """
    Consumes a Pillow Image and returns an image flipped vertically
    
    Args:
        image (PIL_Image): A Pillow image
        
    Returns:
        PIL_Image: A new Pillow image that has been flipped vertically
    """
    width, length = image.size

    for w in range(width):
        for l in range(length):
            red,green,blue = image.getpixel((w,l))
            image.putpixel((width - w - 1, l), (red, green, blue))

    return image