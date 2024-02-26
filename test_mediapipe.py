import cv2
import numpy as np
import mediapipe as mp


mp_objectron = mp.solutions.objectron
mp_drawing = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

objectron = mp_objectron.Objectron(static_image_mode=False,
                            max_num_objects=2,
                            min_detection_confidence=0.4,
                            min_tracking_confidence=0.70,
                            model_name='Shoe')

# Read video stream and feed into the model
while cap.isOpened():
    success, image = cap.read()

    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = objectron.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.detected_objects:
        volume = []
        vactor = []
        for detected_object in results.detected_objects:

            # Draw landmarks and axis
            mp_drawing.draw_landmarks(image, detected_object.landmarks_2d, mp_objectron.BOX_CONNECTIONS)
            mp_drawing.draw_axis(image, detected_object.rotation, detected_object.translation)

            # Get direction vector
            direction_vector = detected_object.rotation[:, 2]
            vactor.append(direction_vector)

            # Calculate azimuthal angle
            azimuthal_angle = np.mod(np.arctan2(direction_vector[1], direction_vector[0]) * 180 / np.pi + 360, 360)


            # Plot azimuthal angle on image
            landmarks = detected_object.landmarks_2d.landmark
            left = min([landmark.x for landmark in landmarks])
            top = min([landmark.y for landmark in landmarks])
            right = max([landmark.x for landmark in landmarks])
            bottom = max([landmark.y for landmark in landmarks])
            font = cv2.FONT_HERSHEY_SIMPLEX
            pos = np.round(detected_object.translation, decimals=2)


            # Obtém os pontos extremos do objeto
            landmarks_3d = detected_object.landmarks_3d.landmark
            leftmost = min(landmarks_3d, key=lambda landmark: landmark.x)
            rightmost = max(landmarks_3d, key=lambda landmark: landmark.x)
            topmost = min(landmarks_3d, key=lambda landmark: landmark.y)
            bottommost = max(landmarks_3d, key=lambda landmark: landmark.y)
            nearmost = min(landmarks_3d, key=lambda landmark: landmark.z)
            farmost = max(landmarks_3d, key=lambda landmark: landmark.z)

            # Calcula a largura, comprimento e altura
            width = rightmost.x - leftmost.x
            length = farmost.z - nearmost.z
            height = bottommost.y - topmost.y

            # Calcula o volume
            volume.append(width * length * height*1000)

            pos_foto = (int(left * image.shape[1]), int(top * image.shape[0]) - 10)

            if azimuthal_angle <= 200 and azimuthal_angle >=170:
                cv2.putText(image, f"{azimuthal_angle:.1f}  ,  {pos[0]}  ,  {volume[-1]:.1f}", pos_foto, font, 0.5, (0, 128, 0), 2, cv2.LINE_AA)

            elif azimuthal_angle >= 200:
                cv2.putText(image, f"{azimuthal_angle:.1f}  ,  {pos[0]}  ,  {volume[-1]:.1f}", pos_foto, font, 0.5, (0, 0, 255), 2, cv2.LINE_AA)

            elif azimuthal_angle <= 170:
                cv2.putText(image, f"{azimuthal_angle:.1f}  ,  {pos[0]}  ,  {volume[-1]:.1f}", pos_foto, font, 0.5, (0, 0, 255), 2, cv2.LINE_AA)


        if len(results.detected_objects) >= 2:
            for i in range(len(results.detected_objects)):
                for j in range(i + 1, len(results.detected_objects)):
                    obj1 = results.detected_objects[i]
                    obj2 = results.detected_objects[j]

                    # Get direction vector of obj1
                    direction_vector = obj1.rotation[:, 2]

                    # Calculate azimuthal angle of obj1
                    azimuthal_angle = np.mod(np.arctan2(direction_vector[1], direction_vector[0]) * 180 / np.pi + 360, 360)

                    # Get translation vector of obj2
                    translation_vector = obj2.translation

                    translation_vector[2] = volume[0] - volume[1]

                    # Check if obj1 is facing obj2
                    dot_product = np.dot(direction_vector, translation_vector)
                    angle = np.arccos(dot_product / (np.linalg.norm(direction_vector) * np.linalg.norm(translation_vector))) * 180 / np.pi
                    if angle < 30:
                        print(f"Object {i} is facing object {j}, {translation_vector[2]}")

                    point_vector = obj1.translation - obj2.translation
                    direction_vector =obj1.rotation[:, 2]
                    dot_product = np.dot(direction_vector, point_vector)
                    magnitude_direction_vector = np.linalg.norm(direction_vector)
                    magnitude_point_vector = np.linalg.norm(point_vector)
                    angle = np.arccos(dot_product / (magnitude_direction_vector * magnitude_point_vector)) * 180 / np.pi
                    if angle < 30:
                        print(f"Object {i} is facing object {j}, {translation_vector[2]}")




    cv2.imshow('MediaPipe Objectron', image)


    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()