# TurtleBot4 Controller Simulation

[![ROS2](https://img.shields.io/badge/ROS2-Jazzy-blue.svg)](https://docs.ros.org/en/jazzy/)
[![Python](https://img.shields.io/badge/Python-3.10+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Overview

This project contains a **trajectory tracking controller** for the TurtleBot4 robot in Gazebo simulation. The controller implements a **robust adaptive dynamic controller** based on the methodology by Kim et al. (2004) to follow predefined trajectories (circular or figure-8 patterns) with real-time visualization, handling modeling uncertainties and disturbances.

### Features

- **Trajectory Following**: Supports two trajectory modes:
  - `cercle`: Circular trajectory
  - `8`: Figure-8 trajectory (lemniscate)
- **Real-time Visualization**: Live matplotlib plot showing reference trajectory vs actual robot path
- **Disturbance Support**: Optional noise injection for robustness testing:
  - Gaussian noise
  - Sinusoidal disturbances
- **Configurable Parameters**: Control gains, trajectory duration, and more via ROS2 parameters
- **TurtleBot4 Integration**: Publishes velocity commands compatible with TurtleBot4 hardware limits

## Prerequisites

### System Requirements

- **OS**: Ubuntu 24.04 (Noble) or later
- **ROS2**: Jazzy or later
- **Python**: 3.10+

### Dependencies

- ROS2 packages:
  - `rclpy`
  - `geometry_msgs`
  - `turtlebot4_gz_bringup`
  
- Python libraries:
  - `numpy`
  - `matplotlib`

### Installation

If you don't have the TurtleBot4 simulator installed:

```bash
# Install TurtleBot4 simulator packages
sudo apt update
sudo apt install ros-jazzy-turtlebot4-simulator
```

Install Python dependencies (if not already installed):

```bash
sudo apt install python3-numpy python3-matplotlib
```

## Building the Workspace

1. **Clone the repository**:
```bash
git clone https://github.com/renarddaxel312/Kanayama-trajectory-controller.git
cd Kanayama-trajectory-controller
```

2. **Build the packages**:
```bash
colcon build
```

3. **Source the workspace**:
```bash
source install/setup.bash
```

## Running the Simulation

### Step 1: Launch Gazebo Simulator

Open a terminal and run:

```bash
cd ~/cd Kanayama-trajectory-controller  # Navigate to your workspace
source install/setup.bash
ros2 launch turtlebot4_gz_bringup turtlebot4_gz.launch.py world:=empty sensors:=false dock:=false
```

**Parameters explanation**:
- `world:=empty` - Loads an empty world (no obstacles)
- `sensors:=false` - Disables sensor simulation for better performance
- `dock:=false` - Disables the docking station

Wait for Gazebo to fully load before proceeding to the next step.

### Step 2: Launch the Controller

Open a **new terminal** and run:

```bash
cd ~/cd Kanayama-trajectory-controller  # Navigate to your workspace
source install/setup.bash
ros2 run controller_node controller_node
```

The controller will start, and you should see:
- The robot moving in the Gazebo simulator
- A matplotlib window showing the trajectory tracking in real-time

## Configuration

### Basic Usage with Parameters

You can customize the controller behavior using ROS2 parameters:

```bash
ros2 run controller_node controller_node --ros-args \
  -p mode:='8' \
  -p duration:=30.0 \
  -p k1:=1.0 \
  -p k2:=3.0 \
  -p k3:=2.0 \
  -p disturbance:=true \
  -p dist_type:='sinus'
```

### Available Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `mode` | string | `'8'` | Trajectory type: `'cercle'` (circle) or `'8'` (figure-8) |
| `duration` | float | `30.0` | Trajectory duration in seconds |
| `rate` | float | `100.0` | Control loop frequency in Hz |
| `k1` | float | `1.0` | Kanayama control gain (longitudinal error) |
| `k2` | float | `3.0` | Kanayama control gain (lateral error) |
| `k3` | float | `2.0` | Kanayama control gain (angular error) |
| `disturbance` | bool | `true` | Enable/disable disturbances |
| `dist_type` | string | `'sinus'` | Disturbance type: `'gauss'` or `'sinus'` |
| `sigma_v` | float | `0.1` | Disturbance magnitude for linear velocity |
| `sigma_w` | float | `0.2` | Disturbance magnitude for angular velocity |

### Example Configurations

**Circular trajectory without disturbance**:
```bash
ros2 run controller_node controller_node --ros-args \
  -p mode:='cercle' \
  -p duration:=20.0 \
  -p disturbance:=false
```

**Figure-8 with Gaussian noise**:
```bash
ros2 run controller_node controller_node --ros-args \
  -p mode:='8' \
  -p duration:=40.0 \
  -p dist_type:='gauss' \
  -p sigma_v:=0.05 \
  -p sigma_w:=0.1
```

**Aggressive control gains**:
```bash
ros2 run controller_node controller_node --ros-args \
  -p k1:=2.0 \
  -p k2:=5.0 \
  -p k3:=3.5
```

## Understanding the Controller

### Robust Adaptive Dynamic Controller

The controller implements a robust adaptive dynamic control approach for nonholonomic mobile robots, based on the work by Kim et al. (2004). This method is specifically designed to handle modeling uncertainties and disturbances, which is why the controller includes optional disturbance injection for robustness testing.

The controller computes velocity commands based on tracking errors in the robot's frame:

- **Longitudinal error** (`ex`): Distance ahead/behind reference
- **Lateral error** (`ey`): Perpendicular distance from reference
- **Angular error** (`etheta`): Orientation difference

Control laws:
```
v = vr * cos(etheta) + k1 * ex
w = wr + vr * (k2 * ey + k3 * sin(etheta))
```

Where:
- `vr`, `wr` are reference velocities
- `k1`, `k2`, `k3` are adaptive control gains
- The control law is robust to modeling uncertainties and external disturbances

### Safety Limits

The controller enforces TurtleBot4 hardware limits:
- **Linear velocity**: [-0.3, 0.3] m/s
- **Angular velocity**: [-1.5, 1.5] rad/s

## Visualization

The controller opens a matplotlib window showing:
- **Red dashed line**: Reference trajectory
- **Blue solid line**: Actual robot path
- Real-time updates every 5 control cycles

The plot automatically displays when the trajectory is complete.

## Troubleshooting

### Issue: Robot doesn't move in Gazebo

**Solution**: Check that the controller is publishing commands:
```bash
ros2 topic echo /cmd_vel
```

### Issue: Matplotlib window doesn't appear

**Solution**: Ensure you have a display server running and matplotlib is properly configured:
```bash
export DISPLAY=:0
```

### Issue: "Trajectoire terminée" message appears immediately

**Solution**: The duration might be too short, or the timer is not working. Check ROS2 clock:
```bash
ros2 topic echo /clock
```

### Issue: Controller crashes with import errors

**Solution**: Reinstall dependencies:
```bash
pip3 install --user numpy matplotlib
```

### Issue: TurtleBot4 launches in wrong position

**Solution**: The initial pose is calculated from the trajectory. Ensure the trajectory starts at a valid position.

## Topics and Communication

### Published Topics

| Topic | Type | Description |
|-------|------|-------------|
| `/cmd_vel` | `geometry_msgs/TwistStamped` | Velocity commands for the robot |

### Subscribed Topics

None - The controller runs in open-loop with simulated state estimation.

## Project Structure

```
Kanayama-trajectory-controller/
├── src/
│   ├── controller_node/
│   │   ├── controller_node/
│   │   │   ├── __init__.py
│   │   │   └── controller_node.py      # Main controller implementation
│   │   ├── package.xml                 # Package dependencies
│   │   ├── setup.py                    # Python package setup
│   │   └── test/                       # Unit tests
│   └── turtlebot4_simulator/           # TurtleBot4 Gazebo packages
├── build/                              # Build artifacts
├── install/                            # Installed packages
└── log/                                # Build and runtime logs
```

## Advanced Usage

### Custom Trajectory Generation

To add a new trajectory pattern, modify `controller_node.py`:

1. Add a new mode in the trajectory generation section (around line 44)
2. Define `xr` and `yr` as numpy arrays for x and y positions over time
3. The controller will automatically compute velocities using numerical differentiation

Example:
```python
elif self.mode == 'square':
    # Define your custom trajectory here
    self.xr = custom_x_trajectory
    self.yr = custom_y_trajectory
```

### Tuning Control Gains

For optimal performance:
- Increase `k1` for faster convergence to the path
- Increase `k2` to reduce lateral error
- Increase `k3` for better orientation tracking
- Start with low gains and increase gradually to avoid oscillations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Authors

**Axel Renard** ([@renarddaxel312](https://github.com/renarddaxel312))
**Rayane Yettefti** ([@TeslaYet](https://github.com/TeslaYet))

## Acknowledgments

- TurtleBot4 team for the simulation packages
- ROS2 community for the excellent documentation
- Kim et al. for the robust adaptive dynamic controller methodology

## References

**For detailed academic references and citations, see [REFERENCES.md](REFERENCES.md)**

### Key References

- [TurtleBot4 Documentation](https://turtlebot.github.io/turtlebot4-user-manual/)
- [ROS2 Jazzy Documentation](https://docs.ros.org/en/jazzy/)
- Kim, M.-S., Shin, J.-H., Hong, S.-G., & Lee, J.-J. (2004). "Designing a robust adaptive dynamic controller for nonholonomic mobile robots under modeling uncertainty and disturbances." *Mechatronics*, 14(5), 481-495. DOI: [10.1016/j.mechatronics.2003.10.006](https://doi.org/10.1016/j.mechatronics.2003.10.006)
- Kanayama, Y., et al. (1990). "A stable tracking control method for an autonomous mobile robot." *IEEE International Conference on Robotics and Automation*.

## Support

For issues or questions:
- Open an [issue](https://github.com/renarddaxel312/Kanayama-trajectory-controller/issues) on GitHub
- Check ROS2 logs in the `log/` directory
- Review controller output in the terminal
- Check Gazebo console for simulation errors

---

**Last Updated**: November 3, 2025
