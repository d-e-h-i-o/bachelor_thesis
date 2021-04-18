# Bachelor Thesis

## Project Structure
- `data/`
    - `html_pages/` The raw html_pages that were scraped by `scrape.py`
    - `parsed_laws/` The ouput from `extract.py`
    - `urls/` Contains urls from [gesetze.berlin.de](gesetze.berlin.de) for all [coronavirus laws in Berlin](https://de.wikipedia.org/wiki/SARS-CoV-2-Verordnungen_in_Berlin)
- `scripts/`: 
    - `scrape.py` Scrapes all data from the urls specified in `data/urls/`  to `data/html_pages/`
    - `extract.py` Extracts the laws from `data/html_pages/` to `data/parsed_laws/laws.json` in the [data format](#Format)
    
## Data format

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

I still have to inlcude dates.
## Next steps
- [ ] Improve `extract.py` (e.g. include dates) The parsing is still awkward
- [ ] Annotate (ongoing on [Hypothesis](https://hypothes.is/users/niklas_thesis))