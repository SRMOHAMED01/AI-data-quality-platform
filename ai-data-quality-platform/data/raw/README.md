# data/raw/

## À FAIRE ICI
Ce dossier contient les données brutes, non modifiées, telles qu'elles arrivent
de la source (aucune transformation, aucun nettoyage).

## Quoi mettre dedans
- Un dataset financier réaliste. Recommandation : dataset Kaggle "Credit Card
  Fraud Detection" (https://www.kaggle.com/mlg-ulb/creditcardfraud) ou un
  dataset de transactions e-commerce.
- Si tu n'as pas de dataset externe, génère-en un synthétique avec un script
  Python (Faker + numpy) qui simule : id, montant, email, date, statut,
  méthode de paiement, pays.

## Bonnes pratiques
- Ne jamais versionner ces fichiers dans Git s'ils sont volumineux (> quelques
  Mo) — ajoute-les au `.gitignore` et documente juste comment les régénérer
  ou les télécharger.
- Garde toujours une copie brute intacte : les couches suivantes (nettoyage,
  règles, ML) ne doivent JAMAIS écraser ce dossier.
