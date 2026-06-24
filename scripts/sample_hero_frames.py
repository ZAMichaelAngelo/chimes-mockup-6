# scripts/sample_hero_frames.py
import cv2
import os

SRC = r"C:\Users\micha\OneDrive\Desktop\Chimes Work\Source Assets\Must Use Content\Top body video.mp4"
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "_frame_candidates")

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    cap = cv2.VideoCapture(SRC)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    print(f"Total frames: {total}, fps: {fps:.2f}, duration: {total/fps:.1f}s")
    for pct in [0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95]:
        frame_no = int(total * pct)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
        ok, frame = cap.read()
        if not ok:
            print(f"FAILED at {pct}")
            continue
        out_path = os.path.join(OUT_DIR, f"candidate_{int(pct*100)}pct.jpg")
        cv2.imwrite(out_path, frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        print(f"Saved {out_path} (frame {frame_no}, {frame_no/fps:.1f}s)")

if __name__ == "__main__":
    main()
