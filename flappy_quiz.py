import pygame
import sys
import random
import math

# Pygame başlat
pygame.init()

# Ekran boyutları
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Quiz - GençTek'li")

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (100, 150, 250)
DARK_BLUE = (20, 40, 100)
ORANGE = (255, 100, 0)
PURPLE = (150, 0, 255)
CYAN = (0, 255, 255)
PINK = (255, 100, 150)
GRAY = (128, 128, 128)

# Araba renkleri
CAR_COLORS = [RED, BLUE, YELLOW, GREEN, ORANGE, PURPLE, PINK, CYAN]

# Bordo ve Beyaz renkler (engeller için)
BURGUNDY = (128, 0, 32)
BURGUNDY_LIGHT = (180, 50, 70)
BURGUNDY_DARK = (80, 0, 20)
WHITE_PURE = (255, 255, 255)

# Gece/Gündüz renkleri
DAY_SKY = (135, 206, 235)
NIGHT_SKY = (25, 25, 50)
DAY_GROUND = (34, 139, 34)
NIGHT_GROUND = (20, 40, 20)

# Saat
clock = pygame.time.Clock()
FPS = 60

# Fontlar - Luckiest Guy fontu (tüm yazılar için)
def load_font(size):
    try:
        return pygame.font.SysFont('luckiestguy', size)
    except:
        try:
            return pygame.font.SysFont('LuckiestGuy', size)
        except:
            return pygame.font.Font(None, size)

font = load_font(36)
small_font = load_font(28)
title_font = load_font(50)

# Buton boyutları
button_width = 280
button_height = 50
spacing = 12

# Oyun değişkenleri
gravity = 0.5
flap_strength = -8
pipe_gap = 180
pipe_velocity = -3
pipe_spawn_delay = 90
obstacle_count = 0
boss_dodged_count = 0
boss_max_dodge = 7
boss_final_question_asked = False
countdown_active = False
countdown_value = 3
countdown_timer = 0
boss_fight_active = False

# Zorluk seviyesi
difficulty = None
selected_area_temp = None

# Gece/Gündüz değişkenleri
is_night = False
day_night_cycle = 0
CYCLE_DURATION = 1800

# Engel hızlanma değişkenleri
speed_increased = False
normal_pipe_velocity = -3
speed_up_velocity = -5
speed_increase_threshold = 9999  # Başlangıçta hızlanma yok, start_game'de ayarlanır

# Engel hareket değişkenleri (sadece zor modda hareketli)
obstacle_moving = False
obstacle_move_speed = 0.5
obstacle_move_direction = 1

# Hedef engel sayıları
target_obstacles = 40

# Küresel durumlar
game_state = "MENU"
selected_area = None
score = 0
lives = 3
question_text = ""
question_options = []
correct_answer = ""
waiting_for_answer = False
boss_attack_timer = 0
boss_projectiles = []
pipe_spawn_counter = 0
question_counter = 0
previous_game_state = "PLAYING"

# Soru zorluk seviyeleri için ayrı soru havuzları
easy_questions = [
    {"q": "Bilgisayar nedir?", "a": "Elektronik cihaz", "wrong": ["Mobilya", "Yiyecek", "Giyecek"]},
    {"q": "İnternet ne işe yarar?", "a": "Bilgi paylaşımı", "wrong": ["Yemek", "Uyku", "Spor"]},
    {"q": "Klavye ne işe yarar?", "a": "Yazı yazmak", "wrong": ["Oynamak", "Yemek", "Koşmak"]},
    {"q": "Fare ne işe yarar?", "a": "Tıklamak", "wrong": ["Uçmak", "Yüzmek", "Zıplamak"]},
    {"q": "Ekran ne işe yarar?", "a": "Görüntü göstermek", "wrong": ["Ses çalmak", "Yemek pişirmek", "Temizlik"]},
]

medium_questions = [
    {"q": "Python bir programlama dili midir?", "a": "Evet", "wrong": ["Hayır", "Belki", "Oyun"]},
    {"q": "Hangisi bir veritabanıdır?", "a": "MySQL", "wrong": ["Python", "Java", "C++"]},
    {"q": "Algoritma nedir?", "a": "Adım adım çözüm", "wrong": ["Oyun", "Film", "Müzik"]},
    {"q": "Hangisi bir işletim sistemidir?", "a": "Windows", "wrong": ["Word", "Excel", "Chrome"]},
    {"q": "Yazılım hatasına ne denir?", "a": "Bug", "wrong": ["Feature", "Update", "Patch"]},
]

