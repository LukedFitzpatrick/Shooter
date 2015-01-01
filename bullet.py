class Bullet:
    def __init__(self, sprite, xStart, yStart, xVStart, yVStart, alive):
        self.sprite = sprite
        self.x = xStart
        self.y = yStart
        self.xV = xVStart
        self.yV = yVStart
        self.alive = alive
   