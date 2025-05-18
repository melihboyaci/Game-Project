import sys
import os
import pygame

# Gerekli path'leri ekle
sys.path.append(os.path.join(os.path.dirname(__file__), "src", "Middle_Age_Stage"))
sys.path.append(os.path.join(os.path.dirname(__file__), "src", "Rifle_Stage"))
sys.path.append(os.path.join(os.path.dirname(__file__), "src", "Space_Stage"))
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from middle_age import start_middle_age
from game_loop import start_rifle_stage
from stage3 import start_space_stage
from cutscene_utils import play_cutscene
from src.Space_Stage.utils.views import start_screen

def main():
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Gate of Ages")
    clock = pygame.time.Clock()
    
    start_screen(screen, clock)

    # Middle Age Opening (4 ayrı kare, her biri belirli süre ekranda kalır)
    play_cutscene(
        screen,
        "assets/cutscenes_assets/middle-age-opening-1.png",
        "assets/cutscenes_assets/background-music-16s.mp3",
        duration=4,
        subtitle="Zaman Kaydırma Motoru... Kontrolden çıktı. \n Gözlerimi açtığımda kendimi bu... bu ilkel cehennemde buldum."
    )
    play_cutscene(
        screen,
        "assets/cutscenes_assets/middle-age-opening-1.png",
        None,
        duration=4,
        subtitle="Gelişmiş silahlarım, gemim... hepsi yok oldu. \n Sadece eğitimim ve hayatta kalma içgüdülerim var."
    )
    play_cutscene(
        screen,
        "assets/cutscenes_assets/middle-age-opening-1.png",
        None,
        duration=4,
        subtitle="Bu yaratıklar... Orklar... Daha önce sadece efsanelerde duyduğum türden. \n Ama bu öfke, bu vahşet... doğal değil."
    )
    play_cutscene(
        screen,
        "assets/cutscenes_assets/middle-age-opening-1.png",
        None,
        duration=4,
        subtitle="Bu ormanın derinliklerinde bir anomali hissediyorum... \n Bir umut ışığı mı, yoksa daha büyük bir tuzağın başlangıcı mı?"
    )
    pygame.mixer.music.stop()
    # Middle Age Stage
    result = start_middle_age()
    if result != "next":
        return

    # Rifle Opening
    play_cutscene(
        screen,
        "assets/cutscenes_assets/rifle-stage-opening-1.png",
        "assets/cutscenes_assets/background-music-16s.mp3",
        duration=4,
        subtitle="O antik portal... beni bambaşka bir çağa, bambaşka bir vahşete getirdi."
    )
    play_cutscene(
        screen,
        "assets/cutscenes_assets/rifle-stage-opening-1.png",
        None,
        duration=4,
        subtitle="Kılıçların ve baltaların yerini, uzaktan ölüm kusan metal canavarlar almış. \n Bu çağın savaşı daha kişisel değil, ama bir o kadar da acımasız."
    )
    play_cutscene(
        screen,
        "assets/cutscenes_assets/rifle-stage-opening-1.png",
        None,
        duration=4,
        subtitle="Her köşe başında tehlike, her gölgede bir düşman. \n Ama öğrendiğim her şey, beni onlara bir adım daha yaklaştırıyor."
    )
    play_cutscene(
        screen,
        "assets/cutscenes_assets/rifle-stage-opening-1.png",
        None,
        duration=4,
        subtitle="Bir sonraki portalın sinyallerini alıyorum. Daha teknolojik, daha korunaklı. \n Lejyon'un kalbine giden yol buradan geçiyor olmalı."
    )
    pygame.mixer.music.stop()
    # Rifle Stage
    result = start_rifle_stage()
    if result != "next":
        return

    # Space Opening
    play_cutscene(
        screen,
        "assets/cutscenes_assets/space-stage-opening-1.png",
        "assets/cutscenes_assets/background-music-16s.mp3",
        duration=4,
        subtitle="İki çağ boyunca süren mücadele... Zamanın labirentlerinde kayboluş... \n Ve şimdi, her şeyin başladığı ve bittiği yerdeyim: uzayın sonsuz karanlığında."
    )
    play_cutscene(
        screen,
        "assets/cutscenes_assets/space-stage-opening-1.png",
        None,
        duration=4,
        subtitle="O devasa yapı... Kronos Lejyonu'nun kalbi. Orklar, askerler... \n hepsi bu merkezden yayılan bir vebanın parçalarıydı."
    )
    play_cutscene(
        screen,
        "assets/cutscenes_assets/space-stage-opening-1.png",
        None,
        duration=4,
        subtitle="Bu gemi belki onlarınkiler kadar güçlü değil, \n ama içinde geçmişin bilgeliği ve geleceğin umudu var."
    )
    play_cutscene(
        screen,
        "assets/cutscenes_assets/space-stage-opening-1.png",
        None,
        duration=4,
        subtitle="Medeniyetimin kaderi, o istasyonun içinde mühürlü. \n Ve ben o mührü kırmaya geldim. Bu son savaş olacak."
    )
    pygame.mixer.music.stop()
    # Space Stage
    result = start_space_stage()
    if result != "next":
        return
    
    play_cutscene(
        screen,
        "assets/cutscenes_assets/space-stage-ending-1.png",
        "assets/cutscenes_assets/opening-background-music.mp3",
        duration=5,
        subtitle=""
    )  

    play_cutscene(
        screen,
        "assets/cutscenes_assets/final_scene.png",
        None,
        duration=10,
        subtitle="Sürgün bitti. Yıldızların ve evrenin ötesinde, artık yeniden evimdeyim."
    )






    print("Oyun bitti!")
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
     