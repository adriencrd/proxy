README — Proxy tester (ultra rapide)

But
Tester rapidement une liste de proxys (fichier Https.txt) et sauvegarder les valides dans valid_proxies.txt.

Prérequis

Python 3.8+

requests : pip install requests

Pour SOCKS : pip install requests

Fichiers

proxy.py — script (lance le test)

Https.txt — liste de proxys (un par ligne, ex. 1.2.3.4:8080)

valid_proxies.txt — sortie (écrit au fur et à mesure)

Usage rapide

python proxy.py               # utilise Https.txt, timeout=1.5s, workers=400 (config par défaut)
python proxy.py MonFichier.txt 2 1 1.0 400
# args: [input_file] [attempts] [success_needed] [timeout_seconds] [max_workers]


Conseils pour la vitesse

Augmente max_workers (ex. 800) pour plus de parallélisme. 

Réduis timeout (ex. 1.0–1.5s) pour aller plus vite — attention aux faux négatifs.

Met success_needed à 1 pour valider dès 1 réussite.

Utilise https://example.com comme cible de test.

Remarques

Place Https.txt et proxy.py dans le même dossier.

Ne lance pas Https.txt — lance proxy.py.

Usage responsable : n’utilise pas de proxys pour des actions illégales.
