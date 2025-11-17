from PIL import Image as PIL_Image

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
