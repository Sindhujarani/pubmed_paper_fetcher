
import argparse
import requests
import xml.etree.ElementTree as ET
import csv
import re
import sys

# Common company keywords (expandable)
COMPANY_KEYWORDS = ['pharma', 'biotech', 'inc', 'ltd', 'llc', 'gmbh', 'therapeutics', 'laboratories', 'corporation']

def parse_arguments():
    parser = argparse.ArgumentParser(description='Fetch PubMed articles with specific metadata.')
    parser.add_argument('query', type=str, help='PubMed search query in quotes')
    parser.add_argument('--for-file', type=str, help='Output filename (CSV format)')
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output')
    return parser.parse_args()

def debug_print(debug, message):
    if debug:
        print("[DEBUG]", message)

def search_pubmed(query, debug=False):
    url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
    params = {
        'db': 'pubmed',
        'term': query,
        'retmode': 'json',
        'retmax': '20'
    }
    response = requests.get(url, params=params)
    data = response.json()
    debug_print(debug, f"Search returned {len(data['esearchresult']['idlist'])} PMIDs")
    return data['esearchresult']['idlist']

def fetch_details(pmids, debug=False):
    url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi'
    params = {
        'db': 'pubmed',
        'id': ",".join(pmids),
        'retmode': 'xml'
    }
    response = requests.get(url, params=params)
    debug_print(debug, "Fetched XML records.")
    return ET.fromstring(response.text)

def extract_info(article):
    pmid = article.findtext('.//PMID')
    title = article.findtext('.//ArticleTitle')
    pub_date = article.findtext('.//PubDate/Year') or article.findtext('.//PubDate/MedlineDate', default='')

    non_academic_authors = []
    company_affiliations = []
    corresponding_email = ''

    for author in article.findall('.//Author'):
        aff = author.findtext('AffiliationInfo/Affiliation')
        if aff:
            aff_lower = aff.lower()
            is_company = any(kw in aff_lower for kw in COMPANY_KEYWORDS)
            is_academic = any(word in aff_lower for word in ['university', 'institute', 'college', 'school', 'hospital'])

            if is_company:
                company_affiliations.append(aff)
                name = ' '.join(filter(None, [author.findtext('ForeName'), author.findtext('LastName')]))
                non_academic_authors.append(name)

            email_match = re.search(r'[\w\.-]+@[\w\.-]+', aff)
            if email_match and not corresponding_email:
                corresponding_email = email_match.group()

    return {
        'PubmedID': pmid,
        'Title': title,
        'Publication Date': pub_date,
        'Non-academic Author(s)': '; '.join(non_academic_authors),
        'Company Affiliation(s)': '; '.join(company_affiliations),
        'Corresponding Author Email': corresponding_email
    }

def write_to_csv(records, filename):
    fieldnames = ['PubmedID', 'Title', 'Publication Date',
                  'Non-academic Author(s)', 'Company Affiliation(s)', 'Corresponding Author Email']
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            writer.writerow(record)

def print_records(records):
    for record in records:
        print("\n".join(f"{key}: {value}" for key, value in record.items()))
        print("-" * 50)

def main():
    args = parse_arguments()
    debug = args.debug

    try:
        pmids = search_pubmed(args.query, debug)
        xml_data = fetch_details(pmids, debug)

        records = []
        for article in xml_data.findall('.//PubmedArticle'):
            info = extract_info(article)
            records.append(info)

        if args.for_file:
            write_to_csv(records, args.for_file)
            print(f"✅ Results saved to {args.for_file}")
        else:
            print_records(records)

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        if debug:
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()
