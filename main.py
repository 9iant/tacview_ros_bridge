#!/usr/bin/env python3
# main.py
"""
Main entry point for the PX4 to Tacview Real-time Telemetry Bridge.
Handles multiple aircraft by dynamically creating ROS subscribers or simulations.
"""
import threading
import queue
import sys

# Import configurations and components
from config import AIRCRAFT_CONFIG
from tacview_server import TacviewServer

# Check for ROS availability
IS_ROS = False  # Set to True for testing without ROS
if IS_ROS:
    print("[*] Running in ROS mode.")
    import rospy
    from ros_bridge import MAVROSBridge
    ROS_AVAILABLE = True
else:
    print("[*] Running in simulation mode.")
    from simulation import simulate_multiple_aircraft
    ROS_AVAILABLE = False


"""Initializes and runs the bridge components."""
print("PX4 to Tacview Multi-Aircraft Bridge Starting...")

if not AIRCRAFT_CONFIG:
    print("[!] No aircraft configured in config.py. Exiting.")
    sys.exit(1)
    
# Data queue for communication between data source and server
data_queue = queue.Queue(maxsize=100)

# Start Tacview server in a separate thread
tacview_server = TacviewServer(data_queue)
server_thread = threading.Thread(target=tacview_server.start, daemon=True)
server_thread.start()

try:
    if IS_ROS:
        # Start MAVROS bridge for the configured aircraft
        print("[*] Starting MAVROS bridge...")
        mavros_bridge = MAVROSBridge(AIRCRAFT_CONFIG, data_queue)
        mavros_bridge.spin()
    else:
        # Run simulation mode for the configured aircraft
        simulate_multiple_aircraft(AIRCRAFT_CONFIG, data_queue)

except KeyboardInterrupt:
    print("\n[*] Shutdown requested by user.")
except Exception as e:
    print(f"[!] An unexpected error occurred: {e}")
finally:
    tacview_server.stop()
    print("[*] Bridge shutdown complete.")

