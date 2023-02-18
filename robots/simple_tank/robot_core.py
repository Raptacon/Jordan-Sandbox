# Internal imports
import utils

from commands.motion.drive_tank import TankDrive
from subsytems.drivetrain.two_sides import TwoSidedLinearDrivetrain

# Third-party imports
import commands2
import ctre
import wpilib

motor_config = {
    "FL": {
        "side": "left",
        "port": 10
    },
    "FR": {
        "side": "right",
        "port": 11
    },
    "BL": {
        "side": "left",
        "port": 12
    },
    "BR": {
        "side": "right",
        "port": 13
    }
}


class BasicTankDrive(commands2.TimedCommandRobot):
    def __init__(self, period=0.02):
        super().__init__(period)

        self.subsystems = dict()
        self.commands = dict()

        motors = {
            motor_id: ctre.WPI_TalonFX(motor_spec["port"])
            for motor_id, motor_spec in motor_config.items()
        }

        motor_groups = dict()
        for motor_id, motor in motors.items():
            motor_side = motor_config[motor_id]["side"]
            if motor_side in motor_groups:
                motor_groups[motor_side].append(motor)
            else:
                motor_groups[motor_side] = [motor]
        
        self.motor_groups = {
            motor_side: wpilib.MotorControllerGroup(*motor_group)
            for motor_side, motor_group in motor_groups.items()
        }

        self.subsystems["drivetrain"] = TwoSidedLinearDrivetrain(
            motor_groups["left"], motor_groups["right"]
        )

        self.commands["tank_drive"] = TankDrive(
            utils.getStick(wpilib.XboxController.Axis.kRightY, True),
            utils.getStick(wpilib.XboxController.Axis.kLeftY, False),
            self.subsystems["drivetrain"]
        )

    def teleopInit(self):
        if "drivetrain" in self.subsystems:
            self.subsystems["drivetrain"] \
                .setDefaultCommand(self.commands["tank_drive"])
