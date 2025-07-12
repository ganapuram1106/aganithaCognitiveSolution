#!/usr/bin/env python3
"""
PubMed Research Paper Fetcher

A command-line tool that fetches research papers from PubMed based on a search query
and filters for papers with authors affiliated with pharmaceutical or biotech companies.
Results are exported as a CSV file.
"""

import argparse
import csv
import re
import sys
import time
from typing import List, Dict, Optional, Set
import requests
import pandas as pd
from Bio import Entrez

# Import configuration
try:
    from config import (
        PHARMA_KEYWORDS, COMPANY_KEYWORDS, COLLABORATION_KEYWORDS,
        ACADEMIC_INDUSTRY_KEYWORDS, SEARCH_CONFIG, OUTPUT_CONFIG
    )
except ImportError:
    # Fallback configuration if config.py is not available
    PHARMA_KEYWORDS = {
        'pharmaceutical', 'pharma', 'biotech', 'biotechnology', 'drug', 'medication',
        'therapeutics', 'pharmacology', 'clinical', 'trial', 'medicine', 'healthcare',
        'biopharmaceutical', 'biopharma', 'genetic', 'genomics', 'proteomics',
        'molecular', 'cell', 'therapy', 'vaccine', 'antibody', 'protein', 'enzyme'
    }
    COMPANY_KEYWORDS = {
        'pfizer', 'novartis', 'roche', 'johnson & johnson', 'merck', 'gsk', 'glaxosmithkline',
        'astrazeneca', 'sanofi', 'bayer', 'abbvie', 'amgen', 'biogen', 'gilead',
        'moderna', 'biontech', 'regeneron', 'eli lilly', 'bristol-myers squibb',
        'takeda', 'daiichi sankyo', 'astellas', 'boehringer ingelheim', 'novo nordisk',
        'genentech', 'celgene', 'incyte', 'vertex', 'alexion', 'biomarin', 'seattle genetics',
        'exelixis', 'clovis oncology', 'bluebird bio', 'crispr therapeutics', 'editas medicine',
        'intellia therapeutics', 'beam therapeutics', 'precision biosciences'
    }
    COLLABORATION_KEYWORDS = set()
    ACADEMIC_INDUSTRY_KEYWORDS = set()
    SEARCH_CONFIG = {'default_max_results': 100, 'rate_limit_delay': 0.1, 'timeout': 30, 'max_retries': 3}
    OUTPUT_CONFIG = {'default_filename': 'pubmed_results.csv', 'csv_encoding': 'utf-8', 'include_abstract': True, 'include_affiliations': True, 'truncate_long_fields': True, 'max_field_length': 1000}


