from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_moveit_rviz_launch


def generate_launch_description():
    # RViz with the MotionPlanning panel. It talks to a running move_group, so it can run on a
    # workstation while move_group and the hardware run elsewhere.
    moveit_config = (
        MoveItConfigsBuilder('so101', package_name='so101_moveit_config')
        .planning_pipelines(pipelines=['ompl'])
        .to_moveit_configs()
    )
    return generate_moveit_rviz_launch(moveit_config)
