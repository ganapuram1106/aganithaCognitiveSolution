#!/usr/bin/env python3
"""
Batch Processor for PubMed Research Paper Fetcher

This script allows processing multiple search queries and combining results into a single CSV file.
"""

import argparse
import csv
import os
import sys
from datetime import datetime
from typing import List, Dict
import pandas as pd
from pubmed_fetcher import PubMedFetcher


class BatchProcessor:
    """Process multiple PubMed search queries and combine results."""
    
    def __init__(self, email: str):
        """
        Initialize the batch processor.
        
        Args:
            email: Email address for NCBI E-utilities
        """
        self.email = email
        self.fetcher = PubMedFetcher(email)
        self.all_results = []
    
    def process_query(self, query: str, max_results: int = 50, query_name: str = None) -> List[Dict]:
        """
        Process a single query and return results.
        
        Args:
            query: Search query
            max_results: Maximum number of results to process
            query_name: Optional name for the query (for tracking)
            
        Returns:
            List of papers with pharma/biotech affiliations
        """
        print(f"\n{'='*60}")
        if query_name:
            print(f"Processing Query: {query_name}")
        print(f"Search Term: {query}")
        print(f"Max Results: {max_results}")
        print(f"{'='*60}")
        
        papers = self.fetcher.fetch_and_filter_papers(query, max_results)
        
        # Add query information to each paper
        for paper in papers:
            paper['search_query'] = query
            paper['query_name'] = query_name or query
        
        return papers
    
    def process_queries_from_file(self, queries_file: str, max_results_per_query: int = 50) -> List[Dict]:
        """
        Process queries from a text file.
        
        Args:
            queries_file: Path to file containing queries (one per line)
            max_results_per_query: Maximum results per query
            
        Returns:
            Combined list of all papers
        """
        if not os.path.exists(queries_file):
            print(f"Error: Queries file '{queries_file}' not found.")
            return []
        
        all_papers = []
        
        try:
            with open(queries_file, 'r', encoding='utf-8') as f:
                queries = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
            print(f"Found {len(queries)} queries in file: {queries_file}")
            
            for i, query in enumerate(queries, 1):
                print(f"\nProcessing query {i}/{len(queries)}")
                papers = self.process_query(query, max_results_per_query, f"Query_{i}")
                all_papers.extend(papers)
                
        except Exception as e:
            print(f"Error reading queries file: {e}")
            return []
        
        return all_papers
    
    def process_queries_from_list(self, queries: List[str], max_results_per_query: int = 50) -> List[Dict]:
        """
        Process a list of queries.
        
        Args:
            queries: List of search queries
            max_results_per_query: Maximum results per query
            
        Returns:
            Combined list of all papers
        """
        all_papers = []
        
        for i, query in enumerate(queries, 1):
            print(f"\nProcessing query {i}/{len(queries)}")
            papers = self.process_query(query, max_results_per_query, f"Query_{i}")
            all_papers.extend(papers)
        
        return all_papers
    
    def export_combined_results(self, papers: List[Dict], output_file: str):
        """
        Export combined results to CSV with additional metadata.
        
        Args:
            papers: List of all papers
            output_file: Output CSV filename
        """
        if not papers:
            print("No papers to export")
            return
        
        try:
            df = pd.DataFrame(papers)
            
            # Add timestamp
            df['processed_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Reorder columns for better readability
            columns = ['pmid', 'title', 'authors', 'journal', 'publication_date', 
                      'affiliations', 'abstract', 'search_query', 'query_name', 
                      'has_pharma_affiliation', 'processed_date']
            
            # Only include columns that exist in the dataframe
            available_columns = [col for col in columns if col in df.columns]
            df = df[available_columns]
            
            df.to_csv(output_file, index=False, quoting=csv.QUOTE_ALL)
            print(f"\nExported {len(papers)} papers to {output_file}")
            
            # Print summary statistics
            self.print_summary_statistics(df)
            
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
    
    def print_summary_statistics(self, df: pd.DataFrame):
        """
        Print summary statistics for the results.
        
        Args:
            df: DataFrame containing the results
        """
        print(f"\n{'='*60}")
        print("SUMMARY STATISTICS")
        print(f"{'='*60}")
        print(f"Total papers found: {len(df)}")
        
        if 'query_name' in df.columns:
            print(f"\nPapers per query:")
            query_counts = df['query_name'].value_counts()
            for query, count in query_counts.items():
                print(f"  {query}: {count} papers")
        
        if 'journal' in df.columns:
            print(f"\nTop journals:")
            journal_counts = df['journal'].value_counts().head(10)
            for journal, count in journal_counts.items():
                print(f"  {journal}: {count} papers")
        
        if 'publication_date' in df.columns:
            print(f"\nPublication years:")
            # Extract year from publication date
            try:
                df['year'] = df['publication_date'].str[:4]
                year_counts = df['year'].value_counts().sort_index()
                for year, count in year_counts.items():
                    print(f"  {year}: {count} papers")
            except:
                pass


def main():
    """Main function for batch processing."""
    parser = argparse.ArgumentParser(
        description="Batch process multiple PubMed queries for pharmaceutical/biotech affiliations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process queries from a file
  python batch_processor.py -f queries.txt -e "your.email@example.com" -o batch_results.csv
  
  # Process specific queries
  python batch_processor.py -q "cancer immunotherapy" "diabetes treatment" -e "researcher@university.edu"
  
  # Process with custom settings
  python batch_processor.py -f queries.txt -e "scientist@company.com" -m 25 -o results.csv
        """
    )
    
    parser.add_argument(
        '-e', '--email',
        required=True,
        help='Email address for NCBI E-utilities (required by NCBI)'
    )
    
    parser.add_argument(
        '-f', '--file',
        help='File containing search queries (one per line)'
    )
    
    parser.add_argument(
        '-q', '--queries',
        nargs='+',
        help='List of search queries'
    )
    
    parser.add_argument(
        '-o', '--output',
        default=f'batch_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
        help='Output CSV filename'
    )
    
    parser.add_argument(
        '-m', '--max-results-per-query',
        type=int,
        default=50,
        help='Maximum number of results per query (default: 50)'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.file and not args.queries:
        print("Error: You must specify either a file (-f) or a list of queries (-q)")
        sys.exit(1)
    
    if args.file and args.queries:
        print("Error: You cannot specify both a file and queries. Use one or the other.")
        sys.exit(1)
    
    # Create processor
    processor = BatchProcessor(args.email)
    
    print("=" * 60)
    print("PubMed Batch Processor")
    print("Processing Multiple Queries for Pharmaceutical/Biotech Affiliations")
    print("=" * 60)
    
    # Process queries
    if args.file:
        papers = processor.process_queries_from_file(args.file, args.max_results_per_query)
    else:
        papers = processor.process_queries_from_list(args.queries, args.max_results_per_query)
    
    # Export results
    if papers:
        processor.export_combined_results(papers, args.output)
        print(f"\nBatch processing completed successfully!")
        print(f"Results saved to: {args.output}")
    else:
        print("\nNo papers with pharmaceutical/biotech affiliations found.")


if __name__ == "__main__":
    main() 