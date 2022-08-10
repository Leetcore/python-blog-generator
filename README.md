# Einfaches Python Blog Script
Dieses Script generiert eine Startseite mit Blogliste und baut Links zu den 
Blogeinträgen in `/blog/`. Dort sollte ein `#date` als Datum vorhanden sein.

## Template
Der Platzhalter `[#BLOG_INDEX#]` im `/template/template.html` generiert eine
HTML-Liste mit den Links zu den Einträgen.

## Installation
``` cmd
pip3 install -r requirements.txt
```

## Configuration
Blog URL und die Blogbeschreibung kann in der `config.toml` geändert werden.

## Nutzung
``` cmd
python3 generate-blog.py
```