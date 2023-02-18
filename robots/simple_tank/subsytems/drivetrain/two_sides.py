import commands2
import wpilib.drive


class TwoSidedLinearDrivetrain(commands2.SubsystemBase):
    def __init__(self, left_side, right_side):
        super().__init__()

        self.left_motors = left_side
        self.right_motors = right_side

        self.drivetrain = wpilib.drive.DifferentialDrive(
            self.left_motors, self.right_motors
        )

    def drive(self, left_speed, right_speed):
        self.drivetrain.tankDrive(left_speed, right_speed)
