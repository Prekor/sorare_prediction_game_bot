from manager import Manager

from discord_parser.discord_parser import DiscordParser


class ManagerParser(DiscordParser):
    def __init__(self, ctx):
        super().__init__(ctx)

    def get_manager(self):
        return Manager(self.ctx.author)
