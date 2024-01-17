class ExpectedPageNotFound(Exception):
    """Custom exception for indicating that an expected page was not found."""

    def __init__(self, message="Expected page not found"):
        self.message = message
        super().__init__(self.message)
