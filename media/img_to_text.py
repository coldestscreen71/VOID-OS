import sys
from PIL import Image
import uuid
import time

from system.filesystem.data import add_data, get_data
from commands.extra import clear

from system.filesystem.file_control import save_fs, cwd, get_path, dict_info

from system.errorcontrol.error import er

ASCII_CHARS = " .:-=+*#%@"

def resize(image, new_width=80):
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio * 0.55)
    return image.resize((new_width, new_height))

def to_grayscale(image):
    return image.convert("L")

def pixel_to_ascii(image):
    pixels = image.getdata()
    chars = ""
    
    for pixel in pixels:
        index = pixel * (len(ASCII_CHARS)-1) // 255
        chars += ASCII_CHARS[index]
    
    return chars

def image_to_text(path):
    try:
        image = Image.open(path)
    except:
        er("cannot open image")
        return
    
    image = resize(image)
    image = to_grayscale(image)
    
    ascii_str = pixel_to_ascii(image)
    
    width = image.width
    ascii_img = "\n".join(
        ascii_str[i:i+width] for i in range(0, len(ascii_str), width)
    )
    
    return ascii_img

def img(*args):
    if len(args) != 2:
        print("usage: img <input_image's actual path in your system> <name>")
        return
    input_path = args[0]
    name = args[1]
    current = dict_info()
    
    if not current or current["type"] != "dir":
        er("not a directory")
        return
    
    if not name.endswith(".img"):
        name += ".img"
    
    if name in current["children"]:
        er("already exists")
        return
    
    ascii_data = image_to_text(input_path)
    
    if ascii_data is None:
        er("conversion failed")
        return
    
    loc = str(uuid.uuid4())
    
    current["children"][name] = {
        "type": "img",
        "size": len(ascii_data),
        "location": loc
    }
    
    add_data(loc, ascii_data)
    save_fs()
    
    print(f"image created: {name} in {get_path()}")

def view(name):
    current = dict_info()
    
    if not current or name not in current["children"]:
        er("file not found")
        return
    
    file = current["children"][name]
    
    if file["type"] != "img":
        er("not an image")
        return
    
    data = get_data(file["location"])
    
    print(data if data else "[empty image]")
