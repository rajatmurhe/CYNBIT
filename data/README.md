# Data notes

`catalog.json` contains eight manually reviewed routing entries based on Cynbit's public website, accessed 29 October 2026. Source URLs, page sections and review dates travel with every match. Summaries are paraphrased. `search_terms`, discovery questions and next steps are authored for this prototype; they are not quotations or verified service commitments.

`dev_cases.json` is a small synthetic development set. `evaluation_cases.json` is a separate synthetic challenge set, written before the first evaluation run. Neither contains customer data. The retrieval model is fitted only on catalog text, never on these inquiry labels. Both sets were authored in the same project, so they are not an independent benchmark. Test cases are not used to select thresholds.

A maintainer should review the linked source when changing a catalog record, update `reviewed_on`, inspect the diff and rerun evaluation. No scraper runs at startup. A source disappearing or changing is not detected automatically.

Do not add customer inquiries, credentials, contact lists or exported briefs to this repository.
