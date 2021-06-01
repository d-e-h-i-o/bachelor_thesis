# Bachelor Thesis

## Setup

```console
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Workflow

![full pipeline](assets/pipeline.png)

1. Annotate on [Hypothesis](https://hypothes.is/users/niklas_thesis)
2. Run annotation pipepline `python annotation_pipline/run_pipeline.py`
    1. -> Annotations are downloaded from Hypothesis
    2. -> Annotated webpages are saved to [Wayback Machine](https://web.archive.org/)
    3. -> Plaintext article is extraced with [NewsPlease](https://github.com/fhamborg/news-please)
    4. -> `(annotation_id, plaintext, claim_start, claim_end)` is saved to `extraction_data` table in database
    5. -> `(annotation_id, claim, referenced_law, date)` is saved to `matching_data` table in database
  3. Export data:  
     `sqlite3 -header -csv database.db "select plaintext, start, end from extraction_data;" > claim_extraction.csv`  
     `sqlite3 -header -csv database.db "select claim, reference, date from matching_data;" > claim_matching.csv`
4. Import csv to colab notebooks and run preprocessing function (TODO)
5. Train (TODO)

## Project Structure
- `annotation_pipeline` Fetches annotations from Hypothesis, processes them and save them to `database.db`
- `law_scraping`
  - `scrape.py` Scrapes all data from the urls specified in `data/urls/`  to `data/html_pages/`
  - `extract.py` Extracts the laws from `data/html_pages/` to `data/parsed_laws/laws.json` in the [data format](#Format)
  - `data/`
      - `html_pages/` The raw html_pages that were scraped by `scrape.py`
      - `parsed_laws/` The output from `extract.py`
      - `urls/` Contains urls from [gesetze.berlin.de](gesetze.berlin.de) for all [coronavirus laws in Berlin](https://de.wikipedia.org/wiki/SARS-CoV-2-Verordnungen_in_Berlin)
- `database.db` Contains `extraction_data` table and `matching_data` table
    
    
## Data format

### Database

The SQLite database is called `database.db`.

#### Table: extraction_data

| id                     | plaintext | start | end |
|------------------------|-----------|-------|-----|
| HtgxPqAlEeuJxauJOt9Xgg | In Berlin können Geschäfte...   | 513   | 610 |

The `id` is the annotation id from [Hypothesis](https://hypothes.is/users/niklas_thesis). The `plaintext` column contains
the extracted plaintext of the article. The `start` and `end` column contain the position of the claim. E.g. a claim can be
recovered from a row via `SELECT substr(plaintext,start,end-start+1) AS claim FROM extraction_data`.

#### Table: matching_data

| id                     | claim                                | reference              | date     |
|------------------------|--------------------------------------|------------------------|----------|
| k_sREqNEEeuuIJeXczF0ug | Kinder sind von der Maskenpflicht... | $ 4 (4) Nr. 1 InfSchMV | 19.04.21 |

The `id` is the annotation id from [Hypothesis](https://hypothes.is/users/niklas_thesis). The `claim` is the fulltext claim.
The `reference` is the law that is referenced in the claim.  
The `date` column is a bit more difficult to interpret. In general, it should be interpreted as the date when the claim was made. So it 
is often the date when the newspaper article was published. But in some cases, when the article speaks about future laws, the
date will be postdated. Consider the statement: "From Sunday on, the following rules are in place: ...". In this case,
the `date` column will contain a date when the rules are already in place. That is 
so that the preprocessing function can find the valid fulltext text of a referenced law.

### Laws

The parsed laws can currently be found under `data/parsed_laws` in a single `laws.json` file.

The are formatted like this:
```json
{
  "CoronaVVBE4rahmen_4020201107": {
    "§ 1": {
      "titleText": "Grundsätzliche Pflichten",
      "(1)": "{ Text of the first sentence}",
      "(2)": "..."
    },
    "§ 2": {
      "titleText": "..."
    }
  }
}
```
and can be accessed like this: `laws["CoronaVVBE4rahmen_4020201107"]["§ 1"]["(1)"]`

I still have to include dates.
## Next steps
- [ ] Improve `extract.py` (e.g. include dates) The parsing is still awkward
- [ ] Annotate (ongoing on [Hypothesis](https://hypothes.is/users/niklas_thesis))
- [ ] Extract plaintext for the articles that NewsPlease didn't handle correctly
- [ ] Setup preprocessing function for claim extraction task