hard_questions = [
    {"q": "Nesne yönelimli programlamada kalıtım nedir?", "a": "Özellik miras alma", "wrong": ["Saklama", "Silme", "Kopyalama"]},
    {"q": "Veri yapılarında stack nedir?", "a": "LIFO", "wrong": ["FIFO", "Rastgele", "Sıralı"]},
    {"q": "SQL enjeksiyonu nedir?", "a": "Saldırı türü", "wrong": ["Veritabanı", "Program", "Ağ"]},
    {"q": "Hangisi bir şifreleme algoritmasıdır?", "a": "AES", "wrong": ["HTTP", "FTP", "SMTP"]},
    {"q": "Machine Learning nedir?", "a": "Makine öğrenmesi", "wrong": ["Veri tabanı", "Ağ", "Güvenlik"]},
]

# ALANLAR ve SORULAR
area_data = {
    "Siber Güvenlik": {
        "boss": "Anonymous",
        "boss_image": "🦹",
        "color": (0, 200, 0),
        "hover_color": (0, 255, 0),
        "easy_questions": easy_questions,
        "medium_questions": medium_questions,
        "hard_questions": hard_questions,
    },
    "FPV": {
        "boss": "Drone Hunter",
        "boss_image": "🚁",
        "color": (0, 200, 200),
        "hover_color": (0, 255, 255),
        "easy_questions": easy_questions,
        "medium_questions": medium_questions,
        "hard_questions": hard_questions,
    },
    "Yazılım": {
        "boss": "Bug Monster",
        "boss_image": "🐛",
        "color": (255, 100, 0),
        "hover_color": (255, 150, 0),
        "easy_questions": easy_questions,
        "medium_questions": medium_questions,
        "hard_questions": hard_questions,
    },
    "Tasarım": {
        "boss": "Pixel Master",
        "boss_image": "🎨",
        "color": (200, 100, 200),
        "hover_color": (255, 100, 255),
        "easy_questions": easy_questions,
        "medium_questions": medium_questions,
        "hard_questions": hard_questions,
    },
    "İHA": {
        "boss": "Sky Terminator",
        "boss_image": "✈️",
        "color": (200, 200, 0),
        "hover_color": (255, 255, 0),
        "easy_questions": easy_questions,
        "medium_questions": medium_questions,
        "hard_questions": hard_questions,
    }
}

