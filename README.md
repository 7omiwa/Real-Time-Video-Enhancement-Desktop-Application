# Real-Time Video Enhancement Desktop Application

Overview
This repository contains the implementation of a desktop application designed to enhance video quality in real-time for videoconferencing platforms, developed as a final year project at Redeemer’s University. The project addresses the challenges of poor video quality in platforms like Zoom and Microsoft Teams, caused by low-resolution webcams, poor lighting, or network issues. Due to browser sandboxing restrictions, the solution shifted from a browser plugin to a desktop-based approach that captures and enhances video streams by mirroring the parent window.
The application focuses on lightweight, CPU-friendly video enhancement techniques, making it suitable for average hardware used in academic environments. It evaluates multiple models (e.g., ReBotNet, Real-ESRGAN, NAFNet, SwinIR, and CLAHE) for their feasibility in real-time scenarios, prioritizing low latency and perceptual quality.

# Features
Real-Time Video Enhancement: Processes video frames from selected application windows (e.g., Zoom, Teams) to improve clarity, brightness, and reduce noise.
Lightweight Design: Optimized for CPU-based systems, ensuring accessibility for users without high-end GPUs.
User-Friendly Interface: Built with Tkinter, offering a minimalistic UI with options to select windows, toggle enhancements, and switch between light/dark themes.
Flexible Enhancement Modes: Supports both classical (CLAHE) and deep learning-based models (ReBotNet, Real-ESRGAN, etc.) for varied use cases.
Comprehensive Evaluation: Includes quantitative analysis (PSNR, SSIM, compute time) of enhancement models for real-world applicability.

# Problem Statement
Videoconferencing platforms often suffer from poor video quality due to hardware limitations (e.g., low-resolution webcams) and network issues (e.g., compression artifacts, bandwidth constraints). These issues lead to blurry visuals, difficulty interpreting non-verbal cues, and increased cognitive fatigue (e.g., Zoom fatigue). Existing solutions are either computationally intensive, GPU-dependent, or lack real-time capabilities, making them impractical for academic settings with standard hardware.
This project aims to design and evaluate a desktop application that enhances video streams in real-time, improving visual clarity and user engagement while maintaining low latency on CPU-based systems.

# Objectives
Identify common video quality issues in videoconferencing platforms.
Develop a desktop application for real-time video enhancement.
Evaluate lightweight enhancement models suitable for low-resource environments.
Provide quantitative performance metrics (PSNR, SSIM, FPS) for model comparison.
Recommend practical strategies for real-world deployment.

# System Architecture
The application follows a modular architecture:
User Interface (UI): Built with Tkinter for a simple, intuitive control panel.
Frame Capture: Uses Windows APIs (win32gui, mss) to capture video from specific application windows.
Enhancement Engine: Applies classical (CLAHE) or deep learning models (ReBotNet, Real-ESRGAN, NAFNet, SwinIR) for video processing.
Output: Displays enhanced frames in a transparent overlay or routes them to virtual camera tools for integration with conferencing platforms.
<img width="869" height="605" alt="image" src="https://github.com/user-attachments/assets/1c844393-95d5-4a2c-8119-82007b96ec5b" />


# Technologies Used
Programming Language: Python 3.10+
Frontend: Tkinter, PyQt5
Frame Capture: win32gui, mss
Video Processing: OpenCV, NumPy
Model Inference: PyTorch, ONNX Runtime
Evaluation Metrics: PSNR, SSIM (via scikit-image)
Dataset: VideoCall-MOS-Set for testing real-world conferencing scenarios
Other Tools: Conda (environment management), FFmpeg (video processing, deprecated in final pipeline)

# Installation
Prerequisites
Windows 10 or newer
Python 3.10+
8GB RAM (16GB recommended for model testing)
Optional: CUDA-compatible GPU for deep learning models

# Steps
Clone the Repository:
git clone https://github.com/your-username/video-enhancement-app.git
cd video-enhancement-app


# Set Up Environment:
conda create -n video-enhancement python=3.10
conda activate video-enhancement
pip install -r requirements.txt

# Install Dependencies: Ensure the following libraries are installed:
opencv-python
numpy
pywin32
mss
pytorch (with optional CUDA support)
onnxruntime
scikit-image
tk

# Download Pretrained Models:
Download pretrained models (e.g., ReBotNet, Real-ESRGAN) from their respective repositories (links in references).
Place models in the models/ directory.

# Run the Application:
python main.py

