
# PubMed Paper Fetcher

This command-line tool fetches scientific papers from PubMed based on user queries and exports specific metadata to a CSV file.

## 📁 Code Organization

```
pubmed_paper_fetcher/
│
├── pubmed_paper_fetcher/
│   ├── __init__.py
│   └── main.py       # Main logic to fetch, parse and output data
│
├── tests/
│   └── test_main.py  # (Optional) Unit tests
│
├── pyproject.toml    # Poetry configuration and dependencies
├── README.md         # Project documentation
└── .gitignore        # Git ignored files
```

## ⚙️ Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/your-username/pubmed_paper_fetcher.git
cd pubmed_paper_fetcher
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Run the program:
```bash
poetry run get-papers-list "cancer immunotherapy" --for-file output.csv
```

4. View help:
```bash
poetry run get-papers-list --help
```

## 📝 Features

- Fetch PubMed articles based on complex queries.
- Outputs include:
  - PubMed ID
  - Title
  - Publication Date
  - Non-academic Author(s)
  - Company Affiliations
  - Corresponding Author Email
- Debug mode supported.
- Output to CSV or console.


## 🧪 Running Tests

We use **pytest**. Install dev dependencies and run:

```bash
poetry install --with dev
poetry run pytest
```

## 🚀 Publishing to GitHub

1. **Initialize Git:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: PubMed paper fetcher CLI"
   ```

2. **Create a GitHub repository** (replace `<your-username>`):
   ```bash
   gh repo create <your-username>/pubmed_paper_fetcher --public --source=. --remote=origin -y
   ```

   > Requires the [GitHub CLI](https://cli.github.com/) and authentication via `gh auth login`.

3. **Push code:**
   ```bash
   git push -u origin main
   ```

4. **Set up GitHub Actions for CI (optional):** Create `.github/workflows/ci.yml` with:

   ```yaml
   name: CI

   on: [push]

   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         - uses: actions/setup-python@v4
           with:
             python-version: '3.11'
         - name: Install Poetry
           run: |
             curl -sSL https://install.python-poetry.org | python3 -
             echo "$HOME/.local/bin" >> $GITHUB_PATH
         - name: Install deps
           run: poetry install --with dev
         - name: Run tests
           run: poetry run pytest
   ```

Commit and push the workflow to enable automated testing on every push.

---

### ✨ Next Steps

- Expand `COMPANY_KEYWORDS` in `main.py` for improved company detection.
- Add more test cases under `tests/` to increase coverage.
- Consider packaging the tool on PyPI.
