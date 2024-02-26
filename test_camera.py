# Import
import cv2

# Cria o detector de obj
# Cascade = cv2.CascadeClassifier("cascade/cascade2/cascade.xml")
# Cascade = cv2.CascadeClassifier("cascade/cascade1/cascade.xml")
Cascade = cv2.CascadeClassifier("cascade/norg/haarcascade_frontalface_default.xml")

# Captura de vídeo da câmera
video_capture = cv2.VideoCapture(0)

while True:
    # Lê o frame da câmera
    ret, frame = video_capture.read()

    # Converte para escala de cinza
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detecta obj no frame
    obj = Cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Para cada face detectada
    for (x, y, w, h) in obj:
        # Desenha um retângulo ao redor da face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Mostra o frame na tela
    cv2.imshow('Video', frame)

    # Espera por um evento de teclado
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera os recursos
video_capture.release()
cv2.destroyAllWindows()
