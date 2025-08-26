from PIL import Image
import numpy as np

#Defina aqui qual imagem sera cortada e onde os pontos serao salvos
image_input = "images/height_map/height_map.png"
output_path = "generate_data_set/generate_data_set/src"

def import_image(image_input):
    img = Image.open(image_input)
    
    return img

def get_shape(img):
    width, height = img.size
    
    return width, height

def grid_points(width, height, tile=256, stride=32, include_borders=True):
    # gera eixos x,y em passos = stride
    xs = list(range(0, max(1, width  - tile + 1), stride))
    ys = list(range(0, max(1, height - tile + 1), stride))

    # garante que o último patch encoste na borda direita/baixo
    if include_borders:
        last_x = max(0, width  - tile)
        last_y = max(0, height - tile)
        if xs[-1] != last_x:
            xs.append(last_x)
        if ys[-1] != last_y:
            ys.append(last_y)

    # grade cartesiana (ordenada, reprodutível)
    points = [(x, y) for y in ys for x in xs]
    return points

def save_points(points, output_path):
    
    np.savetxt(f"{output_path}/points.txt", points, fmt='%d', delimiter=',')
           
            
print("Importing image...")
img = import_image(image_input)

print("Getting shape of the image...")
width, height = get_shape(img)

print("Generating random points...")
points = grid_points(width,height)

print("Saving points to file...")
save_points(points, output_path)

    
