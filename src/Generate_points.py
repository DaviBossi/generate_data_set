from PIL import Image
import numpy as np

#Defina aqui qual imagem sera cortada e onde os pontos serao salvos
image_input = "./input/JAN_2025/height_map.png"
output_path = "./output/Mina_JAN_2025"

def import_image(image_input):
    img = Image.open(image_input)
    
    return img

def get_shape(img):
    width, height = img.size
    
    return width, height

def generate_random_points(width, height):

    points = set()
    x = y = 0
    
    while y < height:
        while x < width:
            points.add((x,y))
            x += 2
        x = 0
        y += 2
            
    return np.array(list(points))

def save_points(points, output_path):
    
    np.savetxt(f"{output_path}/points.txt", points, fmt='%d', delimiter=',')
           
            
print("Importing image...")
img = import_image(image_input)

print("Getting shape of the image...")
width, height = get_shape(img)

print("Generating random points...")
points = generate_random_points(width, height)

print("Saving points to file...")
save_points(points, output_path)

    
