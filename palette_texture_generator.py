import numpy as np
from PIL import Image
import os
import sys

def gen_from_name(name):
    overlay = "source_textures/"+name+"_overlay.png"
    paletted = "source_textures/"+name+"_paletted.png"
    overlay_img = Image.open(overlay).convert('RGBA')
    paletted_img = Image.open(paletted).convert('RGBA')
    if not (overlay_img.size == paletted_img.size):
        raise Exception("Source images are different sizes")
    o_arr = np.array(overlay_img)
    p_arr = np.array(paletted_img)
    for background in os.listdir('background_textures'):
        if background.endswith('.png'):
            background_img = Image.open("background_textures/"+background).convert('RGBA')
            if not background_img.size == paletted_img.size:
                raise Exception("Background image " + background + " is the wrong size")
            b_arr = np.array(background_img)
            palette = []
            for i in range(16):
                for j in range(16):
                    if b_arr[i,j,3] == 255:
                        if not b_arr[i,j].tolist() in palette:
                            palette.append(b_arr[i,j].tolist())
            palette.sort(key=lambda x:sum(x))
            out_arr = np.zeros((16,16,4),dtype=np.uint8)
            for i in range(16):
                for j in range(16):
                    out = b_arr[i,j].astype(np.float64)
                    if (p_arr[i,j,3] == 255):
                        if len(palette) >= 2:
                            out[0:3] = palette[round(p_arr[i,j,0]/255.0*(len(palette)-1))][0:3]
                    out[0:3] = out[0:3] * (1-o_arr[i,j,3]/255.0) + o_arr[i,j,0:3].astype(np.float64) * o_arr[i,j,3]/255.0
                    out[3] = 255
                    out_arr[i,j] = out.astype(np.uint8)
            out_file = "out_textures/"+background[0:-4]+"_"+name+".png"
            out_img = Image.fromarray(out_arr,mode='RGBA')
            out_img.save(out_file)

if __name__ == "__main__":
    arg = sys.argv[1]
    if arg=="--all":
        files = [i[0:-12] for i in os.listdir("source_textures") if i.endswith("_overlay.png")]
        for f in files:
            if os.path.exists("source_textures/"+f+"_paletted.png"):
                gen_from_name(f)
    else:
        gen_from_name(sys.argv[1])