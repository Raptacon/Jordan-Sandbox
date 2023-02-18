import commands2


def get_speed_transform(current_time):
    if current_time < 0.5:
        return 0
    if current_time < 2.5:
        return 1
    if current_time < 4.5:
        return 0
    if current_time < 6.5:
        return -1
    return 0


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

        speed_transform = get_speed_transform(current_time)
        auto_speed = self.speed * speed_transform

        self.drivetrain.drive(
            auto_speed, auto_speed
        )

    def end(self, interrupted=False):
        self.drivetrain.drive(0, 0)

    def isFinished(self):
        return False
    