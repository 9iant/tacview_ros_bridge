# config.py
"""
Aircraft configuration for the Tacview bridge.
Define all aircraft to be tracked in this list.
"""

# AIRCRAFT_CONFIG = [
#     {
#         "id": "1001",
#         "ros_namespace": "uav1",
#         "pilot_name": "MAVERICK",
#         "aircraft_type": "F-18",
#         "coalition": "Allies",
#         "country": "US"
#     },
#     {
#         "id": "2002",
#         "ros_namespace": "uav2",
#         "pilot_name": "ICEMAN",
#         "aircraft_type": "F-14",
#         "coalition": "Allies",
#         "country": "US"
#     },
#     {
#         "id": "3003",
#         "ros_namespace": "sim_drone",
#         "pilot_name": "SIM_PILOT_1",
#         "aircraft_type": "Quadcopter",
#         "coalition": "Neutrals",
#         "country": "KR"
#     }
# ]

AIRCRAFT_CONFIG = [
    {
        "id": "1001",
        "ros_namespace": "uav0",
        "pilot_name": "MAVERICK",
        "aircraft_type": "F-18",
        "coalition": "Allies",
        "country": "US"
    },
    {
        "id": "2002",
        "ros_namespace": "uav1",
        "pilot_name": "ICEMAN",
        "aircraft_type": "F-14",
        "coalition": "Allies",
        "country": "US"
    },
    {
        "id": "3003",
        "ros_namespace": "uav2",
        "pilot_name": "SIM_PILOT_1",
        "aircraft_type": "Quadcopter",
        "coalition": "Neutrals",
        "country": "KR"
    }
]

# Server Configuration
HOST = '0.0.0.0'
PORT = 42674