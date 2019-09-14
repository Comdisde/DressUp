import numpy as np
import matplotlib.pyplot as plt
import cv2
from functools import reduce
def apply_mask(img, mask, color, alpha=0.5):
    """Apply the given mask to the image.
    """
    image=img.copy()
    for c in range(3):
        image[:, :, c] = np.where(mask == 1,
                                  image[:, :, c] *
                                  (1 - alpha) + alpha * color[c] * 255,
                                  image[:, :, c])
    return image

def show_out(img,model):
    img_val=img.copy()
    img_val=np.array([cv2.resize(img_val,(512,832))])
    
    size=(512,832) 
    colors=[(.08,.1,0),(0,.1,.06)]
    colors_gen=iter(colors)
    pred=model.predict(img_val).round()
    img_masked=reduce(lambda img,mask: apply_mask(img,mask,next(colors_gen),alpha=.02), [img_val[0],pred[...,1][0],pred[...,2][0]] )
    img_val=cv2.resize(img_val[0],size)
    img_masked=cv2.resize(img_masked,size)
    fig,(ax1,ax2,ax3)=plt.subplots(1,3,figsize=(20,20))
    ax1.axis("off")
    ax2.axis("off")
    ax3.axis("off")
    ax1.imshow(img_val)
    ax2.imshow(img_masked)
    ax3.imshow(cv2.resize(pred[0][...,[1,2]].sum(axis=2),size),cmap="PuBu")
