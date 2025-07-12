# PubMed Research Paper Fetcher - Project Summary

## Overview

This project provides a comprehensive Python command-line tool for fetching research papers from PubMed and filtering them based on pharmaceutical or biotech company affiliations. The tool is designed for researchers, analysts, and professionals who need to identify industry-involved research publications.

## Project Structure

```
pubmed-research-fetcher/
├── pubmed_fetcher.py          # Main command-line tool
├── batch_processor.py         # Batch processing for multiple queries
├── config.py                  # Configuration and customization settings
├── test_pubmed_fetcher.py     # Test script for functionality
├── setup.py                   # Automated setup and installation
├── requirements.txt           # Python dependencies
├── README.md                  # Comprehensive documentation
├── PROJECT_SUMMARY.md         # This file
├── sample_queries.txt         # Sample queries for testing
└── .gitignore                 # Git ignore file
```

## Key Features

### 1. **PubMed Integration**
- Uses NCBI E-utilities API through Biopython
- Respects rate limits and server guidelines
- Comprehensive error handling for network issues

### 2. **Pharmaceutical/Biotech Detection**
- **Company Keywords**: 100+ major pharmaceutical and biotech companies
- **Industry Keywords**: 30+ pharmaceutical/biotech industry terms
- **Collaboration Keywords**: Academic-industry partnership indicators
- **Comprehensive Coverage**: Includes CROs, government institutions, and international organizations

### 3. **Flexible Search Options**
- Single query processing
- Batch processing from file or command line
- Customizable result limits
- Configurable output formats

### 4. **Rich Metadata Extraction**
- PubMed ID (PMID)
- Paper title and abstract
- Author names and affiliations
- Journal name and publication date
- Affiliation analysis results

### 5. **Export Capabilities**
- CSV export with proper encoding
- Configurable field inclusion/exclusion
- Field length truncation options
- Summary statistics generation

## Core Components

### 1. **PubMedFetcher Class** (`pubmed_fetcher.py`)
- Main class for PubMed interaction
- Affiliation detection algorithms
- Paper metadata extraction
- CSV export functionality

### 2. **BatchProcessor Class** (`batch_processor.py`)
- Multiple query processing
- Combined result management
- Statistical analysis
- Progress tracking

### 3. **Configuration System** (`config.py`)
- Customizable keyword lists
- Search behavior settings
- Output format options
- Easy modification for specific needs

## Installation and Setup

### Quick Start
```bash
# 1. Clone or download the project
# 2. Run the setup script
python setup.py

# 3. Test the installation
python test_pubmed_fetcher.py
```

### Manual Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Test imports
python -c "import requests, pandas, Bio; print('All modules imported successfully')"
```

## Usage Examples

### Basic Usage
```bash
# Single query
python pubmed_fetcher.py -q "cancer immunotherapy" -e "your.email@example.com"

# With custom output
python pubmed_fetcher.py -q "diabetes treatment" -e "researcher@university.edu" -o results.csv

# Limited results
python pubmed_fetcher.py -q "COVID-19 vaccine" -e "scientist@company.com" -m 25
```

### Batch Processing
```bash
# From file
python batch_processor.py -f sample_queries.txt -e "your.email@example.com"

# Multiple queries
python batch_processor.py -q "cancer immunotherapy" "diabetes treatment" -e "researcher@university.edu"
```

## Pharmaceutical/Biotech Detection Algorithm

The tool uses a multi-layered approach to identify industry affiliations:

### 1. **Company Name Matching**
- Direct company name detection (e.g., "Pfizer", "Novartis")
- Common variations and abbreviations (e.g., "GSK", "J&J")
- Subsidiary and division names

### 2. **Industry Keyword Detection**
- Pharmaceutical terms: "pharmaceutical", "pharma", "drug development"
- Biotechnology terms: "biotech", "biotechnology", "genetic engineering"
- Clinical research terms: "clinical trial", "drug safety", "regulatory affairs"

### 3. **Collaboration Indicators**
- Academic-industry partnerships
- Sponsored research indicators
- Industry funding mentions

### 4. **Institutional Coverage**
- Major pharmaceutical companies (top 20+)
- Biotech startups and established companies
- Contract Research Organizations (CROs)
- Government research institutions
- International regulatory bodies

## Output Format

The tool generates CSV files with the following structure:

| Column | Description |
|--------|-------------|
| pmid | PubMed ID |
| title | Paper title |
| authors | Author names (semicolon-separated) |
| journal | Journal name |
| publication_date | Publication date |
| affiliations | Author affiliations |
| abstract | Paper abstract |
| has_pharma_affiliation | Boolean indicator |
| search_query | Original search query (batch mode) |
| processed_date | Processing timestamp (batch mode) |

## Configuration Options

### Search Configuration
- Default result limits
- Rate limiting delays
- Timeout settings
- Retry mechanisms

### Output Configuration
- CSV encoding options
- Field inclusion/exclusion
- Field length limits
- Default filenames

### Keyword Customization
- Add/remove company names
- Modify industry keywords
- Update collaboration terms
- Custom detection rules

## Error Handling

The tool includes comprehensive error handling for:
- Network connectivity issues
- PubMed API errors
- Invalid email addresses
- File I/O problems
- Data parsing errors
- Rate limit violations

## Performance Considerations

### Rate Limiting
- 0.1-second delay between requests (configurable)
- Respects NCBI E-utilities guidelines
- Prevents server overload

### Memory Management
- Streams large result sets
- Configurable field truncation
- Efficient data structures

### Scalability
- Batch processing capabilities
- Configurable result limits
- Progress tracking for large datasets

## Limitations and Considerations

### Technical Limitations
- PubMed E-utilities rate limits
- Affiliation data availability varies
- Some papers may have incomplete metadata
- Keyword matching has false positive/negative potential

### Data Quality
- Affiliation information depends on journal submission
- Company name variations may be missed
- Academic-industry collaborations may be under-detected

### Usage Guidelines
- Requires valid email for NCBI access
- Respects fair use policies
- Recommended for research purposes only

## Future Enhancements

### Potential Improvements
1. **Enhanced Affiliation Detection**
   - Machine learning-based classification
   - Fuzzy string matching
   - Geographic location analysis

2. **Additional Data Sources**
   - CrossRef integration
   - Scopus API support
   - Web of Science integration

3. **Advanced Analytics**
   - Citation analysis
   - Collaboration network mapping
   - Trend analysis over time

4. **User Interface**
   - Web-based interface
   - Interactive query builder
   - Real-time result preview

## Support and Maintenance

### Documentation
- Comprehensive README
- Code comments and docstrings
- Usage examples
- Configuration guides

### Testing
- Unit tests for core functions
- Integration tests for API calls
- Sample data for validation

### Updates
- Regular dependency updates
- Keyword list maintenance
- Bug fixes and improvements

## License and Usage

This project is open source and available for research and educational purposes. Users should:
- Respect NCBI's terms of service
- Use responsibly and ethically
- Attribute appropriately in publications
- Report bugs and suggest improvements

## Conclusion

The PubMed Research Paper Fetcher provides a robust, flexible, and user-friendly solution for identifying pharmaceutical and biotech industry involvement in research publications. With its comprehensive detection algorithms, batch processing capabilities, and customizable configuration, it serves as a valuable tool for researchers, analysts, and professionals in the life sciences industry. 