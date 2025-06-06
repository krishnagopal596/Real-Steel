#!/usr/bin/env python3
"""
Main script for controlling PoseMirror3D with Robot Retargeting.
This allows upper body boxing motion to be detected, retargeted to a robot figure,
and recorded to CSV files.
"""

import os
import argparse
from datetime import datetime

from pose_mirror_retargeting import PoseMirror3DWithRetargeting

def main():
    parser = argparse.ArgumentParser(description='Run pose detection and retargeting system')
    
    parser.add_argument('--record', action='store_true', 
                        help='Start recording immediately')
    parser.add_argument('--output', type=str, default='recordings',
                        help='Directory to save recordings (default: recordings)')
    parser.add_argument('--freq', type=int, default=10,
                        help='Recording frequency in Hz (default: 10)')
    parser.add_argument('--window', type=int, nargs=2, default=(800, 600),
                        help='Window size as width height (default: 800 600)')
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    
    # Initialize the system
    system = PoseMirror3DWithRetargeting(window_size=tuple(args.window))
    
    # Set recording frequency
    system.robot_retargeter.recording_freq = args.freq
    
    # Auto-start recording if requested
    if args.record:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"{args.output}/robot_motion_{timestamp}.csv"
        system.robot_retargeter.start_recording(filename)
        print(f"Auto-recording to {filename}")
    
    # Run the system
    print("Starting PoseMirror3D with Robot Retargeting")
    print("Controls:")
    print("  R - Reset calibration")
    print("  S - Start/stop recording")
    print("  Q - Quit")
    print("  Arrow keys - Rotate view")
    
    try:
        system.run()
    except KeyboardInterrupt:
        print("\nExiting gracefully...")
    
    print("Done.")

if __name__ == "__main__":
    main()