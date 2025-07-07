
import pytest
from unittest.mock import patch, MagicMock
import pubmed_paper_fetcher.main as main_mod

# Mocked XML response for efetch
MOCK_XML = """<?xml version=\"1.0\"?>
<PubmedArticleSet>
  <PubmedArticle>
    <MedlineCitation>
      <PMID>12345678</PMID>
      <Article>
        <ArticleTitle>Test Article</ArticleTitle>
        <AffiliationInfo>
          <Affiliation>ACME Biotech Inc., New York, USA. contact@acmebio.com</Affiliation>
        </AffiliationInfo>
        <AuthorList>
          <Author>
            <ForeName>Jane</ForeName>
            <LastName>Doe</LastName>
            <AffiliationInfo>
              <Affiliation>ACME Biotech Inc., New York, USA. jane.doe@acmebio.com</Affiliation>
            </AffiliationInfo>
          </Author>
        </AuthorList>
      </Article>
      <ArticleDate>
        <Year>2024</Year>
        <Month>12</Month>
        <Day>15</Day>
      </ArticleDate>
    </MedlineCitation>
  </PubmedArticle>
</PubmedArticleSet>"""


@patch("requests.get")
def test_search_and_fetch(mock_get):
    # Mock the esearch JSON response
    mock_esearch_resp = MagicMock()
    mock_esearch_resp.json.return_value = {
        "esearchresult": {
            "idlist": ["12345678"]
        }
    }
    mock_esearch_resp.text = ""

    # Mock the efetch XML response
    mock_efetch_resp = MagicMock()
    mock_efetch_resp.text = MOCK_XML

    # Side effects: first call esearch, second call efetch
    mock_get.side_effect = [mock_esearch_resp, mock_efetch_resp]

    pmids = main_mod.search_pubmed("test query")
    assert pmids == ["12345678"]

    xml_data = main_mod.fetch_details(pmids)
    article = xml_data.find('.//PubmedArticle')
    record = main_mod.extract_info(article)

    assert record["PubmedID"] == "12345678"
    assert record["Title"] == "Test Article"
    assert "ACME Biotech Inc." in record["Company Affiliation(s)"]
    assert record["Corresponding Author Email"].endswith("@acmebio.com")
