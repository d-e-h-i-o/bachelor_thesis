# Bachelor Thesis

Everything is still WIP.
## Project Structure

- `scraping/`: 
    - `scrape.py` Scrapes all data from the urls specified in `urls/`  to `html_pages/`
    - `extract.py` Extracts the laws from `html_pages/` to `parsed_laws/` in the [data format](#Format)
    - `data/`
        - `html_pages/`
        - `parsed_laws/` 
        - `urls/` Contains urls from [gesetze.berlin.de](gesetze.berlin.de)
    
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

I'm not really sure whether that is the best format yet, but it can easily be modified.

## Next steps
- [ ] Improve `extract.py` (e.g. include dates)
- [ ] Annotate