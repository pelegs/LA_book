from subprocess import DEVNULL, STDOUT, run

import numpy as np
from tqdm import tqdm


def rotate(vec, th):
    c, s = np.cos(th), np.sin(th)
    R = np.array([[c, -s], [s, c]])
    return np.dot(R, vec)


a_vec = np.array([5, 2])
b_vec = np.array([3, 0])

num_frames = 60
b_angles = np.linspace(np.pi / 6, np.pi / 2, num_frames, endpoint=True)
b_vec_rotated = np.zeros(2)

pbar = tqdm(b_angles, desc="Rendering frames")
for frame, th in enumerate(pbar):
    b_vec_rotated = rotate(b_vec, th)
    pdflatex = rf"pdflatex '\def\ax{{{a_vec[0]}}} \def\ay{{{a_vec[1]}}} \def\bx{{{b_vec_rotated[0]}}} \def\by{{{b_vec_rotated[1]}}} \input{{trans}}'"
    convert = rf"magick -density 300 trans.pdf -alpha remove -background white -resize 75% trans_frame{frame:03d}.png"
    run(pdflatex, shell=True, stdout=DEVNULL, stderr=STDOUT)
    run(convert, shell=True, stdout=DEVNULL, stderr=STDOUT)

a_ys = np.linspace(2, -2, num_frames)
pbar = tqdm(a_ys, desc="Rendering frames")
for frame, y_val in enumerate(pbar, start=num_frames):
    pdflatex = rf"pdflatex '\def\ax{{{a_vec[0]}}} \def\ay{{{y_val}}} \def\bx{{{b_vec_rotated[0]}}} \def\by{{{b_vec_rotated[1]}}} \input{{trans}}'"
    convert = rf"magick -density 300 trans.pdf -alpha remove -background white -resize 75% trans_frame{frame:03d}.png"
    run(pdflatex, shell=True, stdout=DEVNULL, stderr=STDOUT)
    run(convert, shell=True, stdout=DEVNULL, stderr=STDOUT)

mv = "rm frames/*.png; mv *.png frames"
run(mv, shell=True, stdout=DEVNULL, stderr=STDOUT)

ffmpeg = "yes | ffmpeg -framerate 60 -i frames/trans_frame%03d.png -vcodec libx264 -crf 22 test_video.mp4"
run(ffmpeg, shell=True)
