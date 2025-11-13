#from ultralytics import YOLO
#model = YOLO("yolo11n.pt")
#model.train(data="./American Sign Language Letters.v1i.yolov11/data.yaml", epochs=10, imgsz=640)

from ultralytics import YOLO
import time
import cv2

model = YOLO("runs/detect/train2/weights/best.pt")
results = model.predict(source=0, stream=True)

letras_reconocidas = []
letras_no_reconocidas = []
ultimo_tiempo = 0
intervalo = 2

for result in results:
    tiempo_actual = time.time()
    if tiempo_actual - ultimo_tiempo >= intervalo:
        if result.boxes:
            letra = result.names[int(result.boxes[0].cls)]
            conf = float(result.boxes[0].conf)
            if conf > 0.5:
                letras_reconocidas.append(letra)
            else:
                letras_no_reconocidas.append(letra)
        ultimo_tiempo = tiempo_actual
    ventana = result.orig_img.copy()
    if len(letras_reconocidas) > 10:
        letras_reconocidas = []
    if len(letras_no_reconocidas) > 10:
        letras_no_reconocidas = []
    cv2.putText(ventana, f"Reconocidas: {''.join(letras_reconocidas)}",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(ventana, f"No reconocidas: {''.join(letras_no_reconocidas)}",
                (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.imshow("Resultado", ventana)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()