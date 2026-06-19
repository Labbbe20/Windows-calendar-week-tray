import datetime              # Wird benutzt um Datum / Kalenderwoche zu bekommen
import threading             # Damit ein Hintergrund-Thread laufen kann
import time                  # Für Wartezeiten
from PIL import Image, ImageDraw, ImageFont   # Pillow → erstellt das Icon mit Text
import pystray               # Bibliothek für System-Tray Icons


# Funktion: aktuelle Kalenderwoche holen
def get_calendar_week():
    # isocalendar() gibt Jahr, Woche und Wochentag zurück
    return datetime.datetime.now().isocalendar().week


# Funktion: erzeugt ein Icon mit der Kalenderwoche als Zahl
def create_icon(week):

    # Transparentes Bild erstellen (RGBA statt RGB)
    img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))

    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 55)
    except:
        font = ImageFont.load_default()

    text = str(week)

    # Textgröße berechnen
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    # Schwarze Schrift auf transparentem Hintergrund
    draw.text(
        ((64 - w) / 2, (64 - h) / 2),
        text,
        fill=(255, 255, 255, 255),   # Schwarz
        font=font
    )

    return img


# Funktion: aktualisiert das Tray-Icon regelmäßig
def update_icon(icon):

    while True:
        # aktuelle Kalenderwoche holen
        week = get_calendar_week()

        # neues Icon erzeugen
        icon.icon = create_icon(week)

        # 1 Stunde warten
        # (reicht völlig, da sich die Woche nur einmal pro Woche ändert)
        time.sleep(3600)


# Funktion: Programm beenden (wenn man im Tray-Menü "Beenden" klickt)
def on_quit(icon, item):
    icon.stop()


# Beim Start einmal aktuelle Woche holen
week = get_calendar_week()

# Tray-Icon erstellen
icon = pystray.Icon(
    "calendar_week",          # interner Name
    create_icon(week),        # Icon Bild
    "Kalenderwoche"           # Tooltip Text
)


# Hintergrundthread starten der das Icon aktualisiert
threading.Thread(
    target=update_icon,
    args=(icon,),
    daemon=True
).start()


# Menü für Rechtsklick auf das Tray-Icon
icon.menu = pystray.Menu(
    pystray.MenuItem("Beenden", on_quit)
)

# Icon starten (Programm läuft jetzt im System-Tray)
icon.run()