# Baseline — 2026-06-16

Mesures prises sur la branche `main` (commit `831c7c7`) avant toute modification de la refonte, sur la branche `refonte-typeheavy`.

## Tailles répertoires

```
190M    .git
1.6M    static
 16M    _vendor
 15M    public  (après build propre)
```

## CSS

```
292K    public/css/main.4bfbe891095c59d94bbbdb462da10cdaf9dfd70692ab86df228819ddc9c80c3a.css
```

CSS généré par Hugo Blox / Tailwind, minifié. C'est la cible principale de la refonte : descendre à un fichier CSS écrit à la main, nettement plus léger.

## JS

```
80K     total (find public -name '*.js')
```

## Pages générées

```
Pages            :  93
Paginator pages  :   2
Non-page files   :   5
Static files     :   7
Processed images :   2
Aliases          :  32

Build time : 1388 ms
```

## Endpoints critiques

| Fichier | Présent |
|---|---|
| `public/almanach/index.json` | ✅ |
| `public/articles-aleatoires.json` | ✅ |
| `public/rhizome-curieux/index.json` | ✅ |
| `public/almanach/index.html` | ✅ absent (attendu) |

## Objectifs de la refonte (à comparer à la fin)

- CSS : de 292K → idéalement < 20K (CSS main écrit à la main, sans Tailwind)
- JS : réduction significative (suppression des moteurs JS non essentiels)
- Build : maintenir ou réduire le temps
- Pages : même nombre (aucune régression de contenu)
- Endpoints : inchangés
