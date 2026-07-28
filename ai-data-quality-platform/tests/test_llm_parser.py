"""
test_llm_parser.py
=====================

RÔLE DE CE FICHIER
-------------------
Tests unitaires pour la partie "parsing" de src/llm/rule_generator.py —
vérifier que le code sait correctement parser/valider/nettoyer une
réponse LLM, SANS appeler la vraie API (on mocke la réponse).

CE QU'IL FAUT IMPLÉMENTER
--------------------------
1. `test_parses_clean_json_response()` :
   simule une réponse LLM déjà en JSON propre, vérifie que le parsing
   fonctionne et retourne la bonne structure Python.

2. `test_strips_markdown_code_fences()` :
   simule une réponse LLM du type :
       ```json
       [{"column": "amount", ...}]
       ```
   vérifie que le nettoyage retire bien les balises ```json avant de
   parser (cas très fréquent avec les LLM).

3. `test_validate_rules_rejects_missing_keys()` :
   simule une règle générée par le LLM à qui il manque une clé
   obligatoire (ex: pas de "rule_sql") — vérifie que `validate_rules()`
   la rejette et ne plante pas.

4. `test_validate_rules_accepts_well_formed_rules()` :
   vérifie qu'une règle bien formée passe la validation sans erreur.

5. `test_generate_rules_retries_on_invalid_json()` (avec mock) :
   utilise `unittest.mock.patch` pour simuler un `LLMClient.complete()`
   qui renvoie d'abord un JSON invalide, puis un JSON valide au 2e
   appel — vérifie que la logique de retry fonctionne.

COMMENT MOCKER L'APPEL LLM (exemple de pattern à utiliser)
----------------------------------------------------------------
    from unittest.mock import patch

    @patch("src.llm.llm_client.LLMClient.complete")
    def test_xxx(mock_complete):
        mock_complete.return_value = '[{"column": "amount", ...}]'
        ...

COMMENT LANCER
----------------
    pytest tests/test_llm_parser.py -v

POINTS D'ATTENTION
-------------------
- Ces tests ne doivent JAMAIS faire de vrai appel réseau — c'est tout
  l'intérêt du mock : tester la logique de parsing indépendamment de
  l'API externe (rapide, gratuit, déterministe).
"""

# TODO: import pytest, json
# TODO: from unittest.mock import patch
# TODO: from src.llm.rule_generator import generate_rules, validate_rules
# TODO: implémenter les tests décrits ci-dessus
