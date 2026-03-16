# WaitTimer ⏰

Visuell väntetimer för barn. Hjälper barn att förstå och hantera väntetid med stora, tydliga siffror och roliga firanden!

## Funktioner

- Stor, lättläst nedräkning
- Preset-tider: 5, 10, 15 och 30 minuter
- Färgändringar när tiden nästan är ute (rött under 10 sekunder)
- Firande med emojis när tiden är slut
- Pausa/fortsätt och avbryt
- Mörkt, barnvänligt tema

## Installation

```bash
pip install PyGObject
python -m waittimer.main
```

Eller via setup.py:

```bash
pip install .
waittimer
```

## Krav

- Python 3.8+
- GTK4
- libadwaita
- PyGObject

### macOS

```bash
brew install gtk4 libadwaita pygobject3
pip install PyGObject
```

### Ubuntu/Debian

```bash
sudo apt install python3-gi gir1.2-gtk-4.0 gir1.2-adw-1
```

## Användning

Starta appen och tryck på en av tidsknapparna (5, 10, 15 eller 30 min). Timern räknar ner med stora siffror. När tiden är ute visas ett firande!

## Licens

MIT
