from board import Board
from host import Host


class Router_interface(Host):
    def __init__(self, rect, mac, router, if_id):
        super().__init__(rect, mac)
        self.router = router
        self.id = if_id
    def dragged(self, pos, button):
        pass
    def receive(self, packet, board:Board):
        board[self.router].receive(packet,board, self.id)