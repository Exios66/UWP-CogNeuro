#!/usr/bin/env python
"""
Algorithm: Frame Dropping & Temporal Disruption in Optical Flow
Simulating akinetopsia by disrupting motion perception.

Libraries required:
    - OpenCV (cv2)
    - NumPy
    - TensorFlow

Ensure you have installed these via:
    pip install opencv-python numpy tensorflow
"""

import cv2
import numpy as np
import tensorflow as tf  # For an alternative MCMC (Markov chain) state update

# ---------------------------
# Markov Chain state update
# ---------------------------

def markov_chain_update_numpy(state, transition_matrix):
    """
    Update the current state using NumPy-based random choice.
    state: current state index (0: normal, 1: disrupted)
    transition_matrix: list of lists with row [P(normal), P(disrupted)]
    Returns the next state.
    """
    probabilities = transition_matrix[state]
    next_state = np.random.choice([0, 1], p=probabilities)
    return next_state

def markov_chain_update_tf(state, transition_matrix):
    """
    Update the current state using TensorFlow's categorical sampling.
    state: current state (0 or 1)
    transition_matrix: list of lists with row [P(normal), P(disrupted)]
    Returns the next state (as int).
    """
    # Convert the probability row to a tensor and take the log
    probs = tf.constant(transition_matrix[state], dtype=tf.float32)
    # tf.random.categorical expects a 2D tensor; sample 1 value.
    next_state = tf.random.categorical(tf.math.log([probs]), num_samples=1)
    return int(next_state.numpy()[0][0])

# ---------------------------
# Optical Flow Computation
# ---------------------------

def compute_optical_flow(prev_gray, curr_gray):
    """
    Compute dense optical flow using Farneback's algorithm.
    prev_gray: previous frame in grayscale.
    curr_gray: current frame in grayscale.
    Returns the flow field.
    """
    flow = cv2.calcOpticalFlowFarneback(prev_gray, curr_gray,
                                        None,      # initial flow
                                        0.5, 3, 15, 3, 5, 1.2, 0)
    return flow

# ---------------------------
# Visualization Helper
# ---------------------------

def flow_to_rgb(flow):
    """
    Convert the optical flow field to an RGB visualization using HSV mapping.
    flow: optical flow field (NxMx2 array).
    Returns an RGB image.
    """
    # Create an HSV image where:
    # Hue encodes the angle, Saturation is set to maximum,
    # and Value encodes the magnitude (normalized).
    hsv = np.zeros((flow.shape[0], flow.shape[1], 3), dtype=np.uint8)
    hsv[..., 1] = 255

    mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    # Angle mapping: convert to degrees and scale down to [0,180]
    hsv[..., 0] = ang * 180 / np.pi / 2
    hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
    rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return rgb

# ---------------------------
# Main Processing Loop
# ---------------------------

def main():
    # Video input file (update with your video source)
    video_path = 'input_video.mp4'
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to read the first frame.")
        return

    # Convert the first frame to grayscale
    prev_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Initialize Markov chain parameters:
    # State 0: Normal optical flow processing.
    # State 1: Disrupted processing (simulate akinetopsia).
    current_state = 0
    # Transition matrix [from_state][to_state]:
    # For example, when in normal state, 90% chance to remain normal, 10% to disrupt.
    # In disrupted state, a 60% chance to return to normal, 40% to remain disrupted.
    transition_matrix = [[0.9, 0.1],
                         [0.6, 0.4]]

    # Saccadic masking: Compute optical flow only every N frames.
    optical_flow_interval = 5
    last_flow = None
    frame_count = 0

    # Choose which state update function to use:
    use_tensorflow_update = False  # Set True to use TensorFlow-based update.
    
    print("Processing video for simulated akinetopsia...")
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert current frame to grayscale
        curr_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Update state using Markov chain.
        if use_tensorflow_update:
            current_state = markov_chain_update_tf(current_state, transition_matrix)
        else:
            current_state = markov_chain_update_numpy(current_state, transition_matrix)
        
        # Determine if optical flow is computed on this frame (saccadic masking)
        if frame_count % optical_flow_interval == 0:
            if current_state == 0:
                # Normal: compute optical flow normally.
                flow = compute_optical_flow(prev_gray, curr_gray)
            else:
                # Disrupted: simulate a breakdown.
                # Option 1: set the flow to zeros (i.e. no motion detected).
                flow = np.zeros((curr_gray.shape[0], curr_gray.shape[1], 2), dtype=np.float32)
                # Option 2: Alternatively, you could use the previous valid flow:
                # flow = last_flow if last_flow is not None else compute_optical_flow(prev_gray, curr_gray)
                # Option 3: Or add noise to simulate erratic motion perception.
        else:
            # Between intervals, re-use the last computed flow (simulating saccadic masking)
            flow = last_flow if last_flow is not None else compute_optical_flow(prev_gray, curr_gray)

        # Store the last computed flow for reuse.
        last_flow = flow

        # Visualize the flow
        rgb_flow = flow_to_rgb(flow)
        cv2.imshow('Simulated Optical Flow', rgb_flow)

        # Exit if 'q' is pressed.
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

        # Update the previous frame.
        prev_gray = curr_gray
        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