# Kuş sınıfı
class Bird:
    def __init__(self):
        self.x = 100
        self.y = SCREEN_HEIGHT // 2
        self.vel_y = 0
        self.radius = 18
        self.wing_angle = 0
        self.wing_direction = 1

    def flap(self):
        self.vel_y = flap_strength
        self.wing_angle = -30

    def update(self):
        self.vel_y += gravity
        self.y += self.vel_y
        self.wing_angle += 8 * self.wing_direction
        if self.wing_angle > 30:
            self.wing_angle = 30
            self.wing_direction = -1
        elif self.wing_angle < -30:
            self.wing_angle = -30
            self.wing_direction = 1

    def draw(self):
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, (255, 200, 0), (int(self.x), int(self.y)), self.radius - 3)
        pygame.draw.circle(screen, WHITE, (int(self.x) + 8, int(self.y) - 6), 5)
        pygame.draw.circle(screen, BLACK, (int(self.x) + 9, int(self.y) - 6), 3)
        pygame.draw.polygon(screen, ORANGE, [
            (int(self.x) + 18, int(self.y) - 3),
            (int(self.x) + 28, int(self.y)),
            (int(self.x) + 18, int(self.y) + 3)
        ])
        wing_points_left = [
            (int(self.x) - 8, int(self.y)),
            (int(self.x) - 25, int(self.y) - 10 + self.wing_angle // 2),
            (int(self.x) - 20, int(self.y)),
            (int(self.x) - 25, int(self.y) + 10 - self.wing_angle // 2)
        ]
        pygame.draw.polygon(screen, (255, 180, 0), wing_points_left)
        wing_points_right = [
            (int(self.x) + 5, int(self.y) - 5),
            (int(self.x) + 20, int(self.y) - 15 + self.wing_angle // 2),
            (int(self.x) + 15, int(self.y) - 3),
            (int(self.x) + 20, int(self.y) + 5 - self.wing_angle // 2)
        ]
        pygame.draw.polygon(screen, (255, 180, 0), wing_points_right)

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

# Engel sınıfı (tüm modlarda hareketli)
class Obstacle:
    def __init__(self, x):
        self.x = x
        self.original_height = random.randint(150, SCREEN_HEIGHT - pipe_gap - 150)
        self.height = self.original_height
        self.move_offset = 0
        
        self.top_rect = pygame.Rect(x, 0, 60, self.height)
        self.bottom_rect = pygame.Rect(x, self.height + pipe_gap, 60, SCREEN_HEIGHT - self.height - pipe_gap)

    def update(self):
        global obstacle_move_direction
        self.x += pipe_velocity
        
        # Sadece zor modda (obstacle_moving=True) engeller hareket eder
        if obstacle_moving:
            self.move_offset += obstacle_move_speed * obstacle_move_direction
            if abs(self.move_offset) > 30:
                obstacle_move_direction *= -1
            
            self.height = self.original_height + self.move_offset
            self.height = max(100, min(SCREEN_HEIGHT - pipe_gap - 100, self.height))
            
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x
        self.top_rect.height = self.height
        self.bottom_rect.y = self.height + pipe_gap
        self.bottom_rect.height = SCREEN_HEIGHT - self.height - pipe_gap

    def draw(self):
        pygame.draw.rect(screen, BURGUNDY, self.top_rect)
        pygame.draw.rect(screen, BURGUNDY, self.bottom_rect)
        
        for i in range(0, self.top_rect.height, 25):
            stripe_rect = pygame.Rect(self.x + 5, i, 50, 10)
            pygame.draw.rect(screen, WHITE_PURE, stripe_rect)
        
        for i in range(0, self.bottom_rect.height, 25):
            stripe_rect = pygame.Rect(self.x + 5, self.height + pipe_gap + i, 50, 10)
            pygame.draw.rect(screen, WHITE_PURE, stripe_rect)
        
        pygame.draw.rect(screen, BURGUNDY_DARK, self.top_rect, 3)
        pygame.draw.rect(screen, BURGUNDY_DARK, self.bottom_rect, 3)
        
        pygame.draw.rect(screen, (255, 215, 0), (self.x - 5, self.top_rect.bottom - 15, 70, 15), border_radius=5)
        pygame.draw.rect(screen, (255, 215, 0), (self.x - 5, self.bottom_rect.y - 5, 70, 15), border_radius=5)

    def offscreen(self):
        return self.x + 60 < 0

# Araba sınıfı
class Car:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.y = SCREEN_HEIGHT - 65
        self.width = 30
        self.height = 20
        self.color = random.choice(CAR_COLORS)
        self.speed = random.randint(3, 6)
        
    def update(self):
        self.x -= self.speed
        
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), border_radius=5)
        pygame.draw.rect(screen, (100, 100, 200), (self.x + 5, self.y - 5, 8, 8), border_radius=2)
        pygame.draw.rect(screen, (100, 100, 200), (self.x + 17, self.y - 5, 8, 8), border_radius=2)
        pygame.draw.circle(screen, BLACK, (self.x + 5, self.y + self.height - 3), 4)
        pygame.draw.circle(screen, BLACK, (self.x + self.width - 5, self.y + self.height - 3), 4)
        pygame.draw.circle(screen, BLACK, (self.x + 5, self.y + 3), 4)
        pygame.draw.circle(screen, BLACK, (self.x + self.width - 5, self.y + 3), 4)
        
    def offscreen(self):
        return self.x + self.width < 0

# Buton sınıfı
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.is_hovered = False

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=10)
        text_surf = font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered and self.action:
                return self.action()
        return None

# Boss füzesi
class BossProjectile:
    def __init__(self, x, y, target_y):
        self.x = x
        self.y = y
        self.target_y = target_y
        self.radius = 8
        self.speed_x = -5
        self.passed = False
        
    def update(self):
        self.x += self.speed_x
        if self.y < self.target_y:
            self.y += 2
        elif self.y > self.target_y:
            self.y -= 2

    def draw(self):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, ORANGE, (int(self.x), int(self.y)), self.radius - 2)
        pygame.draw.polygon(screen, RED, [
            (int(self.x) + 12, int(self.y)),
            (int(self.x) + 4, int(self.y) - 4),
            (int(self.x) + 4, int(self.y) + 4)
        ])

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

