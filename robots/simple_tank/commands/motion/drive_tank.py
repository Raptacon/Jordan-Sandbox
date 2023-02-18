import commands2


class TankDrive(commands2.CommandBase):
    def __init__(self, left_input, right_input, drivetrain):
        super().__init__()

        self.left_input = left_input
        self.right_input = right_input
        self.drivetrain = drivetrain

        self.addRequirements(self.drivetrain)

    def execute(self):
        self.drivetrain.drive(
            self.left_input(), self.right_input()
        )

    def end(self, interrupted):
        self.drivetrain.drive(0, 0)

    def isFinished(self):
        return False
