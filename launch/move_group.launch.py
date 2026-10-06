from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_move_group_launch


def generate_launch_description():
    # MoveIt's move_group: planning, IK and execution through arm_controller and
    # gripper_controller. It needs the robot's /joint_states and the controllers' actions, so it
    # can run on any host on the same ROS domain whose clock is synchronized with the robot's.
    moveit_config = (
        MoveItConfigsBuilder('so101', package_name='so101_moveit_config')
        .planning_pipelines(pipelines=['ompl'])
        .to_moveit_configs()
    )
    return generate_move_group_launch(moveit_config)