class PubMedFetcher:
    """Fetches and filters PubMed research papers for pharmaceutical/biotech affiliations."""
    
    def __init__(self, email: str):
        """
        Initialize the PubMed fetcher.
        
        Args:
            email: Email address for NCBI E-utilities (required by NCBI)
        """
        Entrez.email = email
        self.pharma_keywords = PHARMA_KEYWORDS
        self.company_keywords = COMPANY_KEYWORDS
        self.collaboration_keywords = COLLABORATION_KEYWORDS
        self.academic_industry_keywords = ACADEMIC_INDUSTRY_KEYWORDS
        
        # Combine all keywords for comprehensive detection
        self.all_keywords = (
            self.pharma_keywords | 
            self.company_keywords | 
            self.collaboration_keywords | 
            self.academic_industry_keywords
        )
    
    def search_pubmed(self, query: str, max_results: int = None) -> List[str]:
        """
        Search PubMed for papers matching the query.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to retrieve
            
        Returns:
            List of PubMed IDs
        """
        if max_results is None:
            max_results = SEARCH_CONFIG['default_max_results']
            
        print(f"Searching PubMed for: '{query}'")
        
        try:
            # Search PubMed
            handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results, sort="relevance")
            record = Entrez.read(handle)
            handle.close()
            
            pmids = record["IdList"]
            print(f"Found {len(pmids)} papers")
            return pmids
            
        except Exception as e:
            print(f"Error searching PubMed: {e}")
            return []
    
    def has_pharma_affiliation(self, affiliation: str) -> bool:
        """
        Check if an affiliation contains pharmaceutical or biotech keywords.
        
        Args:
            affiliation: Author affiliation string
            
        Returns:
            True if affiliation contains pharma/biotech keywords
        """
        if not affiliation:
            return False
            
        affiliation_lower = affiliation.lower()
        
        # Check for company names
        for company in self.company_keywords:
            if company in affiliation_lower:
                return True
        
        # Check for pharmaceutical/biotech keywords
        for keyword in self.pharma_keywords:
            if keyword in affiliation_lower:
                return True
        
        # Check for collaboration keywords
        for keyword in self.collaboration_keywords:
            if keyword in affiliation_lower:
                return True
        
        # Check for academic-industry collaboration keywords
        for keyword in self.academic_industry_keywords:
            if keyword in affiliation_lower:
                return True
        
        return False
    
    def get_paper_details(self, pmid: str) -> Optional[Dict]:
        """
        Get detailed information for a specific paper.
        
        Args:
            pmid: PubMed ID
            
        Returns:
            Dictionary containing paper details or None if error
        """
        try:
            # Fetch paper details using XML format
            handle = Entrez.efetch(db="pubmed", id=pmid, rettype="xml", retmode="xml")
            record = Entrez.read(handle)
            handle.close()
            
            if not record:
                return None
            
            paper = record['PubmedArticle'][0]['MedlineCitation']['Article']
            
            # Extract basic information
            title = paper.get('ArticleTitle', '')
            abstract = ''
            if 'Abstract' in paper and 'AbstractText' in paper['Abstract']:
                abstract_texts = paper['Abstract']['AbstractText']
                if isinstance(abstract_texts, list):
                    abstract = ' '.join(abstract_texts)
                else:
                    abstract = str(abstract_texts)
            
            journal = paper.get('Journal', {}).get('Title', '')
            pub_date = ''
            if 'Journal' in paper and 'JournalIssue' in paper['Journal']:
                pub_info = paper['Journal']['JournalIssue'].get('PubDate', {})
                year = pub_info.get('Year', '')
                month = pub_info.get('Month', '')
                day = pub_info.get('Day', '')
                pub_date = f"{year} {month} {day}".strip()
            
            # Extract authors and affiliations
            authors = []
            affiliations = []
            has_pharma_author = False
            
            if 'AuthorList' in paper:
                for author in paper['AuthorList']:
                    if 'LastName' in author and 'ForeName' in author:
                        author_name = f"{author['ForeName']} {author['LastName']}"
                        authors.append(author_name)
                    
                    # Check for affiliations
                    if 'AffiliationInfo' in author:
                        for aff_info in author['AffiliationInfo']:
                            if 'Affiliation' in aff_info:
                                affiliation = aff_info['Affiliation']
                                affiliations.append(affiliation)
                                if self.has_pharma_affiliation(affiliation):
                                    has_pharma_author = True
            
            # Also check for general affiliations in the article
            if 'Affiliation' in paper:
                for affiliation in paper['Affiliation']:
                    affiliations.append(affiliation)
                    if self.has_pharma_affiliation(affiliation):
                        has_pharma_author = True
            
            # Truncate long fields if configured
            if OUTPUT_CONFIG.get('truncate_long_fields', True):
                max_length = OUTPUT_CONFIG.get('max_field_length', 1000)
                if len(abstract) > max_length:
                    abstract = abstract[:max_length] + "..."
                if len(title) > max_length:
                    title = title[:max_length] + "..."
            
            return {
                'pmid': pmid,
                'title': title,
                'abstract': abstract if OUTPUT_CONFIG.get('include_abstract', True) else '',
                'journal': journal,
                'publication_date': pub_date,
                'authors': '; '.join(authors) if authors else '',
                'affiliations': '; '.join(affiliations) if affiliations and OUTPUT_CONFIG.get('include_affiliations', True) else '',
                'has_pharma_affiliation': has_pharma_author
            }
            
        except Exception as e:
            print(f"Error fetching details for PMID {pmid}: {e}")
            return None
    
    def fetch_and_filter_papers(self, query: str, max_results: int = None) -> List[Dict]:
        """
        Fetch papers and filter for those with pharmaceutical/biotech affiliations.
        
        Args:
            query: Search query
            max_results: Maximum number of results to process
            
        Returns:
            List of papers with pharma/biotech affiliations
        """
        pmids = self.search_pubmed(query, max_results)
        
        if not pmids:
            return []
        
        filtered_papers = []
        print(f"Processing {len(pmids)} papers...")
        
        for i, pmid in enumerate(pmids, 1):
            print(f"Processing paper {i}/{len(pmids)} (PMID: {pmid})")
            
            paper_details = self.get_paper_details(pmid)
            
            if paper_details and paper_details['has_pharma_affiliation']:
                filtered_papers.append(paper_details)
                print(f"  ✓ Found pharma/biotech affiliation")
            else:
                print(f"  ✗ No pharma/biotech affiliation found")
            
            # Be respectful to NCBI servers
            time.sleep(SEARCH_CONFIG.get('rate_limit_delay', 0.1))
        
        print(f"\nFound {len(filtered_papers)} papers with pharmaceutical/biotech affiliations")
        return filtered_papers
    
    def export_to_csv(self, papers: List[Dict], output_file: str):
        """
        Export papers to CSV file.
        
        Args:
            papers: List of paper dictionaries
            output_file: Output CSV filename
        """
        if not papers:
            print("No papers to export")
            return
        
        try:
            df = pd.DataFrame(papers)
            
            # Reorder columns for better readability
            columns = ['pmid', 'title', 'authors', 'journal', 'publication_date', 
                      'affiliations', 'abstract', 'has_pharma_affiliation']
            # Only include columns that exist in the dataframe
            available_columns = [col for col in columns if col in df.columns]
            df = df[available_columns]
            
            df.to_csv(output_file, index=False, quoting=csv.QUOTE_ALL, 
                     encoding=OUTPUT_CONFIG.get('csv_encoding', 'utf-8'))
            print(f"Exported {len(papers)} papers to {output_file}")
            
        except Exception as e:
            print(f"Error exporting to CSV: {e}")


