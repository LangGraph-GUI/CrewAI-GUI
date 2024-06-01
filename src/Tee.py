import sys
import datetime

class Tee:
    def __init__(self, filename, mode='a'):  # Use 'a' for append mode
        self.file = open(filename, mode)
        self.stdout = sys.stdout
        sys.stdout = self

    def write(self, message):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message_with_timestamp = f"{timestamp} - {message}"
        self.stdout.write("\n")
        self.stdout.write(message_with_timestamp)
        self.file.write(message_with_timestamp)
        self.file.flush()

    def flush(self):
        self.stdout.flush()
        self.file.flush()

    def close(self):
        sys.stdout = self.stdout
        self.file.close()
