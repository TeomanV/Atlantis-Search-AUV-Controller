import time
import math
from datetime import datetime
import numpy as np
from config import *
from visualization import AUVVisualizer

class AUVController:
    def __init__(self, simulation_mode=True):
        self.start_time = None
        self.current_position = [0.0, 0.0]  # Initialize with [x, y] coordinates
        self.current_depth = 0.0
        self.current_heading = 0.0
        self.battery_level = 100
        self.mission_completed = False
        self.emergency_mode = False
        self.simulation_mode = simulation_mode
        self.position_history = []  # Store position history for visualization
        self.visualizer = None
        self.last_update_time = None
        
    def initialize(self):
        """Initialize all systems and sensors"""
        print("Initializing AUV systems...")
        if self.simulation_mode:
            print("Running in simulation mode")
            # Initialize simulation parameters
            self.current_position = [0.0, 0.0]  # Start at origin
            self.current_heading = 0.0
            self.current_depth = 0.0
            # Initialize visualizer
            self.visualizer = AUVVisualizer()
        else:
            # Initialize actual hardware here
            # This would include GPS, IMU, depth sensor, etc.
            pass
            
        self.start_time = time.time()
        self.last_update_time = self.start_time
        self.position_history.append(self.current_position.copy())
        print(f"Initial position: {self.current_position}")
        print("Initialization complete")
        
    def check_safety(self):
        """Check all safety parameters"""
        if self.battery_level < BATTERY_LOW_THRESHOLD:
            print("WARNING: Low battery!")
            self.emergency_surface()
            return False
            
        # Check mission time
        if time.time() - self.start_time > MAX_MISSION_TIME:
            print("WARNING: Mission time exceeded!")
            self.emergency_surface()
            return False
            
        return True
    
    def emergency_surface(self):
        """Emergency surfacing procedure"""
        print("Initiating emergency surface procedure")
        self.emergency_mode = True
        self.current_depth = EMERGENCY_SURFACE_DEPTH
        print(f"Emergency surface completed. Current depth: {self.current_depth}m")
        
    def navigate_to_target(self, target_position):
        """Navigate to target position while maintaining depth"""
        if not self.check_safety():
            return False
            
        # Calculate distance and heading to target
        dx = target_position[0] - self.current_position[0]
        dy = target_position[1] - self.current_position[1]
        distance = math.sqrt(dx*dx + dy*dy)
        target_heading = math.degrees(math.atan2(dy, dx))
        
        print(f"Distance to target: {distance:.2f}m")
        print(f"Current heading: {self.current_heading:.1f}°")
        print(f"Target heading: {target_heading:.1f}°")
        
        # Adjust heading
        heading_diff = target_heading - self.current_heading
        if abs(heading_diff) > HEADING_TOLERANCE:
            # Simulate heading adjustment
            if heading_diff > 0:
                self.current_heading += min(HEADING_TOLERANCE, heading_diff)
            else:
                self.current_heading -= min(HEADING_TOLERANCE, abs(heading_diff))
            print(f"Adjusted heading to: {self.current_heading:.1f}°")
            
        # Move forward while maintaining depth
        if distance > POSITION_TOLERANCE:
            # Calculate time since last update
            current_time = time.time()
            dt = current_time - self.last_update_time
            self.last_update_time = current_time
            
            # Simulate movement with proper timing
            step_size = min(SPEED * dt, distance)  # Move based on time elapsed
            self.current_position[0] += step_size * math.cos(math.radians(self.current_heading))
            self.current_position[1] += step_size * math.sin(math.radians(self.current_heading))
            self.position_history.append(self.current_position.copy())
            print(f"New position: {self.current_position}")
            
        return True
        
    def maintain_depth(self, target_depth):
        """Maintain specified depth"""
        if not self.check_safety():
            return False
            
        depth_diff = target_depth - self.current_depth
        if abs(depth_diff) > 0.1:
            # Calculate time since last update
            current_time = time.time()
            dt = current_time - self.last_update_time
            self.last_update_time = current_time
            
            # Simulate depth control with proper timing
            step_size = min(0.5 * dt, abs(depth_diff))  # 0.5 m/s vertical speed
            if depth_diff > 0:
                self.current_depth += step_size
            else:
                self.current_depth -= step_size
            print(f"Current depth: {self.current_depth:.2f}m")
            
        return True
        
    def execute_mission(self):
        """Execute the main mission"""
        print("Starting mission...")
        self.initialize()
        
        # Mission sequence
        try:
            # 1. Dive to target depth
            print("Diving to target depth...")
            while abs(self.current_depth - TARGET_DEPTH) > 0.1:
                if not self.maintain_depth(TARGET_DEPTH):
                    return False
                if self.simulation_mode and self.visualizer:
                    self.visualizer.update(self.position_history, self.current_depth,
                                         time.time() - self.start_time, self.current_heading)
                time.sleep(0.1)  # Add small delay for smoother simulation
                
            # 2. Navigate to smallest finish area
            print("Navigating to finish area...")
            target_finish = self.get_target_finish_position()
            while True:
                if not self.navigate_to_target(target_finish):
                    return False
                    
                # Check if we've reached the target
                dx = target_finish[0] - self.current_position[0]
                dy = target_finish[1] - self.current_position[1]
                distance = math.sqrt(dx*dx + dy*dy)
                
                if distance <= POSITION_TOLERANCE:
                    break
                    
                if self.simulation_mode and self.visualizer:
                    self.visualizer.update(self.position_history, self.current_depth,
                                         time.time() - self.start_time, self.current_heading)
                time.sleep(0.1)  # Add small delay for smoother simulation
                
            # 3. Surface at finish
            print("Surfacing at finish...")
            while abs(self.current_depth) > 0.1:
                if not self.maintain_depth(0.0):
                    return False
                if self.simulation_mode and self.visualizer:
                    self.visualizer.update(self.position_history, self.current_depth,
                                         time.time() - self.start_time, self.current_heading)
                time.sleep(0.1)  # Add small delay for smoother simulation
                
            self.mission_completed = True
            mission_time = time.time() - self.start_time
            print(f"Mission completed in {mission_time:.2f} seconds")
            
            # Keep the visualization window open for a few seconds after completion
            if self.simulation_mode and self.visualizer:
                time.sleep(3)
                self.visualizer.close()
                
            return True
            
        except Exception as e:
            print(f"Mission failed: {str(e)}")
            self.emergency_surface()
            if self.simulation_mode and self.visualizer:
                self.visualizer.close()
            return False
            
    def get_target_finish_position(self):
        """Get the position of the smallest finish area"""
        # For simulation, return a position 10 meters away at 45 degrees
        return [10.0, 10.0]

def main():
    # Run in simulation mode
    controller = AUVController(simulation_mode=True)
    success = controller.execute_mission()
    
    if success:
        print("Mission completed successfully!")
    else:
        print("Mission failed!")

if __name__ == "__main__":
    main() 