# Einfaches Python Blog Script
Dieses Script generiert eine Startseite mit Blogliste und baut Links zu den 
Blogeinträgen in `/blog/`. Dort sollte ein `#date` als Datum vorhanden sein.

## Template
Der Platzhalter `[#BLOG_INDEX#]` im `/template/index.html` generiert eine
HTML-Liste mit den Links zu den Einträgen. In `/template/index.html` ist die 
Vorlage für neue Blogposts.

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

## Upload
Der Inhalt des Public-Ordner muss hochgeladen werden.