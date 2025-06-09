# simulation.py
"""
Simulates data for multiple aircraft when ROS is not available.
"""
import time
import math
import queue
from typing import List, Dict
from aircraft_state import AircraftState

def simulate_multiple_aircraft(configs: List[Dict], data_queue: queue.Queue):
    """Simulates flight data for a list of aircraft configurations."""
    print("[*] Running in multi-aircraft simulation mode.")
    
    states = [
        AircraftState(
            aircraft_id=config["id"],
            pilot_name=config.get("pilot_name", "SIM_PILOT"),
            aircraft_type=config.get("aircraft_type", "Simulator")
        ) for config in configs
    ]
    
    start_time = time.time()
    
    while True:
        elapsed = time.time() - start_time
        
        for i, state in enumerate(states):
            # Create a unique pattern for each aircraft
            angle = elapsed * (0.1 + i * 0.02)
            radius = 1 + i * 0.1
            
            state.latitude = 37.5665 + radius * math.cos(angle)
            state.longitude = 126.9780 + radius * math.sin(angle)
            state.altitude_m = 200 + i * 50 + 50 * math.sin(elapsed * 0.1 + i)
            
            state.yaw_deg = (math.degrees(angle)) % 360 
            state.roll_deg = -20 * math.cos(angle)
            state.pitch_deg = 5 * math.sin(angle)
            
            state.ground_speed_mps = 30 + 10 * math.sin(elapsed * 0.2 + i)
            state.armed = True
            state.mode = "AUTO"
            state.last_update = time.time()
            
            try:
                data_queue.put_nowait(state)
            except queue.Full:
                pass
        
        time.sleep(0.1)