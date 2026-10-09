import datetime

class CleaningHistoryTracker:
    def __init__(self):
        self.logs = []

    def log(self, action: str, details: str):
        self.logs.append({
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "action": action,
            "details": details
        })

    def get_logs(self):
        return self.logs
