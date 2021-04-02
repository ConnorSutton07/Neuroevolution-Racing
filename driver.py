import sys
from core.ui import ui
from core import settings
#from core.track import Track
#from core.engine import Engine

class Driver():
    def __init__(self, debug: bool = False) -> None:
        self.debug = debug
        #self.engine = Engine()
        #self.Track = Track()#type="perlin")
        #self.Track.plot()
        print()
        print("     +" + "-"*21 + "+")
        print("      NEUROEVOLUTION RACING")
        print("     +" + "-"*21 + "+")
        print()

    def run(self) -> None:
        modes = [
                ("Player vs AI", self._playerVsAI),
                ("AI Battle", self._playAI),
                ("Evolve AI", self._evolveAI),
                ("Exit", lambda: sys.exit())
        ]

        ui.runModes(modes)

    def _playerVsAI(self) -> None:
        print("Not implemented!")
        sys.exit()

    def _playAI(self) -> None:
        print("Not implemented!")
        sys.exit()

    def _evolveAI(self) -> None:
        print("not implemented")
        sys.exit()

    # def run(self) -> None:
    #     while True:
    #         for object in self.gameObjects:
    #             track_edges = self.Track.getTrack()
    #             left_edges = track_edges[0]
    #             right_edges = track_edges[1]
    #             self.engine.renderLines(left_edges, 10)
    #             self.engine.renderLines(right_edges, 10)


