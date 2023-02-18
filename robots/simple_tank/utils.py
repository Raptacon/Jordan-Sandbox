import wpimath

def getStick(controller, axis, invert=False):
    sign = -1.0 if invert else 1.0
    slew = wpimath.filter.SlewRateLimiter(3)
    return lambda: slew.calculate(
        wpimath.applyDeadband(
            sign * controller.getRawAxis(axis), 0.1
        )
    )