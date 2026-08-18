# Rocket League AI Mechanics Analyzer & Coach

> A 3D telemetry processor and analytics engine that parses Rocket League replay files to evaluate player kinematics, detect mechanic attempts, and generate coaching feedback.

## Overview

This project provides an automated analytics pipeline for Rocket League. Instead of using heavy Computer Vision models on video recordings, it parses raw binary replay files (30 Hz network logs containing X, Y, Z coordinates, rotation quaternions, velocities, and wheel contact states) to evaluate movement efficiency, detect mechanic attempts (such as flip resets, flicks, and wave dashes), and supply data-driven feedback.

## Architecture

1. Replay Files (.replay)
2. boxcars-py Parser (Rust/Python)
3. Pandas DataFrames + SciPy Spatial Math
4. Vector Feature Engine (Car-to-ball relative speed, quaternion rotation spikes, roof contacts)
5. Mechanic Detector (Differentiates Attempted vs. Executed Mechanics)
6. JSON Summary Export / Analytics Logs

## Technical Stack

* Language: Python 3
* File Parsing: boxcars-py (Rust-powered parser with Python bindings)
* Data Manipulation: Pandas
* Spatial & Vector Math: SciPy (Quaternion transformations and 3D space calculations)
* Version Control: Git, GitHub

## How It Works

1. Replay Parsing: Reads native binary .replay files and extracts frame-by-frame entity telemetry into Pandas DataFrames.
2. Quaternion Conversion: Uses SciPy to convert compressed car orientation quaternions into 3D directional vectors (nose, roof, and side vectors).
3. Mechanic Detection:
   * Flip Resets: Monitors wheel-contact flags while car height > 200 units, checking for post-contact jump impulses.
   * Flicks: Tracks distance between roof vector and ball center, identifying relative zero-velocity alignment followed by angular acceleration spikes.
   * Wave Dashes: Detects single-wheel ground contact paired with sudden pitch/roll impulse transfers near ground level.
4. Data Export: Structures detected events, timestamps, and movement stats into clean JSON output files.

## Project Setup

1. Clone the repository:
   git clone https://github.com/Thomas-Coulter/RL-Coach.git

2. Install dependencies:
   pip install boxcars pandas scipy

3. Run the analyzer on a replay file:
   python main.py --replay path/to/your_file.replay

## License & Intellectual Property

© 2026 Thomas Coulter. All rights reserved.

This repository and its source code are published solely for portfolio evaluation and demonstration purposes. No permission is granted for commercial use, redistribution, modification, or inclusion in proprietary software.
