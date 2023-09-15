Making a video of still images (after installing ffmpeg and adding it to path)

ffmpeg -r 6 -i "images/frame_%04d.png" -c:v libx264 -pix_fmt yuv420p tuuli_10min.mp4
