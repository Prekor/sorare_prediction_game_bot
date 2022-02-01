

class DiscordParser:
    def __init__(self, ctx):
        self.ctx = ctx

    def get_message_without_command(self):
        message: list[str] = []
        for line in self.ctx.message.content.splitlines():
            if line[0] == "!":
                continue
            else:
                message.append(line)
        return message
