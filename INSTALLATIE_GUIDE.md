# Stap-voor-Stap Handleiding: Blockade 3D Classic Aimbot

## 📋 Vereisten

- Windows 10/11
- Python 3.8 of hoger (aanbevolen: Python 3.10+)
- Blockade 3D Classic geïnstalleerd via Steam
- Administrator rechten (voor mouse/keyboard input)

---

## Stap 1: Python Installeren

1. Download Python van https://www.python.org/downloads/
2. Tijdens installatie: **vink aan** "Add Python to PATH"
3. Installeer Python
4. Open Command Prompt (cmd) en test:
   ```bash
   python --version
   ```
   Je zou iets moeten zien zoals: `Python 3.10.x`

---

## Stap 2: Dependencies Installeren

1. Open Command Prompt (cmd) of PowerShell
2. Navigeer naar de aimbot map:
   ```bash
   cd C:\Users\Gebruiker\aimbot-image-processing-blockade3d
   ```
   (Pas het pad aan naar waar je de bestanden hebt)

3. Installeer alle benodigde packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Wacht tot alles geïnstalleerd is (kan een paar minuten duren)

---

## Stap 3: Blockade 3D Classic Instellen

### 3.1 Game Instellingen

1. Start **Blockade 3D Classic** via Steam
2. Ga naar **Settings** (Instellingen)
3. Zet de resolutie op **1024x768**
4. Zet de game in **Windowed Mode** (Venster modus)
5. Sla de instellingen op en herstart de game

### 3.2 Window Positie

1. Zorg dat de game window in de **linkerbovenhoek** van je scherm staat
2. De **Windows title bar** (bovenkant van het venster) moet zichtbaar zijn
3. Het venster moet precies in de hoek staan (x=0, y=0)

---

## Stap 4: Window Calibratie (Eerste Keer)

1. Open Command Prompt in de aimbot map
2. Run het calibratie script:
   ```bash
   python top_left_B3D_prep_4_aimbot_v3.py
   ```

3. Je ziet een countdown (4, 3, 2, 1)
4. **Tijdens de countdown**: 
   - Zet je muis op de **witte title bar** van het Blockade 3D venster
   - Laat de muis daar staan
   - Wacht tot het script klaar is (10-50 seconden)

5. Als je ziet: "top left corner achieved" of het script stopt, is het klaar
6. **BELANGRIJK**: Laat het game venster op deze positie staan!

---

## Stap 5: Aimbot Starten

1. Zorg dat Blockade 3D Classic draait in windowed mode (1024x768)
2. Zorg dat het venster in de linkerbovenhoek staat
3. Open Command Prompt in de aimbot map
4. Start de aimbot:
   ```bash
   python main_074_3.6.5.py
   ```

5. Je ziet:
   - Countdown (4, 3, 2, 1)
   - "GUI started! Press INSERT to show/hide the UI"
   - FPS informatie

6. **Druk op INSERT** om de GUI te openen

---

## Stap 6: GUI Configureren

### 6.1 GUI Openen

- Druk op **INSERT** (in het spel of op desktop)
- De GUI verschijnt

### 6.2 Aimbot Activeren

1. In de GUI, klik op **"Enable Aimbot"**
   - Status verandert naar: "Aimbot: ON" (groen)

2. (Optioneel) Klik op **"Enable Lock-on"** voor right-click lock-on feature

### 6.3 Instellingen Aanpassen (Optioneel)

- **Aim Accuracy**: Slider (85-99%) - lager = meer menselijk
- **Reaction Time**: Min-Max in milliseconden
- **Max Aim Distance**: Maximale afstand om te richten

3. Klik op **"Apply Settings"** om op te slaan

---

## Stap 7: In-Game Gebruik

### 7.1 Basis Gebruik

1. Join een game in Blockade 3D Classic
2. Druk **ESC** en disable chat (optioneel, maar aanbevolen)
3. Equip **m700** of **crossbow** (geen muzzle flash)
4. De aimbot werkt nu automatisch!

### 7.2 Hotkeys

- **INSERT** - Toon/verberg GUI
- **TAB** - Pauzeer aimbot (bijvoorbeeld voor scoreboard)
- **N** - Stop de aimbot volledig
- **Right-Click** - Lock-on op target (als lock-on enabled is)

### 7.3 Right-Click Lock-On (Optioneel)

1. Zorg dat **"Enable Lock-on"** aan staat in de GUI
2. In-game: **Right-click** op een vijand
3. De aimbot lockt nu op die target en volgt automatisch
4. Om te unlocken: Disable lock-on in GUI of druk op TAB

---

## Stap 8: Troubleshooting

### Probleem: Aimbot werkt niet

**Oplossing:**
- Check of game in 1024x768 windowed mode staat
- Check of window in linkerbovenhoek staat
- Herstart het calibratie script (stap 4)
- Check of GUI zegt "Aimbot: ON"

### Probleem: GUI verschijnt niet

**Oplossing:**
- Druk op INSERT (meerdere keren proberen)
- Check of Python script nog draait
- Herstart het main script

### Probleem: Aimbot richt verkeerd

**Oplossing:**
- Herstart calibratie script (stap 4)
- Check of window positie correct is
- Pas threshold aan in config.py (THRESHOLD_VALUE)

### Probleem: Te veel/te weinig misses

**Oplossing:**
- Pas AIM_ACCURACY aan in config.py (hoger = accurater)
- Pas MISS_CHANCE aan in config.py (lager = minder misses)

---

## Stap 9: Optimalisatie Tips

### Voor Betere Performance

1. **INT_SUBDIV**: In config.py, verhoog naar 24-30 voor snellere processing
2. **Close andere programma's** die veel CPU gebruiken
3. **Disable chat** in-game voor betere FPS

### Voor Meer Realisme

1. **AIM_ACCURACY**: Zet op 0.92-0.94 voor meer menselijke fouten
2. **MISS_CHANCE**: Zet op 0.10-0.15 voor meer misses
3. **Reaction Time**: Verhoog naar 100-300ms voor langzamere reacties

---

## Stap 10: Stoppen

1. Druk op **N** in het spel of Command Prompt
2. Of sluit de Command Prompt window
3. De GUI sluit automatisch
4. Statistics worden getoond (als je op N drukt)

---

## ⚠️ Belangrijke Notities

1. **Gebruik op eigen risico** - Cheats kunnen leiden tot bans
2. **Test eerst offline** of in private games
3. **Gebruik verantwoordelijk** - Niet gebruiken om andere spelers te pesten
4. **Window positie is cruciaal** - Moet exact in linkerbovenhoek staan
5. **Resolutie moet exact 1024x768 zijn** - Anders werkt detectie niet

---

## 📞 Snelle Referentie

```
1. Python installeren + PATH
2. pip install -r requirements.txt
3. Game: 1024x768 windowed, linkerbovenhoek
4. python top_left_B3D_prep_4_aimbot_v3.py (calibratie)
5. python main_074_3.6.5.py (start aimbot)
6. INSERT (open GUI)
7. Enable Aimbot
8. Spelen!
```

---

## 🎮 Game Setup Checklist

- [ ] Python 3.8+ geïnstalleerd
- [ ] Dependencies geïnstalleerd (pip install -r requirements.txt)
- [ ] Blockade 3D Classic: 1024x768 windowed
- [ ] Window in linkerbovenhoek
- [ ] Calibratie script gedraaid
- [ ] Main script gestart
- [ ] GUI geopend (INSERT)
- [ ] Aimbot enabled
- [ ] m700 of crossbow ge-equipped
- [ ] Chat disabled (optioneel)

**Veel succes! 🎯**

