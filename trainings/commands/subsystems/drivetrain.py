import commands2
import math
import wpilib
import wpilib.drive as wpid


class DriveTrain(commands2.SubsystemBase):
    """
    A drivetrain subsystem for mobilizing the robot
    """

    def __init__(self) -> None:
        super().__init__()

        MOTOR_PORTS = [1, 2, 3, 4]

        COUNTS_PER_REV = 1024
        WHEEL_DIAMETER = 6 #inches
        pulse_to_dist = (WHEEL_DIAMETER * math.pi) / COUNTS_PER_REV

        # Group together motors on left side of bot
        self.left_motors = wpilib.MotorControllerGroup(
            wpilib.PWMMotorController("lu_wheel", MOTOR_PORTS[0]),
            wpilib.PWMMotorController("ll_wheel", MOTOR_PORTS[1])
        )

        # Group together motors on right side of bot
        self.right_motors = wpilib.MotorControllerGroup(
            wpilib.PWMMotorController("ru_wheel", MOTOR_PORTS[2]),
            wpilib.PWMMotorController("rl_wheel", MOTOR_PORTS[3])
        )

        # Setup up drive functionality on motors
        self.drive = wpid.DifferentialDrive(
            self.left_motors, self.right_motors
        )

        # Instantiate drive-side encoders
        self.left_encoder = wpilib.Encoder(
            MOTOR_PORTS[0], MOTOR_PORTS[1], False
        )
        self.right_encoder = wpilib.Encoder(
            MOTOR_PORTS[2], MOTOR_PORTS[3], True
        )

        # Specify conversion factor between encoder pulses
        # and distance traveled
        self.left_encoder.setDistancePerPulse(pulse_to_dist)
        self.right_encoder.setDistancePerPulse(pulse_to_dist)

        # Invert one side to ensure uniform directionality
        # given a positive voltage applied
        self.right_motors.setInverted(True)

    def arcadeDrive(self, speed: float, rotation: float) -> None:
        """
        Operate the robot using standard arcade drive
        """
        self.drive.arcadeDrive(speed, rotation)

    def resetEncoders(self) -> None:
        """
        Return encodings to starting position of 0
        """
        self.left_encoder.reset()
        self.right_encoder.reset()

    def getAverageEncoderDistance(self) -> float:
        """
        Get average distance traversed between the 
        encoders on each side of the bot
        """
        avg_dist = (
            self.left_encoder.getDistance() + self.right_encoder.getDistance()
        ) / 2.0

        return avg_dist

    def setMaxOutput(self, max_output: float) -> None:
        """
        Set max output drivetrain can produce
        """
        self.drive.setMaxOutput(max_output)
