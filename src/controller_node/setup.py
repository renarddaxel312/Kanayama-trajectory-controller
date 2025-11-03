from setuptools import find_packages, setup

package_name = 'controller_node'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'numpy', 'matplotlib', 'rclpy', 'geometry_msgs'],
    zip_safe=True,
    maintainer='Axel Renard',
    maintainer_email='axel@todo.todo',
    description='Robust adaptive dynamic trajectory tracking controller for TurtleBot4 based on Kim et al. (2004)',
    license='MIT',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'controller_node = controller_node.controller_node:main',
        ],
    },

)
