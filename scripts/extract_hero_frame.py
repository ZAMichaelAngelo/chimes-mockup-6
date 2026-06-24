# scripts/extract_hero_frame.py
import cv2
import os
import sys

SRC = r"C:\Users\micha\OneDrive\Desktop\Chimes Work\Source Assets\Must Use Content\Top body video.mp4"
OUT = os.path.join(os.path.dirname(__file__), "..", "Cinematic Images", "hero-still.jpg")

# Set to the percentage chosen in Step 3 after viewing the 10 candidates.
CHOSEN_PCT = 0.45  # chosen after visual review: best balance of cab, full chassis, and lit boom/hook

def main():
    cap = cv2.VideoCapture(SRC)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_no = int(total * CHOSEN_PCT)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
    ok, frame = cap.read()
    if not ok:
        sys.exit(f"Failed to read frame {frame_no}")
    cv2.imwrite(OUT, frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
    print(f"Saved {OUT} from frame {frame_no} ({CHOSEN_PCT*100:.0f}%)")

if __name__ == "__main__":
    main()
