import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import time
from config import *
import math

class AUVVisualizer:
    def __init__(self):
        plt.ion()  # Turn on interactive mode
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(15, 5))
        self.fig.suptitle('AUV Simulation')
        
        # Initialize empty plots
        self.path_line, = self.ax1.plot([], [], 'b-', label='Path')
        self.auv_point, = self.ax1.plot([], [], 'ro', label='AUV')
        self.depth_line, = self.ax2.plot([], [], 'g-', label='Depth')
        
        # Add finish area visualization
        self.finish_area = None
        
        # Add heading indicator
        self.heading_arrow = None
        
        # Setup the top-down view (ax1)
        self.ax1.set_title('Top-Down View')
        self.ax1.set_xlabel('X (m)')
        self.ax1.set_ylabel('Y (m)')
        self.ax1.grid(True)
        self.ax1.legend()
        
        # Setup the depth view (ax2)
        self.ax2.set_title('Depth Profile')
        self.ax2.set_xlabel('Time (s)')
        self.ax2.set_ylabel('Depth (m)')
        self.ax2.grid(True)
        self.ax2.legend()
        
        # Set axis limits
        self.ax1.set_xlim(-5, 15)
        self.ax1.set_ylim(-5, 15)
        self.ax2.set_xlim(0, MAX_MISSION_TIME)
        self.ax2.set_ylim(MAX_DEPTH + 1, -1)  # Inverted for intuitive depth display
        
        # Initialize data storage
        self.times = []
        self.depths = []
        
        # Show the initial plot
        plt.show(block=False)
        
    def draw_finish_area(self, position, size):
        """Draw the finish area as a square"""
        if self.finish_area is not None:
            self.finish_area.remove()
            
        x = position[0] - size/2
        y = position[1] - size/2
        self.finish_area = plt.Rectangle((x, y), size, size, 
                                      fill=False, color='g', 
                                      linestyle='--', label='Finish Area')
        self.ax1.add_patch(self.finish_area)
        
    def draw_heading_indicator(self, position, heading, length=0.5):
        """Draw an arrow indicating the AUV's heading"""
        if self.heading_arrow is not None:
            self.heading_arrow.remove()
            
        # Convert heading to radians
        angle = math.radians(heading)
        dx = length * math.cos(angle)
        dy = length * math.sin(angle)
        
        self.heading_arrow = self.ax1.arrow(position[0], position[1], 
                                          dx, dy, 
                                          head_width=0.1, 
                                          head_length=0.15,
                                          fc='r', 
                                          ec='r')
        
    def update(self, position_history, current_depth, current_time, current_heading):
        """Update the visualization"""
        try:
            # Update path
            if position_history and len(position_history) > 0:
                # Convert position history to numpy array
                positions = np.array(position_history)
                
                # Update path line
                self.path_line.set_data(positions[:, 0], positions[:, 1])
                
                # Update AUV position
                self.auv_point.set_data([positions[-1, 0]], [positions[-1, 1]])
                
                # Draw finish area if we have a target position
                target_pos = [10.0, 10.0]  # This should come from the controller
                self.draw_finish_area(target_pos, 2.0)  # 2m square finish area
                
                # Draw heading indicator
                self.draw_heading_indicator(positions[-1], current_heading)
            
            # Update depth profile
            self.times.append(current_time)
            self.depths.append(current_depth)
            self.depth_line.set_data(self.times, self.depths)
            
            # Update axis limits if needed
            if len(self.times) > 0:
                self.ax2.set_xlim(0, max(self.times) + 1)
            
            # Update title with current status
            status = "Mission in Progress"
            if current_depth < 0.1:
                status = "Surfaced"
            elif current_depth > TARGET_DEPTH - 0.1 and current_depth < TARGET_DEPTH + 0.1:
                status = "At Target Depth"
            self.fig.suptitle(f'AUV Simulation - {status}')
            
            # Update the display
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()
            
        except Exception as e:
            print(f"Visualization error: {str(e)}")
            # Don't raise the exception, just continue with the mission
        
    def close(self):
        """Close the visualization window"""
        plt.close(self.fig) 