# Usage
Launch the application (main.py).
Select the target window (e.g., "Zoom" or "Microsoft Teams") from the UI dropdown.
Load a pretrained ONNX model or use the default CLAHE enhancement.
Toggle enhancement settings (e.g., brightness, denoising) or switch between light/dark themes.
Start real-time enhancement and view the output in a transparent overlay window.
Optionally, integrate with virtual camera tools (e.g., pyvirtualcam) for use in conferencing platforms.
Evaluation Results

# The following table summarizes the performance of evaluated models on a single frame:
Model, Compute-Time(s), PSNR(dB), SSIM, Remarks

# Real-ESRGAN (BSRGAN)
Compute Time(s) 0.50
PSNR (dB) 32.01
SSIM 0.8719
Preserved structure, mild blur remained

# Real-ESRGAN + SwinIR-M onnx Model
Compute Time(s) 0.48s
PSNR (dB) 29.32
SSIM 0.8168
Too smooth, facial deformation observed

# Real-ESRGAN + SwinIR-Lx 4 onnx Model
Compute Time(s) 0.48s
PSNR (dB) 29.32
SSIM 0.8168
Well-enhanced, looks AI generated (too much enhancement)

# SwinIR onnx Model
Compute Time(s) 17.01s (GPU)
PSNR (dB) 30.44
SSIM 0.8071
Slow, unnatural face textures

#NAFNet onnx Model
Compute Time(s) 2.84s (CPU)
PSNR (dB) 36.13
SSIM 0.9715
High quality, too slow for real-time


# EvTexture onnx Model
N/A (OOM)
-
-
High memory usage (~14GB), not runnable

# ReBotNet
TBD
PSNR (dB) 33.86
SSIM 0.9409
Failed to enhance visually

#CLAHE (OpenCV) onnx Model
0.0008
PSNR (dB) 24.39
SSIM 0.9019
Fast, modest enhancement, suitable for real-time
<img width="1238" height="1353" alt="image" src="https://github.com/user-attachments/assets/7793fe54-b21c-42d3-9e40-93b2b3993ad3" />


# Key Insights:
SwinIR-Lx4 (RealSr Variant) : Achieves near real-time performance (0.8ms/frame, ~1250 FPS) with acceptable visual clarity, making it the most practical for low-resource systems.
Deep Learning Models: High-quality outputs but too slow (0.48–18s/frame) for real-time use without GPU optimization.
Trade-offs: Balancing quality, speed, and resource usage remains a challenge, with no single model meeting all requirements.

# Limitations
Hardware Constraints: Deep learning models require GPU acceleration for optimal performance, limiting accessibility.
Temporal Consistency: Most models lack video-specific temporal modeling, leading to flickering in enhanced streams.
Platform Restrictions: Browser-based approaches were abandoned due to sandboxing, increasing desktop app complexity.
Testing Scope: Evaluations were limited to local setups and a single dataset (VideoCall-MOS-Set).

# Future Work
Develop a custom lightweight model using knowledge distillation for better CPU performance.
Implement adaptive resolution pipelines to adjust enhancement intensity dynamically.
Explore edge-cloud hybrid processing to offload heavy computations while maintaining low latency.
Add user-configurable quality controls (e.g., sliders for enhancement strength).
Expand testing to diverse hardware and network conditions.

# References
Valanarasu, J. M. J., et al. (2023). ReBotNet: Fast real-time video enhancement. WACV 2025.
Wang, X., et al. (2021). Real-ESRGAN: Training Real-World Blind Super-Resolution with Pure Synthetic Data. arXiv:2107.10833.
Chen, X., et al. (2022). Simple Baselines for Image Restoration. arXiv:2204.04676.
Liang, J., et al. (2021). SwinIR: Image Restoration Using Swin Transformer. ICCV Workshops.
Zuiderveld, K. (1994). Contrast Limited Adaptive Histogram Equalization. Graphics Gems IV.
Papers with Code. VideoCall-MOS-Set Dataset. Link.

# Contributing
Contributions are welcome! Please follow these steps:
Fork the repository.
Create a new branch (git checkout -b feature/your-feature).
Commit your changes (git commit -m 'Add your feature').
Push to the branch (git push origin feature/your-feature).
Open a pull request.

# License
This project is licensed under the MIT License. See the LICENSE file for details.

# Contact
For questions or feedback, please reach out to [olaonipekuntomiwa@gmail.com] or open an issue on this repository.
