from mandelbrothers import *
import asyncio

async def run(game):
        # game loop
        game.playing = True
        while game.playing:
            game.dt = game.clock.tick(FPS) / 1000
            game.events()
            if game.on_main_menu:
                game.main_menu()
            else:
                if not (game.paused or game.game_over) and (not game.win or game.interact):
                    game.update()
                game.drawScreen()
            await asyncio.sleep(0)

async def main():
        while True:
                game = Game()
                await run(game)