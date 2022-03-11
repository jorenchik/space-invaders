import pathlib as pl

# Enemies
absPath = pl.Path.cwd()
assets = pl.Path(absPath/'assets')
enemySprites = list(assets.glob("enemy_*.png"))

# Player
playerSprite = pl.Path(assets/"player_sprite.png")

# Fireball (Player's weapon)
fireballSprite = pl.Path(assets/"fireball_sprite.png")

# Ball (enemys' weapon)
ballSprite = pl.Path(assets/"ball.png")

# Hearth (indicator of lifes remaining)
heartSprite = pl.Path(assets/"heart.png")

bg = pl.Path(assets/"background.jpg")
