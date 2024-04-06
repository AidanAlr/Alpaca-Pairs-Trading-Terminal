class NoSuitablePairsError(Exception):
    """Raised when no suitable pairs are found"""
    def __init__(self):
        # Pass the message to the base Exception class
        super().__init__("NoSuitablePairsError: No suitable pairs found, try again with a different ticker list.")
