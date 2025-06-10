# ros_bridge.py
"""
ROS1 MAVROS Bridge to collect telemetry for multiple aircraft.
"""
import rospy
import math
import queue
from typing import Dict, List
from sensor_msgs.msg import NavSatFix, Imu
from geometry_msgs.msg import TwistStamped
from mavros_msgs.msg import State
from aircraft_state import AircraftState, RAD_TO_DEG

class MAVROSBridge:
    """ROS1 node to collect and manage MAVROS data for multiple aircraft."""
    
    def __init__(self, configs: List[Dict], data_queue: queue.Queue):
        self.data_queue = data_queue
        self.aircraft_states: Dict[str, AircraftState] = {}
        
        rospy.init_node('tacview_multi_mavros_bridge', anonymous=True)

        for config in configs:
            ac_id = config["id"]
            ns = config["ros_namespace"]
            
            # Create a state object for each aircraft
            self.aircraft_states[ac_id] = AircraftState(
                aircraft_id=ac_id,
                pilot_name=config.get("pilot_name", "PILOT"),
                aircraft_type=config.get("aircraft_type", "Generic"),
                coalition=config.get("coalition", "Neutrals"),
                country=config.get("country", "XX")
            )
            
            # Dynamically create subscribers for each namespace
            rospy.Subscriber(
                f'/{ns}/mavros/global_position/global', NavSatFix, 
                self.global_position_callback, callback_args=ac_id, queue_size=10
            )
            rospy.Subscriber(
                f'/{ns}/mavros/imu/data', Imu, 
                self.imu_callback, callback_args=ac_id, queue_size=10
            )
            rospy.Subscriber(
                f'/{ns}/mavros/local_position/velocity_local', TwistStamped, 
                self.velocity_callback, callback_args=ac_id, queue_size=10
            )
            rospy.Subscriber(
                f'/{ns}/mavros/state', State, 
                self.state_callback, callback_args=ac_id, queue_size=10
            )
            rospy.loginfo(f"Subscribed to topics for aircraft ID {ac_id} in namespace '/{ns}'")

        self.timer = rospy.Timer(rospy.Duration(0.1), self.publish_states)  # 10Hz

    def global_position_callback(self, msg, ac_id):
        state = self.aircraft_states[ac_id]
        if msg.status.status >= 0:
            state.latitude = msg.latitude
            state.longitude = msg.longitude
            state.altitude_m = msg.altitude
        #print(f"Global position updated for {ac_id}: "
        #      f"Lat={state.latitude}, Lon={state.longitude}, Alt={state.altitude_m}m")

    def imu_callback(self, msg, ac_id):
        state = self.aircraft_states[ac_id]
        q = msg.orientation
        sinr_cosp = 2 * (q.w * q.x + q.y * q.z)
        cosr_cosp = 1 - 2 * (q.x * q.x + q.y * q.y)
        state.roll_deg = math.atan2(sinr_cosp, cosr_cosp) * RAD_TO_DEG
        
        sinp = 2 * (q.w * q.y - q.z * q.x)
        state.pitch_deg = (math.copysign(math.pi / 2, sinp) * RAD_TO_DEG 
                           if abs(sinp) >= 1 else math.asin(sinp) * RAD_TO_DEG)
        
        siny_cosp = 2 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1 - 2 * (q.y * q.y + q.z * q.z)
        yaw = math.atan2(siny_cosp, cosy_cosp) * RAD_TO_DEG
        state.yaw_deg = yaw if yaw >= 0 else yaw + 360

    def velocity_callback(self, msg, ac_id):
        state = self.aircraft_states[ac_id]
        state.ground_speed_mps = math.sqrt(msg.twist.linear.x**2 + msg.twist.linear.y**2)

    def state_callback(self, msg, ac_id):
        state = self.aircraft_states[ac_id]
        state.armed = msg.armed
        state.mode = msg.mode

    def publish_states(self, event):
        for ac_id, state in self.aircraft_states.items():
            state.last_update = rospy.get_time()
            try:
                self.data_queue.put_nowait(state)
            except queue.Full:
                rospy.logwarn(f"Data queue is full. Skipping state publish for {ac_id}.")

    def spin(self):
        try:
            rospy.spin()
        except rospy.ROSInterruptException:
            rospy.loginfo("ROS node interrupted")