"""
notifier.py
=============

RÔLE DE CE FICHIER
-------------------
Envoyer des alertes automatiques (Slack, Teams, ou email) quand le
pipeline détecte un problème de qualité important : soit une règle SQL
avec un % de conformité trop bas, soit trop d'anomalies ML détectées.

CE QU'IL FAUT IMPLÉMENTER
--------------------------
1. `send_slack_alert(message: str, webhook_url: str)` :
   envoie une requête POST au webhook Slack (format JSON `{"text": message}`)
   via la librairie `requests`. Récupérer `webhook_url` depuis `.env`
   (SLACK_WEBHOOK_URL=...).

   Doc Slack Incoming Webhooks : créer un webhook depuis l'app Slack, le
   coller dans `.env`.

2. `send_teams_alert(message: str, webhook_url: str)` : équivalent pour
   Microsoft Teams si tu préfères (format de payload légèrement différent,
   utilise des "MessageCard" ou "Adaptive Cards").

3. `build_alert_message(quality_report: dict) -> str` :
   construit un message lisible à partir du rapport de qualité, ex :
   "🚨 Data Quality Alert — 3 règles en dessous de 90% de conformité.
   Règle la plus critique : 'amount >= 0' → 82% conforme (180 lignes en
   échec). 12 anomalies ML détectées non couvertes par les règles."

4. `should_alert(quality_report: dict, threshold: float = 0.9) -> bool` :
   logique de décision : est-ce qu'on déclenche une alerte ou pas ?
   (ex: si au moins une règle "high severity" est sous le seuil)

POINTS D'ATTENTION
-------------------
- Ne jamais spammer : ajoute une logique simple pour éviter d'envoyer
  la même alerte plusieurs fois de suite (ex: comparer avec la dernière
  alerte envoyée, stockée en base ou dans un fichier).
- Toujours logger l'envoi (succès/échec de l'appel webhook) séparément
  de l'alerte elle-même.
"""

# TODO: import requests, os, logging
# TODO: implémenter send_slack_alert, send_teams_alert, build_alert_message, should_alert
