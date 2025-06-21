def _text_to_binary(text):
    return ''.join(format(ord(c), '08b') for c in text)

def _binary_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(c, 2)) for c in chars)

def encode_image(image, message):
    binary_msg = _text_to_binary(message) + '1111111111111110'
    img = image.convert('RGB')
    pixels = img.load()
    width, height = img.size
    index = 0

    for y in range(height):
        for x in range(width):
            if index >= len(binary_msg):
                break
            r, g, b = pixels[x, y]
            r = (r & ~1) | int(binary_msg[index])
            index += 1
            if index < len(binary_msg):
                g = (g & ~1) | int(binary_msg[index])
                index += 1
            if index < len(binary_msg):
                b = (b & ~1) | int(binary_msg[index])
                index += 1
            pixels[x, y] = (r, g, b)
        if index >= len(binary_msg):
            break

    return img

def decode_image(image):
    img = image.convert('RGB')
    pixels = img.load()
    width, height = img.size
    binary_msg = ""
    end_marker = '1111111111111110'

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            for value in (r, g, b):
                binary_msg += str(value & 1)
                if binary_msg.endswith(end_marker):
                    binary_msg = binary_msg[:-len(end_marker)]
                    return _binary_to_text(binary_msg)
    return ""
