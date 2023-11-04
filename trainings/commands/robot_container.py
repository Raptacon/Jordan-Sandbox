import commands2
import commands2.button as cb
import commands2.cmd as cc

from subsystems.arm import Arm
from subsystems.drivetrain import DriveTrain

class RobotContainer:
    """
    This instantiates the structure of the robot and will
    be directly fed into the robot.py script. Can
    analogously think of this class as the query
    and the robot.py file as the query executor.
    """

    def __init__(self) -> None:
        # Instantiate robot subsystems
        self.subsystems = {
            "drivetrain": DriveTrain(),
            "arm": Arm()
        }

        # Instantiate controller plugged into drive station
        self.driver_controller = cb.CommandPS4Controller(0)

        # Bind controller inputs to robot actions
        self.configureButtonBindings()

        # Make arcade driving the default command to
        # run on the drivetrain subsystem
        self.subsystems["drivetrain"].setDefaultCommand(
            cc.run(
                lambda: self.subsystems["drivetrain"].arcadeDrive(
                    -self.driver_controller.getLeftY(),
                    -self.driver_controller.getRightX()
                ),
                [self.subsystems["drivetrain"]]
            )
        )

    def configureButtonBindings(self) -> None:
        """
        Map controller inputs to command actions
        """
        
        # Map A button to moving arm to the 2 radians position
        self.driver_controller.circle().onTrue(
            cc.run(lambda: self.moveArm(2), [self.subsystems["arm"]])
        )

        # Map B button to moving arm back to starting position
        self.driver_controller.triangle().onTrue(
            cc.run(
                lambda: self.moveArm(self.subsystems["arm"].ARM_STARTING_OFFSET),
                [self.subsystems["arm"]]
            )
        )

        # Map Y button to disabling arm
        self.driver_controller.square().onTrue(
            cc.runOnce(lambda: self.subsystems["arm"].disable())
        )

        # Constrain max drive speed to half when holding down right trigger
        self.driver_controller.R2().onTrue(
            cc.runOnce(lambda: self.subsystems["drivetrain"].setMaxOutput(0.5))
        )
        self.driver_controller.R2().onFalse(
            cc.runOnce(lambda: self.subsystems["drivetrain"].setMaxOutput(1.0))
        )

    def disablePIDSubsystems(self) -> None:
        """
        Disable the robot arm
        """
        self.subsystems["arm"].disable()
    
    def getAutonomousCommand(self) -> commands2.Command:
        """
        Retrieve the command to use during autonomous
        """
        return cc.nothing()
    
    def moveArm(self, radians: int) -> None:
        """
        Move arm to the specified radians position
        """
        self.subsystems["arm"].setGoal(radians)
        self.subsystems["arm"].enable()
