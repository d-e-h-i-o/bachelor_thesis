# Bachelor Thesis

This is the repository for my bachelor thesis `Claim retrieval and matching with laws for COVID-19 related legislation`.

It is concerned with the following goals:
- Define the claim extraction task (extract claims about Covid-19 related laws from newspaper articles)
- Define the law matching task (match those claims with the laws that are referenced in the claim)
- Collect datasets for both tasks
- Train models for both tasks

## Table of Contents
[1. Setup](#setup)  
[2. Training](#training)  
[3. Database](#database)  
[4. Legislation](#legislation)  

## Setup

```console
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Training

#### Claim extraction
````
Usage: training claim-extraction [OPTIONS]

Options:
  --epochs INTEGER                [default: 3]
  --cross-validation / --no-cross-validation
                                  [default: True]
  --inspect / --no-inspect        [default: False]
  --learning-rate FLOAT           [default: 2e-05]
  --filter-examples-without-claims / --no-filter-examples-without-claims
                                  [default: False]
  --help                          Show this message and exit.
````
e.g. ``python training claim-extraction --epochs 10``
#### Law matching
````
Usage: training law-matching [OPTIONS]

Options:
  --epochs INTEGER                [default: 3]
  --cross-validation / --no-cross-validation
                                  [default: True]
  --inspect / --no-inspect        [default: False]
  --learning-rate FLOAT           [default: 2e-05]
  --help                          Show this message and exit.
````
e.g. ``python training law-matching --epochs 10 --no-cross-validation --inspect``

## Database

The SQLite database is called `database.db`. It contains the claim extraction and law matching data.
See [initial_migration.sql](initial_migration.sql) for the data format or `sqlite3 database.db -cmd .schema`

## Legislation

The legislation text can be found in the [legislation folder](legislation). The json files contain the section with their
respective validity dates. Currently, the following legislation is there:
- 1\. InfSchMV
- 2\. InfSchMV
- 3\. InfSChMV
- Corona-ArbSchV
- GroßveranstVerbV
- SARS-CoV-2-EindV.json
- Zweite Pflegemaßnahmen-Covid-19-Verordnung.json
- 3\. PflegeM-Cov-19-V.json
- Krankenhaus-Covid-19-Verordnung.json
- SARS-CoV-2-Infektionsschutzverordnung.json

The are formatted like this:
```json
{
  "name": "SARS-CoV-2-Arbeitsschutzverordnung",
  "abbreviation": "Corona-ArbSchV",
  "sections": [
    {
      "sectionNumber": "1",
      "sectionTitle": "Ziel und Anwendungsbereich",
      "valid_from": "27.01.2021",
      "valid_to": "12.03.2021",
      "text": "..."
    }
  ]
}
```

#### Scraping and parsing new legislation
For scraping and parsing new legislation from [gesetze.berlin.de](gesetze.berlin.de), their url should be placed in the `law_scraping/data/urls` folder.

#### Scrape
``` 
Usage: law_scraping scrape [OPTIONS]

Options:
  --url TEXT             Specify if a singe url should be scraped
  --law TEXT             Name of the law
  --file-with-urls TEXT  File in data/urls/{file} with urls to scrape
  --help                 Show this message and exit.
```
e.g. `python law_scraping scrape --file_with_urls SchulHygCoV-19-VO.json`

#### Parse
```
Usage: law_scraping extract [OPTIONS]

Options:
  --prefix TEXT  Only extract those with prefix in name
  --help         Show this message and exit.
```
e.g. `python law_scraping extract --prefix Schul`