# Arka plan
def draw_game_background():
    global is_night, day_night_cycle
    
    day_night_cycle += 1
    if day_night_cycle >= CYCLE_DURATION:
        day_night_cycle = 0
        is_night = not is_night
    
    if is_night:
        for y in range(SCREEN_HEIGHT):
            color_value = int(25 + (y / SCREEN_HEIGHT) * 30)
            pygame.draw.line(screen, (color_value, color_value, color_value + 20), (0, y), (SCREEN_WIDTH, y))
        
        for i in range(50):
            star_x = (i * 131) % SCREEN_WIDTH
            star_y = (i * 253) % (SCREEN_HEIGHT // 2)
            star_size = ((i * 7) % 2) + 1
            pygame.draw.circle(screen, WHITE, (int(star_x), int(star_y)), star_size)
        
        pygame.draw.circle(screen, (255, 255, 200), (SCREEN_WIDTH - 80, 60), 25)
        pygame.draw.circle(screen, (30, 30, 50), (SCREEN_WIDTH - 70, 55), 22)
    else:
        for y in range(SCREEN_HEIGHT):
            color_value = int(135 + (y / SCREEN_HEIGHT) * 100)
            pygame.draw.line(screen, (100, 150, color_value), (0, y), (SCREEN_WIDTH, y))
        
        pygame.draw.circle(screen, (255, 255, 100), (80, 80), 35)
        pygame.draw.circle(screen, (255, 255, 0), (80, 80), 30)
        
        cloud_rects = [(100, 120, 60, 40), (140, 110, 70, 50), (180, 120, 50, 35)]
        for rect in cloud_rects:
            pygame.draw.ellipse(screen, (255, 255, 255), rect)
    
    ground_color = DAY_GROUND if not is_night else NIGHT_GROUND
    pygame.draw.rect(screen, ground_color, (0, SCREEN_HEIGHT - 80, SCREEN_WIDTH, 80))
    
    for i in range(0, SCREEN_WIDTH, 40):
        pygame.draw.rect(screen, YELLOW, (i, SCREEN_HEIGHT - 45, 20, 5))
    
    # Sadece "Haydi GençTek'li!" yazısı (üstteki hareketli engeller yazısı kaldırıldı)
    slogan = small_font.render("Haydi GençTek'li!", True, YELLOW if not is_night else (255, 255, 150))
    slogan_rect = slogan.get_rect(center=(SCREEN_WIDTH // 2, 40))
    screen.blit(slogan, slogan_rect)
    
    cycle_text = small_font.render("🌞" if not is_night else "🌙", True, WHITE)
    screen.blit(cycle_text, (SCREEN_WIDTH - 40, 10))

# Geri sayım çizimi
def draw_countdown():
    if countdown_active:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        count_font = load_font(100)
        count_text = count_font.render(str(countdown_value), True, YELLOW)
        screen.blit(count_text, (SCREEN_WIDTH//2 - count_text.get_width()//2, SCREEN_HEIGHT//2 - 50))
        
        go_text = font.render("Hazır ol!", True, WHITE)
        screen.blit(go_text, (SCREEN_WIDTH//2 - go_text.get_width()//2, SCREEN_HEIGHT//2 + 30))

# Soru ekranı
def ask_question(area, is_boss_question=False):
    global game_state, waiting_for_answer, question_text, question_options, correct_answer, question_counter
    
    if difficulty == "easy":
        q_list = area_data[area]["easy_questions"]
    elif difficulty == "medium":
        q_list = area_data[area]["medium_questions"]
    else:
        q_list = area_data[area]["hard_questions"]
    
    question_counter = (question_counter + 1) % len(q_list)
    q_data = q_list[question_counter]
    question_text = q_data["q"]
    correct_answer = q_data["a"]
    options = [correct_answer] + q_data["wrong"]
    random.shuffle(options)
    question_options = options
    waiting_for_answer = True
    if is_boss_question:
        game_state = "BOSS_QUESTION"
    else:
        game_state = "QUESTION"

def handle_answer(selected_opt):
    global game_state, waiting_for_answer, countdown_active, countdown_value, countdown_timer, obstacles, bird, pipe_spawn_counter
    
    if selected_opt == correct_answer:
        if game_state == "BOSS_QUESTION":
            game_state = "GAME_END"
            waiting_for_answer = False
        else:
            countdown_active = True
            countdown_value = 3
            countdown_timer = pygame.time.get_ticks()
            game_state = "COUNTDOWN"
            waiting_for_answer = False
    else:
        game_state = "MENU"
        waiting_for_answer = False

# Menü butonlarını oluştur
def create_menu_buttons():
    buttons = []
    areas = ["Siber Güvenlik", "FPV", "Yazılım", "Tasarım", "İHA"]
    total_height = len(areas) * button_height + (len(areas) - 1) * spacing
    start_y = (SCREEN_HEIGHT - total_height) // 2 - 50

    for i, area in enumerate(areas):
        y = start_y + i * (button_height + spacing)
        btn = Button(
            (SCREEN_WIDTH - button_width) // 2, y, button_width, button_height,
            f"🌟 {area} 🌟", 
            area_data[area]["color"], 
            area_data[area]["hover_color"],
            action=lambda a=area: select_area(a)
        )
        buttons.append(btn)
    return buttons

def select_area(area):
    global selected_area_temp, game_state
    selected_area_temp = area
    game_state = "DIFFICULTY"

# Zorluk seçim menüsü
def create_difficulty_buttons():
    buttons = []
    difficulties = [("KOLAY", (0, 200, 0)), ("ORTA", (200, 200, 0)), ("ZOR", (200, 0, 0))]
    total_height = len(difficulties) * button_height + (len(difficulties) - 1) * spacing
    start_y = (SCREEN_HEIGHT - total_height) // 2
    
    for i, (diff_text, color) in enumerate(difficulties):
        y = start_y + i * (button_height + spacing)
        btn = Button(
            (SCREEN_WIDTH - button_width) // 2, y, button_width, button_height,
            diff_text, color, (min(255, color[0]+50), min(255, color[1]+50), min(255, color[2]+50)),
            action=lambda d=diff_text: set_difficulty(d)
        )
        buttons.append(btn)
    return buttons

def set_difficulty(diff):
    global difficulty, game_state, selected_area
    diff_map = {"kolay": "easy", "orta": "medium", "zor": "hard"}
    difficulty = diff_map.get(diff.lower(), "easy")
    start_game(selected_area_temp)

# Pause menü butonları
def create_pause_buttons():
    buttons = []
    buttons.append(Button(
        (SCREEN_WIDTH - 200) // 2, SCREEN_HEIGHT // 2 - 40, 200, 50,
        "▶ Devam Et", GREEN, (0, 255, 0),
        action=lambda: "resume"
    ))
    buttons.append(Button(
        (SCREEN_WIDTH - 200) // 2, SCREEN_HEIGHT // 2 + 30, 200, 50,
        "🚪 Çıkış Yap", RED, (255, 0, 0),
        action=lambda: "exit"
    ))
    return buttons

def start_game(area):
    global game_state, selected_area, bird, obstacles, score, lives, boss_dodged_count, boss_final_question_asked, boss_projectiles, pipe_spawn_counter, obstacle_count, question_counter, boss_attack_timer, boss_fight_active, pipe_velocity, speed_increased, target_obstacles, obstacle_moving, speed_increase_threshold
    
    selected_area = area
    game_state = "PLAYING"
    bird = Bird()
    obstacles.clear()
    score = 0
    lives = 3
    boss_dodged_count = 0
    boss_final_question_asked = False
    boss_projectiles.clear()
    pipe_spawn_counter = 0
    obstacle_count = 0
    boss_attack_timer = 0
    boss_fight_active = False
    question_counter = random.randint(0, 4)
    speed_increased = False
    pipe_velocity = normal_pipe_velocity
    
    if difficulty == "easy":
        pipe_gap = 200
        boss_max_dodge = 5
        target_obstacles = 35
        obstacle_moving = False          # Kolay: engeller sabit
        speed_increase_threshold = 9999  # Kolay: hızlanma yok
        print("🎮 Kolay mod - Engeller sabit, 35 hedef engel, hızlanma yok")
    elif difficulty == "medium":
        pipe_gap = 180
        boss_max_dodge = 7
        target_obstacles = 55
        obstacle_moving = False          # Orta: engeller sabit
        speed_increase_threshold = 35   # Orta: 35 engelde hızlanma
        print("🎮 Orta mod - Engeller sabit, 55 hedef engel, 35 engelde hızlanma")
    else:
        pipe_gap = 160
        boss_max_dodge = 10
        target_obstacles = 70
        obstacle_moving = True           # Zor: engeller hareketli
        speed_increase_threshold = 50   # Zor: 50 engelde hızlanma
        print("🎮 Zor mod - Engeller hareketli, 70 hedef engel, 50 engelde hızlanma")
    
    print(f"🎮 Oyun başladı: {area} - Zorluk: {difficulty} - Hedef: {target_obstacles} engel")

# Menü çizimi
def draw_menu():
    for y in range(SCREEN_HEIGHT):
        color_value = int(50 + (y / SCREEN_HEIGHT) * 100)
        pygame.draw.line(screen, (color_value, 20, 80), (0, y), (SCREEN_WIDTH, y))
    
    title = title_font.render("FLAPPY QUIZ", True, YELLOW)
    subtitle = small_font.render("Sektörün Yeni Liderleri", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
    screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 110))
    
    for button in menu_buttons:
        button.draw(screen)

# Zorluk menüsü çizimi
def draw_difficulty_menu():
    for y in range(SCREEN_HEIGHT):
        color_value = int(50 + (y / SCREEN_HEIGHT) * 100)
        pygame.draw.line(screen, (color_value, 20, 80), (0, y), (SCREEN_WIDTH, y))
    
    title = title_font.render(f"{selected_area_temp}", True, YELLOW)
    subtitle = small_font.render("Zorluk Seviyesi Seçin", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
    screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 110))
    
    for button in difficulty_buttons:
        button.draw(screen)

# Pause menü çizimi
def draw_pause_menu():
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(150)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    pause_text = title_font.render("OYUN DURDURULDU", True, YELLOW)
    screen.blit(pause_text, (SCREEN_WIDTH//2 - pause_text.get_width()//2, SCREEN_HEIGHT//2 - 120))
    
    info_text = small_font.render("ESC: Devam Et", True, WHITE)
    screen.blit(info_text, (SCREEN_WIDTH//2 - info_text.get_width()//2, SCREEN_HEIGHT//2 - 60))
    
    for button in pause_buttons:
        button.draw(screen)

# Soru ekranını çiz
def draw_question_screen():
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    question_box = pygame.Rect(30, 80, SCREEN_WIDTH - 60, 100)
    pygame.draw.rect(screen, DARK_BLUE, question_box, border_radius=15)
    pygame.draw.rect(screen, WHITE, question_box, 2, border_radius=15)
    
    wrapped_text = []
    words = question_text.split()
    line = ""
    for word in words:
        test_line = line + word + " "
        if small_font.size(test_line)[0] < SCREEN_WIDTH - 80:
            line = test_line
        else:
            wrapped_text.append(line)
            line = word + " "
    wrapped_text.append(line)
    
    y_offset = 110
    for line in wrapped_text:
        q_surf = small_font.render(line, True, WHITE)
        screen.blit(q_surf, (50, y_offset))
        y_offset += 30
    
    for i, opt in enumerate(question_options):
        opt_box = pygame.Rect(50, 250 + i * 60, SCREEN_WIDTH - 100, 45)
        colors = [LIGHT_BLUE, (100, 150, 200), (80, 130, 180), (60, 110, 160)]
        pygame.draw.rect(screen, colors[i % len(colors)], opt_box, border_radius=8)
        pygame.draw.rect(screen, WHITE, opt_box, 2, border_radius=8)
        opt_txt = small_font.render(f"{i+1}. {opt}", True, WHITE)
        screen.blit(opt_txt, (70, 260 + i * 60))
    
    info = small_font.render("Cevap için 1-4 tuşlarına bas | ESC: Menü", True, YELLOW)
    screen.blit(info, (SCREEN_WIDTH//2 - info.get_width()//2, SCREEN_HEIGHT - 60))

# Boss çizimi
def draw_boss():
    boss_name = area_data[selected_area]["boss"]
    boss_icon = area_data[selected_area]["boss_image"]
    
    boss_rect = pygame.Rect(SCREEN_WIDTH - 120, 20, 100, 100)
    pygame.draw.rect(screen, RED, boss_rect, border_radius=15)
    pygame.draw.rect(screen, YELLOW, boss_rect, 3, border_radius=15)
    
    icon_font = load_font(60)
    icon_text = icon_font.render(boss_icon, True, WHITE)
    screen.blit(icon_text, (SCREEN_WIDTH - 85, 35))
    
    name_text = small_font.render(boss_name, True, WHITE)
    screen.blit(name_text, (SCREEN_WIDTH - 115, 130))
    
    dodge_text = small_font.render(f"Kaçış: {boss_dodged_count}/{boss_max_dodge}", True, YELLOW)
    screen.blit(dodge_text, (SCREEN_WIDTH - 115, 150))

# Oyun bitiş ekranı
def draw_game_end():
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    thanks = title_font.render("TEBRİKLER!", True, YELLOW)
    screen.blit(thanks, (SCREEN_WIDTH//2 - thanks.get_width()//2, 50))
    
    text1 = small_font.render("Bu oyunu oynadığınız için teşekkürler", True, WHITE)
    screen.blit(text1, (SCREEN_WIDTH//2 - text1.get_width()//2, 150))
    
    text2 = small_font.render("Oyunumuz", True, WHITE)
    screen.blit(text2, (SCREEN_WIDTH//2 - text2.get_width()//2, 200))
    
    names = [
        "Seydi Ahmet Demir",
        "Mehmet Efe Keskinsoy", 
        "Hayrünnisa Poyraz",
        "Osman Ölmez",
        "Enes Utku Çakmak",
        "Rahmi Çınar Sari",
        "Dilek Kılınç"
    ]
    
    y = 260
    for name in names:
        name_text = small_font.render(name, True, CYAN)
        screen.blit(name_text, (SCREEN_WIDTH//2 - name_text.get_width()//2, y))
        y += 30
    
    by_text = small_font.render("tarafından yapılmıştır", True, WHITE)
    screen.blit(by_text, (SCREEN_WIDTH//2 - by_text.get_width()//2, y + 10))
    
    info = small_font.render("Menüye dönmek için herhangi bir tuşa bas...", True, WHITE)
    screen.blit(info, (SCREEN_WIDTH//2 - info.get_width()//2, SCREEN_HEIGHT - 80))

# Ana oyun döngüsü
bird = Bird()
obstacles = []
cars = []
menu_buttons = create_menu_buttons()
difficulty_buttons = create_difficulty_buttons()
pause_buttons = create_pause_buttons()
car_spawn_counter = 0
CAR_SPAWN_DELAY = 90

running = True
while running:
    current_time = pygame.time.get_ticks()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == "MENU":
            for button in menu_buttons:
                button.handle_event(event)
                
        elif game_state == "DIFFICULTY":
            for button in difficulty_buttons:
                button.handle_event(event)
                
        elif game_state == "PLAYING" or game_state == "BOSS_FIGHT":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()
                elif event.key == pygame.K_ESCAPE:
                    previous_game_state = game_state
                    game_state = "PAUSE_MENU"
                    
        elif game_state == "PAUSE_MENU":
            for button in pause_buttons:
                result = button.handle_event(event)
                if result == "resume":
                    game_state = previous_game_state
                elif result == "exit":
                    game_state = "MENU"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_state = previous_game_state
                    
        elif game_state == "QUESTION" or game_state == "BOSS_QUESTION":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    previous_game_state = game_state
                    game_state = "PAUSE_MENU"
                elif event.key == pygame.K_1 and len(question_options) >= 1:
                    handle_answer(question_options[0])
                elif event.key == pygame.K_2 and len(question_options) >= 2:
                    handle_answer(question_options[1])
                elif event.key == pygame.K_3 and len(question_options) >= 3:
                    handle_answer(question_options[2])
                elif event.key == pygame.K_4 and len(question_options) >= 4:
                    handle_answer(question_options[3])
                    
        elif game_state == "GAME_END":
            if event.type == pygame.KEYDOWN:
                game_state = "MENU"
                
        elif game_state == "COUNTDOWN":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    previous_game_state = game_state
                    game_state = "PAUSE_MENU"

    if game_state == "COUNTDOWN" and countdown_active:
        if current_time - countdown_timer > 1000:
            countdown_value -= 1
            countdown_timer = current_time
            if countdown_value <= 0:
                countdown_active = False
                game_state = "PLAYING"

    # Zorluk seviyesine göre hızlanma eşiği (orta: 35, zor: 50, kolay: hızlanma yok)
    if game_state == "PLAYING":
        if obstacle_count >= speed_increase_threshold and not speed_increased:
            pipe_velocity = speed_up_velocity
            speed_increased = True
            print(f"⚡ {speed_increase_threshold} engel geçildi! Kuş hızlandı! ⚡")

    if game_state == "MENU":
        draw_menu()
        
    elif game_state == "DIFFICULTY":
        draw_difficulty_menu()
        
    elif game_state == "PLAYING":
        draw_game_background()
        bird.update()
        
        car_spawn_counter += 1
        if car_spawn_counter >= CAR_SPAWN_DELAY:
            cars.append(Car())
            car_spawn_counter = 0
        
        for car in cars[:]:
            car.update()
            if car.offscreen():
                cars.remove(car)
            car.draw()
        
        if bird.y - bird.radius <= 0 or bird.y + bird.radius >= SCREEN_HEIGHT - 80:
            lives -= 1
            if lives <= 0:
                game_state = "MENU"
                score = 0
                obstacle_count = 0
            else:
                bird.y = SCREEN_HEIGHT // 2
                bird.vel_y = 0
                countdown_active = True
                countdown_value = 3
                countdown_timer = current_time
                game_state = "COUNTDOWN"

        pipe_spawn_counter += 1
        if pipe_spawn_counter >= pipe_spawn_delay:
            obstacles.append(Obstacle(SCREEN_WIDTH))
            pipe_spawn_counter = 0

        for obstacle in obstacles[:]:
            obstacle.update()
            if obstacle.offscreen():
                obstacles.remove(obstacle)
                score += 10
                obstacle_count += 1
                if obstacle_count >= target_obstacles:
                    game_state = "BOSS_FIGHT"
                    boss_fight_active = True
                    obstacles.clear()
                    print("🔥 BOSS SAVAŞI BAŞLADI! 🔥")

        bird_rect = bird.get_rect()
        for obstacle in obstacles:
            if bird_rect.colliderect(obstacle.top_rect) or bird_rect.colliderect(obstacle.bottom_rect):
                lives -= 1
                if lives <= 0:
                    game_state = "MENU"
                    score = 0
                    obstacle_count = 0
                else:
                    bird.y = SCREEN_HEIGHT // 2
                    bird.vel_y = 0
                    obstacles.clear()
                    bird.x = 80
                    pipe_spawn_counter = 20
                    ask_question(selected_area, is_boss_question=False)
                break

        bird.draw()
        for obstacle in obstacles:
            obstacle.draw()

        score_text = font.render(f"🏆 Skor: {score}", True, WHITE)
        lives_text = font.render(f"❤️ Can: {lives}", True, RED)
        obstacle_text = small_font.render(f"📊 Engel: {obstacle_count}/{target_obstacles}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))
        screen.blit(obstacle_text, (10, 90))
        
        if speed_increased:
            speed_text = small_font.render("⚡ HIZLANDI! ⚡", True, ORANGE)
            screen.blit(speed_text, (SCREEN_WIDTH//2 - speed_text.get_width()//2, 10))
        
        # "HAREKETLİ ENGELLER" yazısı KALDIRILDI
        
        diff_color = GREEN if difficulty == "easy" else (YELLOW if difficulty == "medium" else RED)
        diff_text = small_font.render(f"{difficulty.upper()} MOD", True, diff_color)
        screen.blit(diff_text, (SCREEN_WIDTH//2 - diff_text.get_width()//2, SCREEN_HEIGHT - 30))
        
    elif game_state == "BOSS_FIGHT":
        draw_game_background()
        bird.update()
        
        for car in cars:
            car.update()
            car.draw()
        
        if bird.y - bird.radius <= 0 or bird.y + bird.radius >= SCREEN_HEIGHT - 80:
            lives -= 1
            if lives <= 0:
                game_state = "MENU"
            else:
                bird.y = SCREEN_HEIGHT // 2
                bird.vel_y = 0
                countdown_active = True
                countdown_value = 3
                countdown_timer = current_time
                game_state = "COUNTDOWN"
        
        draw_boss()
        
        boss_attack_timer += 1
        if boss_attack_timer > 30 and boss_dodged_count < boss_max_dodge:
            boss_attack_timer = 0
            boss_projectiles.append(BossProjectile(SCREEN_WIDTH - 60, random.randint(50, SCREEN_HEIGHT - 50), bird.y))

        bird_rect = bird.get_rect()
        for p in boss_projectiles[:]:
            p.update()
            if p.x + p.radius < 0:
                if not p.passed:
                    p.passed = True
                    boss_dodged_count += 1
                    print(f"Füze kaçırıldı! {boss_dodged_count}/{boss_max_dodge}")
                boss_projectiles.remove(p)
                
                if boss_dodged_count >= boss_max_dodge and not boss_final_question_asked:
                    boss_final_question_asked = True
                    ask_question(selected_area, is_boss_question=True)
            elif p.get_rect().colliderect(bird_rect):
                boss_projectiles.remove(p)
        
        bird.draw()
        for p in boss_projectiles:
            p.draw()
        
        score_text = font.render(f"🏆 Skor: {score}", True, WHITE)
        lives_text = font.render(f"❤️ Can: {lives}", True, RED)
        dodge_text = font.render(f"🎯 Kaçış: {boss_dodged_count}/{boss_max_dodge}", True, YELLOW)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))
        screen.blit(dodge_text, (10, 90))
        
        boss_indicator = small_font.render("⚡ BOSS SAVAŞI! ⚡", True, RED)
        screen.blit(boss_indicator, (SCREEN_WIDTH//2 - boss_indicator.get_width()//2, 10))
        
    elif game_state == "QUESTION" or game_state == "BOSS_QUESTION":
        draw_question_screen()
        
    elif game_state == "GAME_END":
        draw_game_end()
        
    elif game_state == "PAUSE_MENU":
        if previous_game_state == "PLAYING":
            draw_game_background()
            bird.draw()
            for obstacle in obstacles:
                obstacle.draw()
            for car in cars:
                car.draw()
            score_text = font.render(f"🏆 Skor: {score}", True, WHITE)
            lives_text = font.render(f"❤️ Can: {lives}", True, RED)
            obstacle_text = small_font.render(f"📊 Engel: {obstacle_count}/{target_obstacles}", True, WHITE)
            screen.blit(score_text, (10, 10))
            screen.blit(lives_text, (10, 50))
            screen.blit(obstacle_text, (10, 90))
        elif previous_game_state == "BOSS_FIGHT":
            draw_game_background()
            bird.draw()
            draw_boss()
            for p in boss_projectiles:
                p.draw()
            score_text = font.render(f"🏆 Skor: {score}", True, WHITE)
            lives_text = font.render(f"❤️ Can: {lives}", True, RED)
            screen.blit(score_text, (10, 10))
            screen.blit(lives_text, (10, 50))
        draw_pause_menu()
        
    elif game_state == "COUNTDOWN":
        draw_game_background()
        bird.draw()
        for obstacle in obstacles:
            obstacle.draw()
        for car in cars:
            car.draw()
        score_text = font.render(f"🏆 Skor: {score}", True, WHITE)
        lives_text = font.render(f"❤️ Can: {lives}", True, RED)
        obstacle_text = small_font.render(f"📊 Engel: {obstacle_count}/{target_obstacles}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))
        screen.blit(obstacle_text, (10, 90))
        draw_countdown()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
