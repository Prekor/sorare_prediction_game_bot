

class DiscordParser:
    def __init__(self, ctx, message):
        self.ctx = ctx
        self.message = message.splitlines()
