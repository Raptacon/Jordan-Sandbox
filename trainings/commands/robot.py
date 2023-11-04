import commands2
import wpilib

from robot_container import RobotContainer

class CommandRobot(commands2.TimedCommandRobot):
    """
    A robot object built using the commands framework
    """
    autonomous_command = None

    def robotInit(self) -> None:
        self.container = RobotContainer()
    
    def robotPeriodic(self) -> None:
        commands2.CommandScheduler.getInstance().run()

    def disabledInit(self) -> None:
        self.container.disablePIDSubsystems()

    def autonomousInit(self) -> None:
        self.autonomous_command = self.container.getAutonomousCommand()

        if self.autonomous_command:
            self.autonomous_command.schedule()
    
    def teleopInit(self) -> None:
        # Kill running autonomous commands
        if self.autonomous_command:
            self.autonomous_command.cancel()

    def testInit(self) -> None:
        # Kill all running commands
        commands2.CommandScheduler.getInstance().cancelAll()
    

if __name__ == "__main__":
    wpilib.run(CommandRobot)
