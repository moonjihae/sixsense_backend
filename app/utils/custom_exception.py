
class CustomUserError(Exception):
    status_code=500
    def __init__(self, status_code, error_message):
        super().__init__()
        self.error_message = error_message

        if status_code is not None:
            self.status_code = status_code
    def to_dict(self):
        rv=dict()
        rv['message']=self.error_message
        return rv


