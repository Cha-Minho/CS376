import cv2
import time
import os

fps = 30
time_per_frame_video = 1 / fps
l_time = time.perf_counter()

if "Data" not in os.listdir(os.getcwd()):
    os.makedirs("Data")

surfix = f"Data"
if "concentrating" not in os.listdir(surfix):
    os.makedirs(f"{surfix}/concentrating")
if "unconcentrating" not in os.listdir(surfix):
    os.makedirs(f"{surfix}/unconcentrating")

CAMERA_ID = 0
FRAME_WIDTH = 640
FRAME_HEIGTH = 480

capture = cv2.VideoCapture(CAMERA_ID)
if capture.isOpened() == False: 
    print(f'Can\'t open the Camera({CAMERA_ID})')
    exit()

capture.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGTH)

concentrating = True
capture_duration = 3
prev_time = time.time()
conc_list = os.listdir(f"{surfix}/concentrating")
unconc_list = os.listdir(f"{surfix}/unconcentrating")
print(len(conc_list))
print(len(unconc_list))
concentrate_frame_id = len(conc_list)
first_conc_f_id = concentrate_frame_id
unconcentrate_frame_id = len(unconc_list)
first_unconc_f_id = unconcentrate_frame_id
concentrate_string = "Concentrating"

while True:
    if time.time() - prev_time >= capture_duration:
        prev_time = time.time()
        ret, frame = capture.read()
        frame = cv2.flip(frame, 1)
        if concentrating:
            cv2.imwrite(f"{surfix}/concentrating/{concentrate_frame_id}.jpg", frame)
            concentrate_frame_id += 1
        else:
            cv2.imwrite(f"{surfix}/unconcentrating/{unconcentrate_frame_id}.jpg", frame)
            unconcentrate_frame_id += 1

    k = cv2.waitKey(1) & 0xFF
    if k == ord("q"):
        break
    if k in [ord("a")]:
        concentrating = False
        concentrate_string = "Unconcentrating"
    if not concentrating and k == ord("o"):
        concentrating = True
        concentrate_string = "Concentrating"

    ret, frame = capture.read()
    frame =cv2.flip(frame, 1)
    cv2.rectangle(frame, (0, 0, 640, 80), (255, 255, 255), -1)
    cv2.putText(frame, concentrate_string, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0))
    cv2.putText(frame, "Quit: Q, Unconcentrate: A, Concentrate: O", (10, 50), cv2.FONT_ITALIC, 0.5, (0, 0, 0))
    cv2.putText(frame, f"Concentration Frame: {concentrate_frame_id - first_conc_f_id}, Unconcentration Frame: {unconcentrate_frame_id - first_unconc_f_id}", (10, 70), cv2.FONT_ITALIC, 0.5, (0, 0, 0))
    cv2.imshow("VideoFrame", frame)

capture.release()
cv2.destroyAllWindows()
