class ControlGroup:
    """
    The interarrivalTime determines for how long the control group will have
    time out, that is when they will not send any packets.
    On keeps count of how many milliseconds that have passed since
    the beginning of the last time out.
    When on exceeds the interarrivalTime, the control group will start
    sending packets again for as long as the interarrivalTime. Then the control
    group will have another time out.
    """
    def __init__(self):
        self.interarrivalTime = 100
        self.on = 1
