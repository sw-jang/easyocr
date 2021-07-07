from dictionary import *

import argparse
import easyocr
import numpy as np
import random
from PIL import ImageFont, ImageDraw, Image
import pyrealsense2 as rs
import cv2
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

# random colors
np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(255, 3),dtype="uint8")
font = ImageFont.truetype('fonts/HMKMRHD.TTF', 20)

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--width', type=int, default=640, help='width of output frame in pixels i.e. 480, 640, ...')
    parser.add_argument('--height', type=int, default=480, help='height of output frame in pixels i. e. 480, 640, ...')
    parser.add_argument('--frame', type=int, default=30, help='fps of output frame')
    parser.add_argument('--device', type=str, default='gpu', help='cpu or gpu')
    opt = parser.parse_args()
    return opt

if __name__ == '__main__':
    opt = parse_opt()

    # set easy ocr
    if opt.device == 'cpu':
        reader = easyocr.Reader(['ko'], gpu=False)
    else:
        reader = easyocr.Reader(['ko'], gpu=True)

    # set realsense camera pipeline
    config = rs.config()
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, opt.frame)

    # start realsense camera pipeline
    pipe = rs.pipeline()
    pipe.start(config)

    try:
        while True:
            # get color frame
            frames = pipe.wait_for_frames()
            frame = np.array(frames.get_color_frame().get_data())
            frame = cv2.resize(frame, (opt.width, opt.height))

            # PILLOW used to print korean
            pil = Image.fromarray(frame)
            draw = ImageDraw.Draw(pil)

            # get all texts on scene
            results = reader.readtext(frame)

            for (bbox, text, prob) in results:
                # if text in target words
                if check_dic(text):
                    # bbox computation
                    (tl, tr, br, bl) = bbox
                    tl = (int(tl[0]), int(tl[1]))
                    tr = (int(tr[0]), int(tr[1]))
                    bl = (int(bl[0]), int(bl[1]))
                    br = (int(br[0]), int(br[1]))

                    # get random color
                    color_idx = random.randint(0,254)
                    color = [int(c) for c in COLORS[color_idx]]

                    # draw and print text read
                    draw.rectangle((tl, br), outline=tuple(color), width=2)
                    draw.text((tl[0], tl[1]-30), text, fill=tuple(color), font = font)
                    a, b, c = get_summary(text)
                    print(a, b, c)
                    frame = np.array(pil)
            # show result image
            cv2.imshow('test', frame)
            # if q break from loop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break   
    finally:
        pipe.stop()