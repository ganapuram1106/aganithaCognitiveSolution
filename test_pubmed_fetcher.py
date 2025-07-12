#!/usr/bin/env python3
"""
Test script for PubMed Research Paper Fetcher

This script demonstrates how to use the PubMedFetcher class programmatically.
"""

import sys
import os
from pubmed_fetcher import PubMedFetcher


def test_pubmed_fetcher():
    """Test the PubMed fetcher with a sample query."""
    
    # Test configuration
    email = "test@example.com"  # Replace with your email
    query = "cancer immunotherapy"
    max_results = 10  # Small number for testing
    
    print("Testing PubMed Research Paper Fetcher")
    print("=" * 50)
    print(f"Query: {query}")
    print(f"Max results: {max_results}")
    print(f"Email: {email}")
    print()
    
    try:
        # Create fetcher instance
        fetcher = PubMedFetcher(email)
        
        # Search and filter papers
        papers = fetcher.fetch_and_filter_papers(query, max_results)
        
        if papers:
            print(f"\nFound {len(papers)} papers with pharmaceutical/biotech affiliations:")
            print("-" * 50)
            
            for i, paper in enumerate(papers, 1):
                print(f"\n{i}. PMID: {paper['pmid']}")
                print(f"   Title: {paper['title'][:100]}...")
                print(f"   Journal: {paper['journal']}")
                print(f"   Authors: {paper['authors'][:80]}...")
                print(f"   Date: {paper['publication_date']}")
            
            # Export to CSV
            output_file = "test_results.csv"
            fetcher.export_to_csv(papers, output_file)
            print(f"\nResults exported to: {output_file}")
            
        else:
            print("No papers with pharmaceutical/biotech affiliations found.")
            
    except Exception as e:
        print(f"Error during testing: {e}")
        return False
    
    return True


if __name__ == "__main__":
    print("Note: This is a test script. Please ensure you have:")
    print("1. Installed all dependencies: pip install -r requirements.txt")
    print("2. A valid email address for NCBI E-utilities")
    print("3. Internet connection")
    print()
    
    success = test_pubmed_fetcher()
    
    if success:
        print("\nTest completed successfully!")
    else:
        print("\nTest failed. Please check the error messages above.")
        sys.exit(1) 