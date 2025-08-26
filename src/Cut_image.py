from PIL import Image
import numpy as np
from tqdm import tqdm

output_path = "data-set/Hm_to_texture"


def import_image(image_input):
    img = Image.open(image_input)
    
    return img

def import_points(points_file):
    points = np.loadtxt(points_file, delimiter=',', dtype=int)
    
    list_of_points = [tuple(point) for point in points]
    
    return list_of_points


def cut_image(img, points, type):

    for i, (x, y) in enumerate(tqdm(points, desc=f"Cutting images {type} in pixels : ")):

        box = (x, y, x + 256, y + 256)
        
        cut_img = img.crop(box)

        cut_img.save(f"{output_path}/{type}/cut_image_{i}.png")


print("Importando Pontos para a textura")
texture_points = import_points("generate_data_set/generate_data_set/src/points.txt")
        
print("Importando textura")
texture = import_image("images/texture/tx_cortado.png")

print("Importando textura")
height_map = import_image("images/height_map/hm_cortado.png")

print("Cortando textura em 256 pixels")
cut_image(texture, texture_points, "texture")

print("Cortando height_map em 256 pixels")
cut_image(height_map, texture_points, "height_map")

