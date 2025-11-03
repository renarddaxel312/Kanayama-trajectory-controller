# Academic References

## Primary Reference

This implementation is based on the following research paper:

### Main Paper

**Kim, M.-S., Shin, J.-H., Hong, S.-G., & Lee, J.-J. (2004)**  
*Designing a robust adaptive dynamic controller for nonholonomic mobile robots under modeling uncertainty and disturbances.*  
**Mechatronics**, 14(5), 481-495.  
DOI: [10.1016/j.mechatronics.2003.10.006](https://doi.org/10.1016/j.mechatronics.2003.10.006)

**Abstract**: The paper presents a robust adaptive dynamic controller for trajectory tracking of nonholonomic mobile robots. The controller is designed to handle modeling uncertainties and external disturbances, which are common in real-world robotics applications.

**Key Contributions**:
- Robust control approach for nonholonomic mobile robots
- Adaptive mechanisms to handle parameter uncertainties
- Dynamic control framework accounting for robot dynamics
- Proven stability under disturbances and modeling errors

**Authors**:
- Min-Soeng Kim - Department of Computer Science and Electrical Engineering, KAIST
- Jin-Ho Shin - Department of Mechatronics Engineering, Dong-eui University
- Sun-Gi Hong - Department of Computer Science and Electrical Engineering, KAIST
- Ju-Jang Lee - Department of Computer Science and Electrical Engineering, KAIST

**Received**: 1 December 2000  
**Accepted**: 5 November 2001

## Implementation Details

This project implements the trajectory tracking controller described in the above paper with the following adaptations:

1. **Robot Platform**: Adapted for TurtleBot4 in Gazebo simulation
2. **ROS2 Integration**: Implemented as a ROS2 node for easy integration
3. **Trajectory Types**: Supports circular and figure-8 trajectories
4. **Disturbance Testing**: Includes optional Gaussian and sinusoidal disturbances
5. **Real-time Visualization**: Added matplotlib visualization for trajectory tracking
6. **Safety Limits**: Enforces TurtleBot4 hardware velocity constraints

## Control Law

The control law implemented follows the general form:

```
v = vr * cos(e_θ) + k1 * ex
w = wr + vr * (k2 * ey + k3 * sin(e_θ))
```

Where:
- `v`, `w` are the commanded linear and angular velocities
- `vr`, `wr` are the reference velocities from the desired trajectory
- `ex`, `ey`, `e_θ` are the tracking errors in the robot's frame
- `k1`, `k2`, `k3` are the adaptive control gains

## Additional References

### Related Work

1. **Kanayama, Y., Kimura, Y., Miyazaki, F., & Noguchi, T. (1990)**  
   *A stable tracking control method for an autonomous mobile robot.*  
   IEEE International Conference on Robotics and Automation, 384-389.  
   (Foundational work on trajectory tracking for nonholonomic robots)

2. **TurtleBot4 Documentation**  
   [https://turtlebot.github.io/turtlebot4-user-manual/](https://turtlebot.github.io/turtlebot4-user-manual/)  
   (Robot platform specifications and simulation setup)

3. **ROS2 Jazzy Documentation**  
   [https://docs.ros.org/en/jazzy/](https://docs.ros.org/en/jazzy/)  
   (Framework documentation)

## Citation

If you use this implementation in your research, please cite both the original paper and this software:

### BibTeX - Original Paper

```bibtex
@article{kim2004designing,
  title={Designing a robust adaptive dynamic controller for nonholonomic mobile robots under modeling uncertainty and disturbances},
  author={Kim, Min-Soeng and Shin, Jin-Ho and Hong, Sun-Gi and Lee, Ju-Jang},
  journal={Mechatronics},
  volume={14},
  number={5},
  pages={481--495},
  year={2004},
  publisher={Elsevier},
  doi={10.1016/j.mechatronics.2003.10.006}
}
```

### BibTeX - This Software

```bibtex
@software{renard2025turtlebot4_controller,
  author = {Renard, Axel},
  title = {TurtleBot4 Robust Adaptive Dynamic Controller},
  year = {2025},
  url = {https://github.com/renarddaxel312/Kanayama-trajectory-controller},
  version = {1.0.0},
  license = {MIT}
}
```

## Contact

For questions about this implementation, please open an issue on the [GitHub repository](https://github.com/renarddaxel312/Kanayama-trajectory-controller/issues).

For questions about the original research, please contact the authors through their institutions or refer to the published paper.

---

**Note**: This is an educational implementation for research and learning purposes. For production robotics applications, additional safety measures and validation should be performed.

