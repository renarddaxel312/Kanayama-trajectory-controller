#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped
import numpy as np
import matplotlib.pyplot as plt

class TrajectoryFollower(Node):
    def __init__(self):
        super().__init__('trajectory_follower')

        # === Paramètres ROS ===
        self.declare_parameter('mode', '8')
        self.declare_parameter('duration', 30.0)
        self.declare_parameter('rate', 100.0)
        self.declare_parameter('k1', 1.0)
        self.declare_parameter('k2', 3.0)
        self.declare_parameter('k3', 2.0)
        self.declare_parameter('disturbance', True)
        self.declare_parameter('dist_type', 'sinus')
        self.declare_parameter('sigma_v', 0.1)
        self.declare_parameter('sigma_w', 0.2)

        # === Lecture des paramètres ===
        self.mode = self.get_parameter('mode').value
        self.duration = self.get_parameter('duration').value
        self.dt = 1.0 / self.get_parameter('rate').value
        self.k1 = self.get_parameter('k1').value
        self.k2 = self.get_parameter('k2').value
        self.k3 = self.get_parameter('k3').value
        self.use_disturbance = self.get_parameter('disturbance').value
        self.disturbance_type = self.get_parameter('dist_type').value
        self.sigma_v = self.get_parameter('sigma_v').value
        self.sigma_w = self.get_parameter('sigma_w').value

        # === Publisher TwistStamped ===
        self.cmd_pub = self.create_publisher(TwistStamped, '/cmd_vel', 10)
        self.timer = self.create_timer(self.dt, self.control_loop)

        # === Trajectoire de référence ===
        self.T = np.arange(0, self.duration, self.dt)
        self.omega_t = 2 * np.pi / self.duration

        if self.mode == 'cercle':
            R = 1.0
            self.xr = R * np.cos(self.omega_t * self.T)
            self.yr = R * np.sin(self.omega_t * self.T)
        elif self.mode == '8':
            A, B = 1.0, 0.5
            self.xr = A * np.sin(self.omega_t * self.T)
            self.yr = B * np.sin(2 * self.omega_t * self.T)
        else:
            raise ValueError("Mode inconnu : 'cercle' ou '8'")

        self.dxr = np.gradient(self.xr, self.dt)
        self.dyr = np.gradient(self.yr, self.dt)
        self.vr = np.sqrt(self.dxr**2 + self.dyr**2)
        self.wr = np.gradient(np.arctan2(self.dyr, self.dxr), self.dt)

        # === État initial ===
        self.t = 0.0
        self.x = float(self.xr[0])
        self.y = float(self.yr[0])
        self.theta = float(np.arctan2(self.dyr[0], self.dxr[0]))
        self.X, self.Y = [self.x], [self.y]

        self.get_logger().info(f"Contrôleur lancé en mode '{self.mode}' pour {self.duration}s")

        # === Graphique temps réel ===
        plt.ion()
        self.fig, self.ax = plt.subplots(figsize=(7, 6))
        self.line_ref, = self.ax.plot(self.xr, self.yr, 'r--', label='Référence')
        self.line_bot, = self.ax.plot(self.X, self.Y, 'b', label='Robot')
        self.ax.set_title(f"Suivi de trajectoire ({self.mode})")
        self.ax.set_xlabel("x [m]")
        self.ax.set_ylabel("y [m]")
        self.ax.axis('equal')
        self.ax.grid(True)
        self.ax.legend()
        plt.show(block=False)

    def control_loop(self):
        i = int(self.t / self.dt)
        if i >= len(self.T):
            self.get_logger().info("Trajectoire terminée.")
            plt.ioff()
            plt.show()
            self.destroy_timer(self.timer)
            return

        # === Erreurs dans le repère robot ===
        ex = np.cos(self.theta) * (self.xr[i] - self.x) + np.sin(self.theta) * (self.yr[i] - self.y)
        ey = -np.sin(self.theta) * (self.xr[i] - self.x) + np.cos(self.theta) * (self.yr[i] - self.y)
        etheta = np.arctan2(np.sin(np.arctan2(self.dyr[i], self.dxr[i]) - self.theta),
                            np.cos(np.arctan2(self.dyr[i], self.dxr[i]) - self.theta))

        # === Commande Kanayama ===
        v = self.vr[i] * np.cos(etheta) + self.k1 * ex
        w = self.wr[i] + self.vr[i] * (self.k2 * ey + self.k3 * np.sin(etheta))

        # === Perturbations ===
        if self.use_disturbance:
            if self.disturbance_type == "gauss":
                v += np.random.normal(0, self.sigma_v)
                w += np.random.normal(0, self.sigma_w)
            elif self.disturbance_type == "sinus":
                v += self.sigma_v * np.sin(2 * np.pi * 0.5 * self.t)
                w += self.sigma_w * np.sin(2 * np.pi * 0.3 * self.t)

        # === Limites de sécurité TurtleBot4 ===
        v = np.clip(v, -0.3, 0.3)     # vitesse linéaire max 0.3 m/s
        w = np.clip(w, -1.5, 1.5)     # vitesse angulaire max 1.5 rad/s

        # === Publier TwistStamped ===
        msg = TwistStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "base_link"
        msg.twist.linear.x = float(v)
        msg.twist.angular.z = float(w)
        self.cmd_pub.publish(msg)

        # === Mise à jour simulation ===
        self.x += v * np.cos(self.theta) * self.dt
        self.y += v * np.sin(self.theta) * self.dt
        self.theta += w * self.dt
        self.t += self.dt

        self.X.append(self.x)
        self.Y.append(self.y)

        # === Mise à jour du graphique ===
        if i % 5 == 0:
            self.line_bot.set_data(self.X, self.Y)
            self.ax.relim()
            self.ax.autoscale_view()
            plt.pause(0.001)

def main(args=None):
    rclpy.init(args=args)
    node = TrajectoryFollower()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()
    plt.ioff()
    plt.show()

if __name__ == '__main__':
    main()
