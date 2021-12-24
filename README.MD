## Example Queries:


```
SELECT *
FROM realisations
WHERE realisation_id IN (
    SELECT realisation_id
    FROM "public"."realisation2gloss", "public"."glosses"
    WHERE realisation2gloss.gloss_id=glosses.gloss_id AND gloss='neg'
)
```

```
SELECT * FROM "public"."realisations"
WHERE realisation_id IN (
    SELECT distinct realisation_id
    FROM "public"."realisation2gloss", "public"."glosses"
    WHERE realisation2gloss.gloss_id = glosses.gloss_id
    AND glosses.gloss = 'ptcl'
   )
AND realisation_id IN (
    SELECT distinct realisation_id
    FROM "public"."realisation2gloss", "public"."glosses"
    WHERE realisation2gloss.gloss_id = glosses.gloss_id AND glosses.gloss = 'neg'
    )
```

```
SELECT * 
FROM "public"."realisations", "public"."formulas", "public"."languages"
WHERE realisations.formula_id = formulas.formula_id AND 
formulas.language_id = languages.language_id AND 
languages.language = 'sr'
```

```
SELECT * 
FROM "public"."realisations" JOIN "public"."intonations" using(intonation_id)
WHERE intonations.intonation='statement'
```

```
SELECT * 
FROM "public"."realisations" JOIN "public"."structures" using(structure_id)
WHERE structure='2'
```

```
SELECT *
FROM "public"."realisations", "public"."formulas", "public"."languages"
WHERE realisations.formula_id = formulas.formula_id AND 
formulas.language_id = languages.language_id
ORDER BY languages.language
```

```
SELECT formula, COUNT(realisation)
FROM "public"."realisations", "public"."formulas"
WHERE realisations.formula_id = formulas.formula_id 
GROUP BY formula
```

```
SELECT formula, COUNT(realisation)
FROM "public"."realisations", "public"."formulas"
WHERE realisations.formula_id = formulas.formula_id 
GROUP BY formula
ORDER BY count DESC
```

```
UPDATE "public"."realisations"
SET examples='eto kak slucilos'
WHERE realisation='eto kak'
```

```
DELETE FROM "public"."realisations"
WHERE realisation='eto kak'
```

```
SELECT * FROM "public"."realisations"
WHERE realisation_id in (
    SELECT distinct realisation_id
    FROM "public"."realisation2gloss", "public"."glosses"
    WHERE realisation2gloss.gloss_id = glosses.gloss_id
    AND glosses.gloss in ('neg', 'ptcl')
    GROUP BY realisation_id having COUNT(*) = 2
)
```

```
INSERT INTO languages (language) VALUES ('sv')
```

```
DELETE FROM languages WHERE language = 'sv'
```

```
INSERT INTO languages (language) VALUES ('sv');

INSERT INTO formulas (formula, language_id) VALUES ('hur det', (SELECT language_id FROM languages WHERE language = 'sv'));

INSERT INTO realisations (realisation, formula_id, intonation_id, examples) VALUES ('hur det', (SELECT formula_id FROM formulas WHERE formula='hur det'), (SELECT intonation_id FROM intonations WHERE intonation='exclamation'), '- Jag är galen! - Hur det?')
```

```
SELECT * FROM realisations
WHERE realisations.formula_id IN (
    SELECT formula_id
    FROM formulas
    WHERE formulas.language_id = (
        SELECT language_id
        FROM languages
        WHERE languages.language = 'sv'
    )
)
```

```
DELETE FROM formulas WHERE formula = 'hur det'
```

```
SELECT * FROM realisations WHERE realisation = 'hur det'
```

```
DELETE FROM languages WHERE language = 'sv'
```
