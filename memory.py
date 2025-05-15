class Memory:
    def __init__(self):
        self.progress = {}

    def update(self, user_id, stage, item):
        self.progress.setdefault(user_id, {}).setdefault(stage, set()).add(item)

    def get_known(self, user_id, stage):
        return list(self.progress.get(user_id, {}).get(stage, []))
