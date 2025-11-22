# 🔍 Aimbot Debug Guide

## Probleem: Aimbot werkt niet

### Stap 1: Check GUI Status
1. Druk op **INSERT** om GUI te openen
2. Check of **"Aimbot: ON"** staat (groen)
3. Als het **"Aimbot: OFF"** zegt (rood), klik dan op **"Enable Aimbot"**

### Stap 2: Check TAB Toets
- **TAB pauzeert de aimbot!**
- Zorg dat TAB **NIET** ingedrukt is
- Laat TAB los als je het hebt ingedrukt

### Stap 3: Check Target Detection
De aimbot werkt alleen als er **targets worden gedetecteerd**:
- Je moet **in-game** zijn (niet in menu)
- Er moeten **spelers** in beeld zijn
- Gebruik **m700** of **crossbow** (geen muzzle flash)

### Stap 4: Check Terminal Output
Kijk in de terminal (waar je `python main_074_3.6.5.py` hebt gestart):
- Zie je `[DEBUG] Target detected!`? → Targets worden gevonden
- Zie je `[DEBUG] No target detected`? → Geen targets gevonden
- Zie je `Aimbot enabled: True`? → Aimbot is aan
- Zie je `TAB pressed: True`? → TAB is ingedrukt (pauzeert aimbot)

### Stap 5: Test Checklist
- [ ] GUI zegt "Aimbot: ON" (groen)
- [ ] TAB is NIET ingedrukt
- [ ] Je bent IN-GAME (niet in menu)
- [ ] Er zijn spelers in beeld
- [ ] Je hebt m700 of crossbow ge-equipped
- [ ] Terminal toont debug berichten

---

## Veelvoorkomende Problemen

### 1. "Aimbot: OFF" in GUI
**Oplossing**: Klik op "Enable Aimbot" knop

### 2. TAB is ingedrukt
**Oplossing**: Laat TAB los (TAB pauzeert aimbot)

### 3. Geen targets gedetecteerd
**Oplossing**: 
- Zorg dat je in-game bent
- Zorg dat er spelers in beeld zijn
- Check of je de juiste wapen hebt (m700/crossbow)

### 4. Aimbot werkt alleen soms
**Oplossing**: 
- Check MAX_AIM_DISTANCE in config (standaard 400px)
- Targets te ver weg worden niet ge-aimed
- Check accuracy settings (86% = soms missen)

---

## Test Commando

Herstart de aimbot met debug output:
```bash
python main_074_3.6.5.py
```

Kijk naar de terminal output voor debug berichten!

