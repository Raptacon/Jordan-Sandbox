import commands2
import math
import wpilib
import wpimath._controls._controls.trajectory
import wpimath.controller as wpic
import wpimath.trajectory as wpit


class Arm(commands2.ProfiledPIDSubsystem):
    """
    A robot arm moving according to the trapezoid profile

    Trapezoid profile: accelerate to a max velocity,
    hold that velocity for a period of time, then
    decelerate to a velocity of zero.
    See https://www.linearmotiontips.com/how-to-calculate-velocity/

    Feedforward control: leverage an equation to estimate
    control input required to reach desired output.
    Will be constrained using a motion profile.
    See https://docs.wpilib.org/en/stable/docs/software/advanced-controls/introduction/introduction-to-feedforward.html#introduction-to-dc-motor-feedforward
    """

    ARM_STARTING_OFFSET = 0.5 #radians

    def __init__(self) -> None:
        MOTOR_PORT = 5
        
        COUNTS_PER_REV = 256
        ROTATION_DIAMETER = 2 #inches
        pulse_to_dist = (ROTATION_DIAMETER * math.pi) / COUNTS_PER_REV

        # Instantiate class derivative with a basic PID
        # controller contrained with a trapezoidal
        # motion profile
        super().__init__(
            wpic.ProfiledPIDController(
                1, # p coeff
                0, # i coeff
                0, # d coeff
                wpit.TrapezoidProfile.Constraints(
                    3, # max velocity in radps
                    10 # max accel in radps**2
                ),
                20 # update every 20 ms
            )
        )

        # Instantiate motor and encoder with ports
        self.motor = wpilib.PWMMotorController("arm", MOTOR_PORT)
        self.encoder = wpilib.Encoder(MOTOR_PORT, MOTOR_PORT + 1)

        # Instantiate arm motion voltage coverter
        # based on feedforward control
        self.feedforward_converter = wpic.ArmFeedforward(
            1, #kS, voltage to just pass static friction
            1, #kG, voltage to just push past gravity
            0.5, #kV, vspr to hit a desired velocity
            1 #kA, vs**2pr to hit a desired acceleration
        )

        # Specify conversion factor between encoder pulses
        # and distance traveled
        self.encoder.setDistancePerPulse(pulse_to_dist)

        # Set the starting position of the arm in radians
        self.setGoal(self.ARM_STARTING_OFFSET)

    def _useOutput(self, pid_out_voltage: float, setpoint: wpit.TrapezoidProfile.State) -> None:
        """
        Calculate the feedforward voltage requried to hit
        a given setpoint and combine with PID voltage to
        update the voltage on the arm's motor
        """
        feedforward_voltage = self.feedforward_converter.calculate(
            setpoint.position, setpoint.velocity
        )

        self.motor.setVoltage(pid_out_voltage + feedforward_voltage)

    def _getMeasurement(self) -> float:
        """
        Get the total offset distance from zero using the
        distance calculated from the encoder combined
        with the known starting offset. Distance in radians
        """
        return self.encoder.getDistance() + self.ARM_STARTING_OFFSET
