class CommandException(Exception):
    """
    Custom exception class for handling command-related errors. This exception
    allows for the inclusion of specific errors that can't be catched with
    ArgumentError and is used in ArgumentParserNoExit.  
    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)