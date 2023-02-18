# Internal imports
from robot_core import BasicTankDrive

# Third-party imports
import commands2
import wpilib


class RobotRunner(commands2.TimedCommandRobot):
    def robotInit(self):
        self.timer = wpilib.Timer()
        self.timer.start()

        self.robot_shell = BasicTankDrive()

    def disabledInit(self) -> None:
        self.robot_shell.disabledInit()

    def disabledExit(self) -> None:
        self.robot_shell.disabledExit()

    def autonomousInit(self) -> None:
        self.timer.reset()
        self.robot_shell.autonomousInit()

    def autonomousPeriodic(self) -> None:
        self.robot_shell.autonomousPeriodic()

    def teleopInit(self) -> None:
        self.robot_shell.teleopInit()

    def teleopPeriodic(self) -> None:
        self.robot_shell.teleopPeriodic()

    def testInit(self) -> None:
        commands2.CommandScheduler.getInstance().cancelAll()
        self.robot_shell.testInit()

    def testPeriodic(self) -> None:
        self.robot_shell.testPeriodic()

if __name__ == "__main__":
    wpilib.run(RobotRunner)
