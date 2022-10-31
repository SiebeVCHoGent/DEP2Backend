class DBException(Exception):
    def __init__(self, message="Database error"):
        self.message = message
        super().__init__(self.message)