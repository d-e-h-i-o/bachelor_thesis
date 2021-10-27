# Bachelor Thesis

This is the repository for my bachelor thesis `Claim retrieval and matching with laws for COVID-19 related legislation`.

The contributions of this thesis are the following:
- A definition of the legal claim extraction task and the law matching task, including a model of underlying concepts like claims.
- Two labeled datasets for those tasks.
- Several trained models with benchmarks, including open source code for data pre-processing and model training.
- Proposals for future work.

## Table of Contents
[1. Setup](#setup)  
[2. Training](#training)  
[3. Database](#database)  
[4. Legislation](#legislation)  

## Setup

```console
git clone https://github.com/d-e-h-i-o/bachelor_thesis.git
cd bachelor_thesis
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

The SQLite database is called `database.db`. It contains the claim extraction and law matching data. For the data format 
see [initial_migration.sql](initial_migration.sql) or `sqlite3 database.db -cmd .schema`

## Legislation

The legislation text can be found in the [legislation folder](legislation). The json files contain the section with their
respective validity dates. Currently, the following legislation is there:
- 1\. InfSchMV (from 16.12.2020 to 06.03.2021)
- 2\. InfSchMV (from 07.03.2021 to 17.06.2021)
- 3\. InfSChMV (from 18.06.2021 to 06.11.2021)
- Corona-ArbSchV (from 27.01.2021 to 10.09.2021)
- GroßveranstVerbV (from 22.04.2020 to 26.06.2020)
- SARS-CoV-2-EindV (from 14.03.2020 to 17.03.2020)
- Zweite Pflegemaßnahmen-Covid-19-Verordnung (from 25.02.2021 to 23.06.2021)
- 3\. PflegeM-Cov-19-V (from 24.06.2021 to 10.09.2021)
- Krankenhaus-Covid-19-Verordnung (from 17.10.2020 to 27.02.2021)
- Zweite Krankenhaus-Covid-19-Verordnung (from 25.02.2021 to 14.08.2021)
- SARS-CoV-2-Infektionsschutzverordnung (from 27.06.2020 to 15.12.2020)
- SchulHygCoV-19-VO (from 28.11.2020 to 08.08.2021)
- SARS-CoV-2-EindmaßnV (from 18.03.2020 to 26.06.2020)

The filename is `{abbreviation}.json`. The format is:
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

### Scraping and parsing new legislation
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
e.g. `python law_scraping scrape --file-with-urls SchulHygCoV-19-VO.json`

#### Parse
```
Usage: law_scraping extract [OPTIONS]

Options:
  --prefix TEXT  Only extract those with prefix in name
  --help         Show this message and exit.
```
e.g. `python law_scraping extract --prefix Schul`