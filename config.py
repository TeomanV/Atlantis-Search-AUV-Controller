# Mission Configuration

# Time limits
MAX_MISSION_TIME = 600  # 10 minutes in seconds

# Area dimensions (to be set during competition)
START_AREA_SIZE = None  # Will be provided during competition
FINISH_AREA_SIZES = {
    'small': None,  # x
    'medium': None,  # y
    'large': None   # z
}

# Navigation parameters
MIN_DEPTH = 1.0  # Minimum depth to maintain underwater
MAX_DEPTH = 5.0  # Maximum safe depth
TARGET_DEPTH = 2.0  # Target depth during navigation

# Safety parameters
BATTERY_LOW_THRESHOLD = 20  # Battery percentage
EMERGENCY_SURFACE_DEPTH = 0.5  # Depth to maintain during emergency surface

# Navigation constants
POSITION_TOLERANCE = 0.5  # Meters
HEADING_TOLERANCE = 5.0  # Degrees
SPEED = 1.0  # m/s

# Sensor update rates
GPS_UPDATE_RATE = 1.0  # Hz
DEPTH_UPDATE_RATE = 5.0  # Hz
IMU_UPDATE_RATE = 10.0  # Hz 