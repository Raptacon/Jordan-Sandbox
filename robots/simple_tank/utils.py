import wpilib
import wpimath

def getStick(axis, invert=False, port=0):
    sign = -1.0 if invert else 1.0
    slew = wpimath.filter.SlewRateLimiter(3)
    return lambda: slew.calculate(
        wpimath.applyDeadband(
            sign * wpilib.XboxController(port).getRawAxis(axis), 0.1
        )
    )