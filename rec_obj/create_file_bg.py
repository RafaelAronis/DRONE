import os

# Diretório contendo as imagens de fundo
bg_dir = 'imgs/negative_imgs'

# Nome do arquivo de saída
output_file = 'bg.txt'

# Lista para armazenar os caminhos das imagens de fundo
bg_paths = []

# Loop através dos arquivos do diretório
for file in os.listdir(bg_dir):
    if file.endswith('.jpg') or file.endswith('.png'):  # Verificar extensões de arquivo desejadas
        bg_path = os.path.join(bg_dir, file)  # Obter o caminho completo do arquivo
        bg_paths.append('./' + bg_path.replace('\\', '/'))  # Adicionar o caminho à lista de caminhos de imagens de fundo

# Escrever os caminhos das imagens de fundo no arquivo de saída
with open(output_file, 'w') as f:
    for bg_path in bg_paths:
        f.write(bg_path + '\n')

print(f'Arquivo {output_file} criado com sucesso!')
