
class Editable:
    def __init__(self):
        self.editing: bool = False

    def start_editing(self):
        self.editing = True

    def stop_editing(self):
        self.editing = False