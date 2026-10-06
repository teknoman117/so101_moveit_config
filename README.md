# so101_moveit_config

MoveIt 2 configuration for the SO-101 follower arm (`so101_description`), using the controllers in
`so101_description/config/so101_controllers.yaml`.

## Launch files

| Launch | Starts |
|---|---|
| `demo.launch.py` | the arm's ros2_control stack (`so101_description/hardware_control.launch.py`, mock hardware by default), `move_group`, RViz |
| `move_group.launch.py` | `move_group` only |
| `moveit_rviz.launch.py` | RViz with the MotionPlanning panel only |

```bash
# everything on one host, mock hardware
ros2 launch so101_moveit_config demo.launch.py
# real arm
ros2 launch so101_moveit_config demo.launch.py use_mock_hardware:=false port:=/dev/ttyACM0
```

Split across hosts: run `so101_description hardware_control.launch.py` on the robot, and
`move_group.launch.py` and `moveit_rviz.launch.py` on a workstation on the same `ROS_DOMAIN_ID`.
The host that runs move_group needs a clock synchronized with the robot's: before it executes a
trajectory, MoveIt waits up to 1 s for a `/joint_states` message stamped at or after its own
current time. Without clock sync, run move_group on the robot.

## Planning groups

The arm has 5 joints, so a 6-DOF pose goal is reachable only for some orientations: for each
gripper position, the approach direction must lie in the vertical plane through the
`shoulder_pan` axis. There are two groups for the same joints, with different IK settings
(`config/kinematics.yaml`, pick_ik):

| Group | IK | Use for |
|---|---|---|
| `arm` | full pose, 1 mm / 0.05 rad | pose goals whose orientation is reachable, joint goals, named poses |
| `arm_position_only` | position only (`rotation_scale: 0`) | position goals, dragging the marker in RViz (the default group in `moveit.rviz`) |
| `gripper` | none (one joint) | `open`, `closed` |

Named poses: `zero` (arm), `open` and `closed` (gripper).

A pose goal on `arm` with an unreachable orientation fails to plan (OMPL "Unable to sample any
valid states for goal tree"). Use `arm_position_only`, or give the orientation constraint enough
tolerance to include a reachable orientation.

## Other configuration

- `config/so101.srdf`: groups, named poses, end effectors and the disabled collision pairs. Only
  links joined by a joint are disabled: the zero pose is otherwise collision-free, and each other
  pair collided in some of 2000 random poses.
- `config/joint_limits.yaml`: 2 rad/s and 4 rad/s² per joint for time parameterization, scaled by
  0.5 by default.
- `config/moveit_controllers.yaml`: `arm_controller` (FollowJointTrajectory) and
  `gripper_controller` (ParallelGripperCommand). `trajectory_execution.allowed_start_tolerance` is
  0.05 rad, looser than the default, for an arm that sags a little under load.
- `.setup_assistant`: lets the MoveIt Setup Assistant open this package
  (`ros2 launch moveit_setup_assistant setup_assistant.launch.py`).
