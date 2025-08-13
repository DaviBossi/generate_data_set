import cv2
import numpy as np

# Caminhos dos arquivos
input_path = "./input/height_map.png"         # Substitua pelo seu heightmap
output_path = "slope_map.png"

# Carrega o heightmap (16 bits preferencialmente)
heightmap = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)

if heightmap is None:
    raise FileNotFoundError("Arquivo não encontrado.")

# Converte para float32 para cálculos
heightmap = heightmap.astype(np.float32)

# Derivadas de 1ª ordem
dx = cv2.Sobel(heightmap, cv2.CV_32F, 1, 0, ksize=3)
dy = cv2.Sobel(heightmap, cv2.CV_32F, 0, 1, ksize=3)

# Cálculo da inclinação (hipotenusa do gradiente)
slope = np.sqrt(dx**2 + dy**2)

# (Opcional) Conversão para graus de inclinação
# cell_size = 1  # metros por pixel se conhecido
# slope_deg = np.arctan(slope / cell_size) * (180 / np.pi)

# Normaliza para imagem 8-bit
slope_norm = cv2.normalize(slope, None, 0, 255, cv2.NORM_MINMAX)
slope_map = slope_norm.astype(np.uint8)

# Salva resultado
cv2.imwrite(output_path, slope_map)
print("Mapa de slope salvo como:", output_path)
