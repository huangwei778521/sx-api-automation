from threading import Thread


class CustomThread(Thread):
    def __init__(self, func, args):
        super(CustomThread, self).__init__()
        self.func = func
        self.args = args
        self.result = None

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception as e:
            return None
