import time
import cv2
import numpy as np
import mss
import win32gui
import random
import onnxruntime as ort 

def find_window(title_substring):
    def callback(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):
            window_title = win32gui.GetWindowText(hwnd)
            if title_substring.lower() in window_title.lower():
                extra.append(hwnd)
    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds[0] if hwnds else None

def get_window_rect(hwnd):
    rect = win32gui.GetWindowRect(hwnd)
    left, top, right, bottom = rect
    return {"top": top, "left": left, "width": right - left, "height": bottom - top}

def enhance_frame(frame, onnx_session):
    # Preprocess: BGR uint8 [H,W,3] -> RGB float32 [1,3,H,W], normalized to [0,1]
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = img.astype(np.float32) / 255.0
    img = np.transpose(img, (2, 0, 1))[np.newaxis, ...]  # [1,3,H,W]

    # ONNX expects input name, usually 'input' or similar
    input_name = onnx_session.get_inputs()[0].name
    ort_inputs = {input_name: img}

    # Run inference
    ort_outs = onnx_session.run(None, ort_inputs)
    out_img = ort_outs[0]  # [1,3,H',W']

    # Postprocess: [1,3,H',W'] -> [H',W',3] uint8 BGR
    out_img = np.clip(out_img, 0, 1)
    out_img = out_img.squeeze(0)
    out_img = np.transpose(out_img, (1, 2, 0))  # [H',W',3]
    out_img = (out_img * 255.0).round().astype(np.uint8)
    out_img = cv2.cvtColor(out_img, cv2.COLOR_RGB2BGR)
    return out_img

def start_capture(window_title, onnx_model_path):
    hwnd = find_window(window_title)
    if not hwnd:
        raise RuntimeError(f"Window with title containing '{window_title}' not found")
    monitor = get_window_rect(hwnd)

    cv2.namedWindow("Overlay", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Overlay", monitor['width'], monitor['height'])

    sct = mss.mss()
    frame_count = 0          # For FPS calculation, resets every second
    total_frame_count = 0    # For sampling, increments continuously
    start_time = time.time()
    selected_r = random.randint(0, 4)  # Random index (0-4) for the first chunk

    try:
        sess = ort.InferenceSession(onnx_model_path, providers=["CPUExecutionProvider"])
        while True:
            if not win32gui.IsWindow(hwnd):
                print("Target window was closed.")
                break

            # Check window size every 5 frames to reduce overhead
            if total_frame_count % 5 == 0:
                new_monitor = get_window_rect(hwnd)
                if (abs(new_monitor['width'] - monitor['width']) > 10 or 
                    abs(new_monitor['height'] - monitor['height']) > 10):
                    cv2.resizeWindow("Overlay", new_monitor['width'], new_monitor['height'])
                    monitor = new_monitor
                    print(f"Window resized to {new_monitor['width']}x{new_monitor['height']}")

            # Skip capture if window is minimized (width/height <= 0)
            if monitor['width'] <= 0 or monitor['height'] <= 0:
                time.sleep(0.1)
                continue

            # Start a new chunk every 5 frames and select a random frame index
            if total_frame_count % 5 == 0:
                selected_r = random.randint(0, 4)

            # Capture the frame
            frame = np.array(sct.grab(monitor))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

            # Enhance with ONNX if this frame is the selected one in the chunk
            if (total_frame_count % 5) == selected_r:
                try:
                    frame = enhance_frame(frame, sess)
                except Exception as e:
                    print(f"Enhancement error: {e}")

            # Display the frame
            cv2.imshow("Overlay", frame)
            
            # Increment counters
            total_frame_count += 1
            frame_count += 1

            # Calculate and display FPS every second
            elapsed = time.time() - start_time
            if elapsed >= 1.0:
                fps = frame_count / elapsed
                print(f"FPS: {fps:.2f}")
                frame_count = 0
                start_time = time.time()

            # Exit on 'q' key press
            if cv2.waitKey(1) == ord("q"):
                break

    finally:
        cv2.destroyAllWindows()

if __name__ == '__main__':
    window_title = "Calculator"
    onnx_model_path = "realSR_BSRGAN_DFO_s64w8_SwinIR-M_x4_GAN.onnx"
    try:
        start_capture(window_title, onnx_model_path)
    except RuntimeError as e:
        print(e)