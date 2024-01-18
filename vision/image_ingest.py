import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from PIL import Image
from PIL.ExifTags import TAGS

if True:
    img = cv2.imread("vision\\20170311_172915.jpg", 0)
    

if False:
    img = cv2.imread("vision\\20170311_172915.jpg", 0)

    scale_perc = 0.15
    height = int(img.shape[0] * scale_perc)
    width = int(img.shape[1] * scale_perc)
    new_dim = (width, height)

    img = cv2.resize(img, new_dim, interpolation=cv2.INTER_AREA)

    #line_grad = pd.Series(img[100, 0:448]).plot(ylim=(-2, 257))
    #plt.show()

    print(img.shape)

    #img = img[0:-1:4, 0:-1:4]
    img = img[-1:0:-1, :]
    print(img.shape)

    cv2.imshow("frame", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if False:
    pixels = np.zeros((200, 200))
    pixels[65:75, 140:160] = 0.5

    while True:
        cv2.imshow("frame", pixels)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if False:
    camera = cv2.VideoCapture("vision\\test_video.mp4")
    ret, pixels = camera.read()
    while True:
        cv2.imshow("frame", pixels)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()

if False:
    camera = cv2.VideoCapture(0)

    frame_width = int(camera.get(3))
    frame_height = int(camera.get(4))
    fps = 30

    video_writer = cv2.VideoWriter(
        "vision\\test_video.mp4",
        cv2.VideoWriter_fourcc("m", "p", "4", "v"),
        fps,
        (frame_width, frame_height)
    )

    for _ in range(90):
        ret, pixels = camera.read()
        if ret:
            video_writer.write(pixels)
            cv2.waitKey(1)
        else:
            break
    
    camera.release()
    video_writer.release()

    cv2.destroyAllWindows()

if False:
    camera = cv2.VideoCapture(0)

    while True:
        ret, pixels = camera.read()
        cv2.imshow("frame", pixels)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()

    #print(frame)

if False:
    img = Image.open("vision\\20170311_172915.jpg")

    metadata = img.getexif()

    # TODO: reshape to tensor
    pixels = np.array(img.getdata())
    print(pixels)

if False:
    for tag_id in metadata:
        tag = TAGS.get(tag_id, tag_id)
        contents = metadata.get(tag_id)

        if isinstance(contents, bytes):
            contents = contents.decode()
        
        print(f"{tag}: {contents}")
        print("----------------------")
