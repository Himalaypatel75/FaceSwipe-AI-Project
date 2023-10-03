import numpy
import os
import glob
import cv2
import matplotlib.pyplot as plt
import insightface
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image

if __name__ == '__main__':
    app = FaceAnalysis(name='buffalo_l')
    app.prepare(ctx_id=0, det_size=(640, 640))
    swapper = insightface.model_zoo.get_model('inswapper_128.onnx', download=True, download_zip=True)


    # img = ins_get_image('t1')
    img = cv2.imread('origin.jpeg')
    # img = 'origin.jpeg'
    faces = app.get(img)
    faces = sorted(faces, key = lambda x : x.bbox[0])
    # assert len(faces)==6
    
    
    simg = cv2.imread('origin.jpeg')
    sfaces = app.get(simg)
    source_face = sfaces[0]
    
    res = img.copy()
    for face in faces:
        res = swapper.get(res, face, source_face, paste_back=True)
        
    cv2.imwrite("./t1_swapped.jpg", res)
    res = []
    for face in faces:
        _img, _ = swapper.get(img, face, source_face, paste_back=False)
        res.append(_img)
    res = numpy.concatenate(res, axis=1)
    cv2.imwrite("./t1_swapped2.jpg", res)