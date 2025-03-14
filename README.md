# Atlantis Search AUV Controller

An autonomous underwater vehicle (AUV) controller for the "Kayıp Hazine Avı: Atlantis'in Peşinde" competition. This project implements a Python-based controller that guides an AUV through a mission to reach a finish area while maintaining specific depth requirements.

## 🚀 Features

- Real-time visualization of AUV path and depth profile
- Autonomous navigation to target coordinates
- Depth control and maintenance
- Safety checks and emergency surfacing
- Interactive mission monitoring
- Configurable mission parameters

## 📋 Mission Requirements

The AUV must:
1. Start from the surface
2. Dive to a target depth (2 meters)
3. Navigate to a finish area (2m x 2m square)
4. Surface at the finish area
5. Complete the mission within 10 minutes

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/TeomanV/Atlantis-Search-AUV-Controller.git
cd Atlantis-Search-AUV-Controller
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## 🎮 Usage

Run the simulation:
```bash
python main.py
```

The visualization will show:
- Left plot: Top-down view of AUV path with heading indicator
- Right plot: Depth profile over time
- Real-time status updates
- Finish area visualization

## 📊 Visualization Features

- **Top-Down View**:
  - Blue line: AUV's path
  - Red dot: Current position
  - Red arrow: Current heading
  - Green dashed square: Finish area
  - Grid for reference

- **Depth Profile**:
  - Green line: Depth over time
  - Time on X-axis
  - Depth on Y-axis (inverted for intuitive display)
  - Grid for reference

## ⚙️ Configuration

Mission parameters can be adjusted in `config.py`:
- `TARGET_DEPTH`: Target operating depth (2m)
- `MAX_DEPTH`: Maximum allowed depth (3m)
- `MAX_MISSION_TIME`: Time limit (600s)
- `SAFETY_DEPTH`: Emergency surfacing depth (0.5m)
- `MOVEMENT_SPEED`: AUV speed (0.5 m/s)
- `DEPTH_CHANGE_RATE`: Vertical movement speed (0.2 m/s)
- `TURNING_SPEED`: Rotation speed (30 degrees/s)

## 🔒 Safety Features

- Emergency surfacing if depth exceeds safety limits
- Real-time depth monitoring
- Mission timeout protection
- Position tracking and visualization

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- Teoman V. - Initial work

## 🙏 Acknowledgments

- Competition organizers for providing the mission requirements
- Contributors and testers 