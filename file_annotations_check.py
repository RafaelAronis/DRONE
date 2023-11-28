import cv2
import pandas as pd

# Lê o arquivo annotations.txt em um DataFrame
df = pd.read_csv('annotations.txt', delimiter=' ', header=None, names=['filename', 'x', 'y', 'w', 'h'])

# Itera sobre as linhas do DataFrame e desenha os retângulos nas imagens
for i, row in df.iterrows():
    # Lê a imagem
    img = cv2.imread(row.name)

    # Converte as coordenadas para inteiros
    x, y, w, h = int(row['x']), int(row['y']), int(row['w']), int(row['h'])

    # Desenha o retângulo na imagem
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)

    # Exibe a imagem com o retângulo
    cv2.imshow('image', img)
    cv2.waitKey(0)

# Fecha a janela de exibição
cv2.destroyAllWindows()
