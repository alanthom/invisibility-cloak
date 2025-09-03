import cv2
import numpy as np

# Input and output video paths
input_path = 'input.mov'
output_path = 'output.mov'


# Open the input video
cap = cv2.VideoCapture(input_path)
if not cap.isOpened():
    print(f'Error: Cannot open {input_path}')
    exit()


# Get video properties
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
if fps == 0:
    fps = 25  # Default to 25 if FPS is not detected

# Output video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
if not out.isOpened():
    print(f'Error: Cannot open video writer for {output_path}')
    cap.release()
    exit()


# Capture background (first 60 frames)
background = None
frame_count = 0
for i in range(60):
    ret, frame = cap.read()
    if not ret:
        print('Warning: Not enough frames for background capture.')
        break
    background = frame
    frame_count += 1
if background is None:
    print('Error: No background frame captured.')
    cap.release()
    out.release()
    exit()
background = np.flip(background, axis=1)  # Flip for consistency

 # Moderately expanded maroon color range in HSV
lower_maroon = np.array([145, 60, 20])
upper_maroon = np.array([179, 255, 255])



frames_written = 0
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
if total_frames == 0:
    total_frames = 1  # Avoid division by zero
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame = np.flip(frame, axis=1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create mask for maroon color
    mask = cv2.inRange(hsv, lower_maroon, upper_maroon)
    # Extra smoothing for cleaner mask
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((9,9), np.uint8))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((13,13), np.uint8))
    mask = cv2.GaussianBlur(mask, (15,15), 0)

    # Refine mask
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))
    mask = cv2.dilate(mask, np.ones((3,3), np.uint8), iterations=1)
    mask_inv = cv2.bitwise_not(mask)

    # Segment out the cloak and replace with background
    res1 = cv2.bitwise_and(background, background, mask=mask)
    res2 = cv2.bitwise_and(frame, frame, mask=mask_inv)
    final = cv2.addWeighted(res1, 1, res2, 1, 0)

    out.write(final)
    frames_written += 1
    if frames_written % 50 == 0 or frames_written == total_frames:
        percent = (frames_written / total_frames) * 100
        print(f'Processed {frames_written}/{total_frames} frames ({percent:.1f}%)')

if frames_written == 0:
    print('Warning: No frames were written to the output video. Check your input file and color range.')


cap.release()
out.release()
print(f'Output saved as {output_path}. Frames written: {frames_written}')
