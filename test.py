import cv2
import numpy as np

# Carrega os parâmetros da câmera
calib_data = np.load('calibration/calibration.npz')
K = calib_data['K']
dist = calib_data['dist']

# Tamanho do padrão do xadrez
pattern_size = (9, 6)

# Tamanho do quadrado em milímetros
square_size = 28.0

# Cria a matriz de pontos do objeto
obj_points = np.zeros((np.prod(pattern_size), 3), dtype=np.float32)
obj_points[:, :2] = np.indices(pattern_size).T.reshape(-1, 2)
obj_points *= square_size

# Define os critérios para a otimização dos pontos de canto
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Abre a câmera
cap = cv2.VideoCapture(0)

while True:
    # Captura um frame da câmera
    ret, frame = cap.read()

    # Converte para escala de cinza
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Encontra os pontos de canto do tabuleiro de xadrez
    ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)

    if ret:
        # Refina os pontos de canto
        corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

        # Projeta os pontos do objeto na imagem
        _, rvecs, tvecs, inliers = cv2.solvePnPRansac(obj_points, corners, K, dist)
        img_points, _ = cv2.projectPoints(obj_points, rvecs, tvecs, K, dist)
        img_points = np.int32(img_points).reshape(-1, 2)

        # Desenha as linhas entre os pontos
        frame = cv2.drawChessboardCorners(frame, pattern_size, corners, ret)

        # Estima a distância em relação ao objeto
        z = tvecs[2]
        distance = np.linalg.norm(z)

        # Exibe a distância no frame
        cv2.putText(frame, 'Distance: {:.2f} cm'.format(distance), (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Exibe o frame na janela
    cv2.imshow('frame', frame)

    # Sai do loop se a tecla 'q' for pressionada
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera a câmera e fecha a janela
cap.release()
cv2.destroyAllWindows()
