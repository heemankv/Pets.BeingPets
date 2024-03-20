import os
os.environ["IMAGEIO_FFMPEG_EXE"] = "/opt/homebrew/Cellar/ffmpeg/6.1.1_5/bin/ffmpeg"

import cv2
import moviepy.editor as mpy
import numpy as np

# Step 1: Detect the dimensions and location of the red rectangle
image_path = "image.png"
video_path = "video.mp4"

image = cv2.imread(image_path)

# Convert the image to HSV color space
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define the range for red color in HSV
lower_red = (0, 120, 70)
upper_red = (10, 255, 255)

# Threshold the HSV image to get only red colors
mask = cv2.inRange(hsv, lower_red, upper_red)

# Find contours in the mask
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Find the largest contour which represents the red rectangle
largest_contour = max(contours, key=cv2.contourArea)

# Calculate the bounding rectangle for the largest contour
x, y, w, h = cv2.boundingRect(largest_contour)

# Print the dimensions and location of the red rectangle
print(f"Red rectangle dimensions: {w}x{h}")
print(f"Red rectangle position: x={x}, y={y}")
video = mpy.VideoFileClip(video_path)

# Now that we know where in the image the red rectangle is, we can overlay the video on it.


# convert the image to a video file of same duration as the video
imageClip = mpy.ImageClip(image_path, duration=video.duration)

final =  mpy.CompositeVideoClip([
  # image 
  # main clip

  imageClip, 
  # the video should have size (w, h)
  video.set_position((x, y)).resize((w, h))
])

print(final.size)
print(video.size)
print(imageClip.size)

# now write file in a format that is compatible with most video players, like .mp4
final.write_videofile("video-final.mp4", fps=video.fps, codec="libx264", audio_codec="aac", temp_audiofile='temp-audio.m4a', remove_temp=True)