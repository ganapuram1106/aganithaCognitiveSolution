"""
Configuration file for PubMed Research Paper Fetcher

This file contains customizable settings for pharmaceutical and biotech company detection.
Users can modify these lists to add or remove keywords and company names.
"""

# Pharmaceutical and biotech industry keywords
PHARMA_KEYWORDS = {
    'pharmaceutical', 'pharma', 'biotech', 'biotechnology', 'drug', 'medication',
    'therapeutics', 'pharmacology', 'clinical', 'trial', 'medicine', 'healthcare',
    'biopharmaceutical', 'biopharma', 'genetic', 'genomics', 'proteomics',
    'molecular', 'cell', 'therapy', 'vaccine', 'antibody', 'protein', 'enzyme',
    'drug discovery', 'drug development', 'clinical research', 'clinical development',
    'regulatory affairs', 'medical affairs', 'research and development', 'r&d',
    'drug safety', 'pharmacovigilance', 'medical device', 'diagnostic',
    'precision medicine', 'personalized medicine', 'targeted therapy',
    'immunotherapy', 'gene therapy', 'cell therapy', 'stem cell',
    'biomarker', 'companion diagnostic', 'orphan drug', 'rare disease'
}

# Major pharmaceutical and biotech company names
COMPANY_KEYWORDS = {
    # Top 20 Pharmaceutical Companies
    'pfizer', 'novartis', 'roche', 'johnson & johnson', 'merck', 'gsk', 'glaxosmithkline',
    'astrazeneca', 'sanofi', 'bayer', 'abbvie', 'amgen', 'biogen', 'gilead',
    'moderna', 'biontech', 'regeneron', 'eli lilly', 'bristol-myers squibb',
    'takeda', 'daiichi sankyo', 'astellas', 'boehringer ingelheim', 'novo nordisk',
    
    # Biotech Companies
    'genentech', 'celgene', 'incyte', 'vertex', 'alexion', 'biomarin', 'seattle genetics',
    'exelixis', 'clovis oncology', 'bluebird bio', 'crispr therapeutics', 'editas medicine',
    'intellia therapeutics', 'beam therapeutics', 'precision biosciences',
    
    # Additional Major Companies
    'janssen', 'bristol myers', 'bristol-myers', 'merck sharp & dohme', 'msd',
    'roche pharmaceuticals', 'genentech inc', 'genentech, inc', 'roche diagnostics',
    'novartis pharmaceuticals', 'novartis institutes', 'pfizer inc', 'pfizer, inc',
    'astrazeneca plc', 'astrazeneca pharmaceuticals', 'sanofi aventis', 'sanofi-aventis',
    'bayer healthcare', 'bayer pharmaceuticals', 'abbvie inc', 'abbvie, inc',
    'amgen inc', 'amgen, inc', 'biogen idec', 'biogen-idec', 'gilead sciences',
    'gilead sciences inc', 'gilead sciences, inc', 'moderna therapeutics',
    'moderna inc', 'moderna, inc', 'biontech se', 'biontech ag', 'regeneron pharmaceuticals',
    'regeneron inc', 'regeneron, inc', 'eli lilly and company', 'lilly', 'eli lilly',
    'bristol-myers squibb company', 'bristol-myers squibb co', 'takeda pharmaceutical',
    'takeda pharmaceuticals', 'daiichi sankyo co', 'daiichi sankyo company',
    'astellas pharma', 'astellas pharmaceutical', 'boehringer ingelheim pharmaceuticals',
    'boehringer ingelheim pharma', 'novo nordisk a/s', 'novo nordisk as',
    
    # Contract Research Organizations (CROs) and Service Providers
    'iqvia', 'covance', 'labcorp', 'parexel', 'icon plc', 'icon plc', 'ppd',
    'syneos health', 'medpace', 'pacific biosciences', 'illumina', 'thermo fisher scientific',
    'agilent technologies', 'waters corporation', 'perkinelmer', 'bio-rad laboratories',
    'qiagen', 'roche molecular systems', 'abbott laboratories', 'abbott',
    'beckman coulter', 'beckman coulter inc', 'beckman coulter, inc',
    
    # Academic Medical Centers with Industry Partnerships
    'harvard medical school', 'stanford medicine', 'ucsf', 'university of california san francisco',
    'johns hopkins medicine', 'mayo clinic', 'cleveland clinic', 'md anderson cancer center',
    'memorial sloan kettering', 'dana-farber cancer institute', 'fred hutchinson cancer center',
    'sloan kettering', 'memorial sloan-kettering', 'fred hutch', 'fred hutchinson',
    
    # Government Research Institutions
    'nih', 'national institutes of health', 'nci', 'national cancer institute',
    'fda', 'food and drug administration', 'cdc', 'centers for disease control',
    'nhlbi', 'national heart lung and blood institute', 'nimh', 'national institute of mental health',
    
    # International Organizations
    'who', 'world health organization', 'ema', 'european medicines agency',
    'health canada', 'pmda', 'pharmaceuticals and medical devices agency',
    'tga', 'therapeutic goods administration'
}

# Additional keywords that might indicate industry collaboration
COLLABORATION_KEYWORDS = {
    'sponsored by', 'funded by', 'supported by', 'in collaboration with',
    'partnership with', 'joint research', 'industry collaboration',
    'pharmaceutical industry', 'biotechnology industry', 'drug industry',
    'clinical trial sponsor', 'study sponsor', 'research sponsor',
    'commercial support', 'industry support', 'corporate funding',
    'pharmaceutical company', 'biotech company', 'drug company',
    'industry partner', 'commercial partner', 'corporate partner'
}

# Keywords that might indicate academic-industry collaboration
ACADEMIC_INDUSTRY_KEYWORDS = {
    'university-industry', 'academic-industry', 'academia-industry',
    'university corporate', 'academic corporate', 'academia corporate',
    'university pharmaceutical', 'academic pharmaceutical', 'academia pharmaceutical',
    'university biotech', 'academic biotech', 'academia biotech',
    'university drug', 'academic drug', 'academia drug',
    'university medicine', 'academic medicine', 'academia medicine',
    'university healthcare', 'academic healthcare', 'academia healthcare'
}

# Configuration for search behavior
SEARCH_CONFIG = {
    'default_max_results': 100,
    'rate_limit_delay': 0.1,  # seconds between requests
    'timeout': 30,  # seconds for API requests
    'max_retries': 3,  # number of retries for failed requests
}

# Output configuration
OUTPUT_CONFIG = {
    'default_filename': 'pubmed_results.csv',
    'csv_encoding': 'utf-8',
    'include_abstract': True,
    'include_affiliations': True,
    'truncate_long_fields': True,
    'max_field_length': 1000,  # characters
} 