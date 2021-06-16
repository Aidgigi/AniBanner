from PIL import Image
import os, sys

def to_jpg(img: Image) -> Image:
    if img.mode != 'RGB': return img.convert('RGB')
    else: return img

def normalize(img: Image, final: float) -> Image:
    size: int = img.size
    ratio: float = float(final) / max(size)

    #new_size: tuple = tuple([int(x*ratio) for x in size])
    new_size = (224, 224)
    img = img.resize(new_size, Image.ANTIALIAS)

    return to_jpg(img)

def bulk_process(root_path: str, output_path: str):
    files = os.listdir(root_path)

    number = 1

    for file in files:
        if file.endswith(".jpg") or file.endswith(".png"):
            print(f"Processing: {file}")
            try:

                img = normalize(Image.open(f"{root_path}/{file}"), 512)

                img.save(f"{output_path}/{number}.jpg", 'JPEG', quality = 90)
                    
                number += 1
            
            except Exception as e:
                print(e)

        else:
            print("Not an image")

bulk_process("./neg/images", "./set/negative")