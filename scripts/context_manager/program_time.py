from datetime import datetime


class ProgramExecutionTime:
    def __enter__(self):
        self.start_time = datetime.now()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.time_of_program = datetime.now() - self.start_time