def main():
    """Main function to handle command-line interface."""
    parser = argparse.ArgumentParser(
        description="Fetch PubMed papers with pharmaceutical/biotech company affiliations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python pubmed_fetcher.py -q "cancer immunotherapy" -e "your.email@example.com"
  python pubmed_fetcher.py -q "COVID-19 vaccine" -e "researcher@university.edu" -o results.csv
  python pubmed_fetcher.py -q "diabetes treatment" -e "scientist@company.com" -m 50
        """
    )
    
    parser.add_argument(
        '-q', '--query',
        required=True,
        help='Search query for PubMed'
    )
    
    parser.add_argument(
        '-e', '--email',
        required=True,
        help='Email address for NCBI E-utilities (required by NCBI)'
    )
    
    parser.add_argument(
        '-o', '--output',
        default=OUTPUT_CONFIG.get('default_filename', 'pubmed_results.csv'),
        help=f'Output CSV filename (default: {OUTPUT_CONFIG.get("default_filename", "pubmed_results.csv")})'
    )
    
    parser.add_argument(
        '-m', '--max-results',
        type=int,
        default=SEARCH_CONFIG.get('default_max_results', 100),
        help=f'Maximum number of results to process (default: {SEARCH_CONFIG.get("default_max_results", 100)})'
    )
    
    args = parser.parse_args()
    
    # Validate email format
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, args.email):
        print("Error: Please provide a valid email address")
        sys.exit(1)
    
    # Create fetcher and process
    fetcher = PubMedFetcher(args.email)
    
    print("=" * 60)
    print("PubMed Research Paper Fetcher")
    print("Filtering for Pharmaceutical/Biotech Affiliations")
    print("=" * 60)
    
    papers = fetcher.fetch_and_filter_papers(args.query, args.max_results)
    
    if papers:
        fetcher.export_to_csv(papers, args.output)
        print(f"\nSummary:")
        print(f"- Total papers processed: {args.max_results}")
        print(f"- Papers with pharma/biotech affiliations: {len(papers)}")
        print(f"- Results saved to: {args.output}")
    else:
        print("\nNo papers with pharmaceutical/biotech affiliations found.")


if __name__ == "__main__":
    main() 