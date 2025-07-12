# PubMed Research Paper Fetcher

A Python command-line tool that fetches research papers from PubMed based on a user-specified search query and filters for papers with authors affiliated with pharmaceutical or biotech companies. Results are exported as a CSV file containing essential metadata for each paper.

## Features

- **PubMed Search**: Search PubMed using custom queries
- **Pharmaceutical/Biotech Filtering**: Automatically identify papers with industry affiliations
- **Comprehensive Metadata**: Extract title, abstract, authors, journal, publication date, and affiliations
- **CSV Export**: Export results to a structured CSV file
- **Rate Limiting**: Respectful to NCBI servers with built-in delays
- **Flexible Configuration**: Customizable search parameters and output options

## Installation

1. **Clone or download the project files**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Dependencies

- `requests`: HTTP library for API calls
- `pandas`: Data manipulation and CSV export
- `biopython`: NCBI E-utilities interface
- `argparse`: Command-line argument parsing

## Usage

### Basic Usage

```bash
python pubmed_fetcher.py -q "your search query" -e "your.email@example.com"
```

### Advanced Usage

```bash
python pubmed_fetcher.py -q "cancer immunotherapy" -e "researcher@university.edu" -o results.csv -m 50
```

### Command Line Arguments

- `-q, --query`: Search query for PubMed (required)
- `-e, --email`: Email address for NCBI E-utilities (required)
- `-o, --output`: Output CSV filename (default: `pubmed_results.csv`)
- `-m, --max-results`: Maximum number of results to process (default: 100)

## Examples

### Example 1: Search for COVID-19 vaccine research
```bash
python pubmed_fetcher.py -q "COVID-19 vaccine" -e "scientist@company.com" -o covid_vaccine_papers.csv
```

### Example 2: Search for cancer treatment papers (limited results)
```bash
python pubmed_fetcher.py -q "cancer treatment" -e "researcher@university.edu" -m 25 -o cancer_papers.csv
```

### Example 3: Search for diabetes research
```bash
python pubmed_fetcher.py -q "diabetes mellitus type 2" -e "phd.student@institute.edu"
```

## Output Format

The tool generates a CSV file with the following columns:

- **pmid**: PubMed ID
- **title**: Paper title
- **authors**: Author names (semicolon-separated)
- **journal**: Journal name
- **publication_date**: Publication date
- **affiliations**: Author affiliations (semicolon-separated)
- **abstract**: Paper abstract
- **has_pharma_affiliation**: Boolean indicating if pharma/biotech affiliation was found

## Pharmaceutical/Biotech Detection

The tool identifies pharmaceutical and biotech affiliations using:

### Company Keywords
- Major pharmaceutical companies: Pfizer, Novartis, Roche, Johnson & Johnson, Merck, GSK, AstraZeneca, Sanofi, Bayer, AbbVie, Amgen, Biogen, Gilead, Moderna, BioNTech, Regeneron, Eli Lilly, Bristol-Myers Squibb, Takeda, Daiichi Sankyo, Astellas, Boehringer Ingelheim, Novo Nordisk, Genentech, Celgene, Incyte, Vertex, Alexion, BioMarin, Seattle Genetics, Exelixis, Clovis Oncology, Bluebird Bio, CRISPR Therapeutics, Editas Medicine, Intellia Therapeutics, Beam Therapeutics, Precision BioSciences

### Industry Keywords
- pharmaceutical, pharma, biotech, biotechnology, drug, medication, therapeutics, pharmacology, clinical, trial, medicine, healthcare, biopharmaceutical, biopharma, genetic, genomics, proteomics, molecular, cell, therapy, vaccine, antibody, protein, enzyme

## Important Notes

1. **Email Requirement**: NCBI requires a valid email address for E-utilities access. This is used for tracking and contacting users if necessary.

2. **Rate Limiting**: The tool includes a 0.1-second delay between requests to be respectful to NCBI servers.

3. **Search Results**: The tool processes papers in order of relevance as returned by PubMed.

4. **Affiliation Detection**: The tool checks both the AD (Affiliation) and FAU (Full Author) fields for pharmaceutical/biotech keywords.

## Error Handling

The tool includes comprehensive error handling for:
- Invalid email addresses
- Network connectivity issues
- PubMed API errors
- CSV export problems

## Limitations

- PubMed's E-utilities have rate limits and usage guidelines
- Affiliation detection relies on keyword matching and may not catch all variations
- Some papers may not have complete affiliation information
- The tool processes papers sequentially to respect server limits

## Contributing

Feel free to contribute by:
- Adding more pharmaceutical/biotech company keywords
- Improving affiliation detection algorithms
- Adding new output formats
- Enhancing error handling

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please check the error messages and ensure:
1. You have a valid email address
2. Your internet connection is stable
3. You're not exceeding NCBI's rate limits
4. Your search query is valid 