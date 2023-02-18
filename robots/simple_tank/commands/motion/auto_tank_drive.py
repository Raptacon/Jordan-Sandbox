import commands2

class AutoTankDrive(commands2.CommandBase):
    def __init__(self, speed, timer, drivetrain):
        super().__init__()

        self.speed = speed
        self.timer = timer
        self.drivetrain = drivetrain

        self.addRequirements(self.drivetrain)

    def execute(self):
        current_time = self.timer.get()
        auto_speed = self.speed
        if (current_time > 2) and (current_time < 4):
            auto_speed = -1 * self.speed
        if current_time >= 4:
            auto_speed = 0
        self.drivetrain.drive(
            auto_speed, auto_speed
        )

    def end(self, interrupted=False):
        self.drivetrain.drive(0, 0)

    def isFinished(self):
        current_time = self.timer.get()
        if current_time >= 4:
            return True
        return False
    