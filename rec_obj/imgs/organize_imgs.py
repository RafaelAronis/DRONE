# import
import os

# Paths
paths = ["positive_imgs", "negative_imgs"]

# Interar sobre os paths
for path in paths:

    arquivos = os.listdir(path) # Lista os arquivos na pasta

    for i, arquivo in enumerate(arquivos, start=1): # Itera sobre os arquivos

        novo_nome = f"{i}.jpg" # Novo nome do arquivo
        old_path = os.path.join(path, arquivo)
        new_path = os.path.join(path, novo_nome)

        if not os.path.exists(new_path):
            os.rename(old_path, new_path) # Rename file
