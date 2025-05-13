# Screen settings
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 640
FPS = 60  # Frames per second


# Game settings
TITLE = "MyGame"


# Player settings
PLAYER_SPEED = 4
PLAYER_START_X = 10
PLAYER_START_Y = 10
PLAYER_BULLETS = 6
PLAYER_FIRE_COOLDOWN = 1000  # Oyuncunun ateş etme bekleme süresi (ms)
PLAYER_BULLET_SPEED = 6  # Oyuncu mermisinin hızı
PLAYER_HEALTH = 1000  # Oyuncunun başlangıç canı

# Enemy settings
ENEMY_SPEED = 1
ENEMY_BULLETS = 6
ENEMY_HEALTH = 300  # Düşmanın canı
ENEMY_DETECTION_RANGE = 300  # Düşmanın oyuncuyu tespit edebileceği mesafe
ENEMY_FIRE_RANGE = 200  # Düşmanın ateş edebileceği mesafe
ENEMY_FIRE_COOLDOWN = 2000  # Düşmanın ateş etme bekleme süresi (ms)
ENEMY_DAMAGE = 10  # Düşmanın her mermide verdiği hasar
ENEMY_VERTICAL_THRESHOLD = 20  # Düşmanın ateş etmek için oyuncuya y ekseninde olması gereken maksimum mesafe
ENEMY_COUNT = 3  # Başlangıçtaki düşman sayısı
ENEMY_MIN_DISTANCE = 400  # Düşmanlar arası minimum mesafe

# Bullet settings
BULLET_MAX_DISTANCE = 250  # Merminin en fazla gidebileceği mesafe

# Death animation speed (for both player and enemy)
DEATH_ANIMATION_SPEED = 0.2

SPRITE_SCALE = 1.75  # Sprite ölçek oranı (1: orijinal, 2: iki katı, 3: üç katı)
