from PIL import Image
import numpy as np
from tqdm import tqdm

output_path = "./output/Mina_JAN_2025"


def import_image(image_input):
    img = Image.open(image_input)
    
    return img

def import_points(points_file):
    points = np.loadtxt(points_file, delimiter=',', dtype=int)
    
    list_of_points = [tuple(point) for point in points]
    
    return list_of_points


def cut_image(img, points, size, type):

    for i, (x, y) in enumerate(tqdm(points, desc=f"Cutting images in {size} pixels : ")):

        box = (x, y, x + size, y + size)
        
        cut_img = img.crop(box)

        cut_img.save(f"{output_path}/{size}x{size}/{type}/cut_image_{i}.png")


print("Importando Pontos para a textura")
texture_points = import_points("./output/Mina_JAN_2025/texture_points.txt")
        
print("Importando textura")
texture = import_image("./input/Textura.png")

print("Cortando textura em 32 pixels")
cut_image(texture, texture_points, 32 , "texture")

