"""
Multi-source citation analyzer with cross-validation.
Supports OpenAlex, Semantic Scholar, and OpenCitations.
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging
import requests

logger = logging.getLogger(__name__)


class CitationAnalyzer:
    """Analyze citations from multiple academic sources with cross-validation."""

    def __init__(self, cache_dir: str = "outputs/intermediates/citations", cache_days: int = 7):
        """
        Initialize CitationAnalyzer.

        Args:
            cache_dir: Directory to store API response cache
            cache_days: Number of days to keep cache entries
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_days = cache_days

        # OpenAlex base URL
        self.openalex_base = "https://api.openalex.org"

        # Initialize APIs (to be implemented in Phase 2)
        self.s2_client = None
        self.opencitations_base = "https://opencitations.net/api/v1"

        # Track available sources
        self.sources = ["openalex"]  # OpenAlex is always available

    def _get_cache_key(self, identifier: str) -> str:
        """Generate cache key from identifier."""
        return hashlib.md5(identifier.encode()).hexdigest()

    def _get_cached(self, cache_key: str) -> Optional[Dict]:
        """Retrieve cached data if not expired."""
        cache_file = self.cache_dir / f"{cache_key}.json"
        if not cache_file.exists():
            return None

        try:
            with open(cache_file) as f:
                cached = json.load(f)

            # Check expiration
            cached_time = datetime.fromisoformat(cached['timestamp'])
            if datetime.now() - cached_time > timedelta(days=self.cache_days):
                logger.debug(f"Cache expired for key: {cache_key}")
                return None

            logger.debug(f"Cache hit for key: {cache_key}")
            return cached['data']
        except Exception as e:
            logger.warning(f"Error reading cache: {e}")
            return None

    def _save_cache(self, cache_key: str, data: Dict):
        """Save data to cache with timestamp."""
        cache_file = self.cache_dir / f"{cache_key}.json"
        cache_data = {
            'timestamp': datetime.now().isoformat(),
            'data': data
        }
        try:
            with open(cache_file, 'w') as f:
                json.dump(cache_data, f, indent=2)
            logger.debug(f"Saved cache for key: {cache_key}")
        except Exception as e:
            logger.warning(f"Error saving cache: {e}")

    def get_paper_id_openalex(self, title: str, authors: str = None, year: int = None) -> Optional[Dict]:
        """
        Phase 1 Task 1: Query OpenAlex to get paper ID and metadata.

        Args:
            title: Paper title
            authors: Author names (optional)
            year: Publication year (optional)

        Returns:
            Dict with paper metadata including openalex_id, doi, title, etc.
        """
        # Check cache first
        cache_key = self._get_cache_key(f"openalex_{title}_{authors}_{year}")
        cached = self._get_cached(cache_key)
        if cached:
            return cached

        try:
            # Build search query
            search_url = f"{self.openalex_base}/works"
            params = {
                "search": title,
                "per_page": 10  # Get top 10 results to find best match
            }

            # Add mailto parameter for polite pool (faster response)
            params["mailto"] = "research@example.com"

            logger.info(f"Querying OpenAlex for: {title}")
            response = requests.get(search_url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()
            results = data.get('results', [])

            # Debug: Log top 3 results
            logger.info(f"Found {len(results)} results. Top 3:")
            for i, r in enumerate(results[:3]):
                logger.info(f"  {i+1}. {r.get('title') or r.get('display_name')} ({r.get('publication_year')}) - {r.get('cited_by_count')} citations")

            if not results:
                logger.warning(f"No results found for: {title}")
                return None

            # Find best matching paper
            best_match = self._find_best_match(results, title, authors, year)

            if not best_match:
                logger.warning(f"No good match found for: {title}")
                return None

            # Extract relevant information
            # Handle both 'title' and 'display_name' fields
            paper_title = best_match.get('title') or best_match.get('display_name')

            # Safely extract venue
            venue = None
            primary_location = best_match.get('primary_location')
            if primary_location and isinstance(primary_location, dict):
                source = primary_location.get('source')
                if source and isinstance(source, dict):
                    venue = source.get('display_name')

            result = {
                "openalex_id": best_match.get('id', '').replace('https://openalex.org/', ''),
                "doi": best_match.get('doi'),
                "title": paper_title,
                "display_name": paper_title,
                "publication_year": best_match.get('publication_year'),
                "cited_by_count": best_match.get('cited_by_count', 0),
                "authors": [a.get('author', {}).get('display_name', '') if a.get('author') else '' for a in best_match.get('authorships', [])],
                "venue": venue,
                "url": best_match.get('id')
            }

            # Save to cache
            self._save_cache(cache_key, result)

            logger.info(f"Found paper: {result['title']} (ID: {result['openalex_id']}, Citations: {result['cited_by_count']})")
            return result

        except requests.RequestException as e:
            logger.error(f"OpenAlex API error: {e}")
            return None
        except Exception as e:
            logger.error(f"Error getting paper ID: {e}")
            return None

    def _find_best_match(self, results: List[Dict], title: str, authors: str = None, year: int = None) -> Optional[Dict]:
        """
        Find best matching paper from search results.

        Args:
            results: List of OpenAlex search results
            title: Original title to match
            authors: Author names (optional)
            year: Publication year (optional)

        Returns:
            Best matching result or None
        """
        if not results:
            return None

        # Score each result
        scored_results = []
        original_title_lower = title.lower()
        original_words = set(original_title_lower.split())

        for result in results:
            score = 0
            result_title = (result.get('title') or result.get('display_name', '')).lower()

            # Word overlap similarity (most important)
            result_words = set(result_title.split())
            overlap = len(original_words & result_words)
            overlap_ratio = overlap / max(len(original_words), 1)
            score += overlap_ratio * 100  # Up to 100 points

            # Year matching
            if year and result.get('publication_year') == year:
                score += 50

            # Citation count (prefer more cited papers)
            score += min(result.get('cited_by_count', 0) / 100, 20)  # Max 20 points

            scored_results.append((score, result, overlap_ratio))

        # Sort by score descending
        scored_results.sort(key=lambda x: x[0], reverse=True)

        # Only return if there's reasonable title overlap (at least 20% of words match)
        if scored_results and scored_results[0][2] >= 0.2:
            return scored_results[0][1]

        # If no good match, return None
        if scored_results:
            logger.info(f"No good title match found (best overlap: {scored_results[0][2]:.2f})")
        return None

    def fetch_citations_openalex(self, openalex_id: str) -> List[Dict]:
        """
        Phase 1 Task 2: Fetch citing papers from OpenAlex.

        Args:
            openalex_id: OpenAlex work ID (e.g., "W123456789")

        Returns:
            List of citing papers with metadata
        """
        # Check cache
        cache_key = self._get_cache_key(f"openalex_citations_{openalex_id}")
        cached = self._get_cached(cache_key)
        if cached:
            return cached

        try:
            # Construct full URL if needed
            if not openalex_id.startswith('https://'):
                work_id = f"https://openalex.org/{openalex_id}"
            else:
                work_id = openalex_id

            citations_url = f"{self.openalex_base}/works"
            params = {
                "filter": f"cites:{work_id}",
                "per_page": 200,  # Get up to 200 citations
                "mailto": "research@example.com"
            }

            logger.info(f"Fetching citations for: {openalex_id}")
            response = requests.get(citations_url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()
            results = data.get('results', [])

            # Process citations
            citations = []
            for work in results:
                # Safely extract venue
                venue = None
                primary_location = work.get('primary_location')
                if primary_location and isinstance(primary_location, dict):
                    source = primary_location.get('source')
                    if source and isinstance(source, dict):
                        venue = source.get('display_name')

                citation = {
                    "openalex_id": work.get('id', '').replace('https://openalex.org/', ''),
                    "title": work.get('title') or work.get('display_name'),
                    "authors": [a.get('author', {}).get('display_name', '') for a in work.get('authorships', []) if a.get('author')],
                    "year": work.get('publication_year'),
                    "venue": venue,
                    "doi": work.get('doi'),
                    "cited_by_count": work.get('cited_by_count', 0)
                }
                citations.append(citation)

            # Save to cache
            self._save_cache(cache_key, citations)

            logger.info(f"Found {len(citations)} citations for {openalex_id}")
            return citations

        except requests.RequestException as e:
            logger.error(f"OpenAlex API error fetching citations: {e}")
            return []
        except Exception as e:
            logger.error(f"Error fetching citations: {e}")
            return []

    def analyze_citations(self, paper_title: str, authors: str = None, year: int = None) -> Dict:
        """
        Phase 1 Task 3: Main method - get and analyze citations.

        Args:
            paper_title: Paper title
            authors: Author names (optional)
            year: Publication year (optional)

        Returns:
            Dict with citation analysis results:
            {
                "total_citations": int,
                "citations": List[Dict],
                "by_year": Dict[int, int],
                "sources_used": List[str],
                "last_updated": str
            }
        """
        logger.info(f"Analyzing citations for: {paper_title}")

        # 1. Get paper ID
        paper_info = self.get_paper_id_openalex(paper_title, authors, year)
        if not paper_info:
            logger.warning(f"Could not find paper: {paper_title}")
            return {
                "total_citations": 0,
                "citations": [],
                "by_year": {},
                "sources_used": [],
                "last_updated": datetime.now().isoformat(),
                "paper_found": False
            }

        # 2. Fetch citations (Phase 1: only OpenAlex)
        citations = self.fetch_citations_openalex(paper_info['openalex_id'])

        # 3. Process results
        result = {
            "total_citations": len(citations),
            "citations": citations[:10],  # Top 10 for preview
            "by_year": self._group_by_year(citations),
            "sources_used": ["OpenAlex"],
            "last_updated": datetime.now().isoformat(),
            "paper_found": True,
            "paper_info": paper_info
        }

        logger.info(f"Analysis complete: {result['total_citations']} citations found")
        return result

    def _group_by_year(self, citations: List[Dict]) -> Dict[int, int]:
        """Group citations by publication year."""
        by_year = {}
        for cit in citations:
            year = cit.get('year')
            if year:
                by_year[year] = by_year.get(year, 0) + 1
        return dict(sorted(by_year.items()))

    # ==================== Phase 2: Multi-Source Integration ====================

    def setup_semantic_scholar(self, api_key: str = None):
        """
        Initialize Semantic Scholar client.

        Args:
            api_key: Optional API key for higher rate limits
        """
        try:
            from semanticscholar import SemanticScholar
            self.s2_client = SemanticScholar(api_key=api_key)
            if "semantic_scholar" not in self.sources:
                self.sources.append("semantic_scholar")
            logger.info("Semantic Scholar client initialized successfully")
        except ImportError:
            logger.warning("semanticscholar package not installed. Run: pip install semanticscholar")
        except Exception as e:
            logger.error(f"Failed to initialize Semantic Scholar: {e}")

    def get_paper_id_semanticscholar(self, title: str, authors: str = None, year: int = None) -> Optional[Dict]:
        """
        Get paper information from Semantic Scholar.

        Args:
            title: Paper title
            authors: Author names (optional)
            year: Publication year (optional)

        Returns:
            Dict with paper metadata including s2_id, title, year, etc.
        """
        if not self.s2_client:
            logger.warning("Semantic Scholar not initialized. Call setup_semantic_scholar() first.")
            return None

        # Check cache
        cache_key = self._get_cache_key(f"s2_{title}_{authors}_{year}")
        cached = self._get_cached(cache_key)
        if cached:
            return cached

        try:
            # Search for paper
            logger.info(f"Querying Semantic Scholar for: {title}")
            results = self.s2_client.search_paper(title, limit=5)

            if not results or not hasattr(results, 'items') or not results.items:
                logger.warning(f"No results found in Semantic Scholar for: {title}")
                return None

            # Convert to list of dicts for matching
            results_list = []
            for paper in results.items:
                results_list.append({
                    'title': paper.title,
                    'year': paper.year,
                    'authors': [a.name for a in paper.authors] if hasattr(paper, 'authors') else [],
                    'citation_count': paper.citationCount if hasattr(paper, 'citationCount') else 0
                })

            # Find best match
            best_match = self._find_best_match(results_list, title, authors, year)

            if not best_match:
                return None

            # Get the corresponding paper object
            for paper in results.items:
                if paper.title == best_match['title']:
                    paper_info = {
                        's2_id': paper.paperId,
                        'title': paper.title,
                        'year': paper.year,
                        'doi': paper.externalIds.get('DOI') if hasattr(paper, 'externalIds') and paper.externalIds else None,
                        'citation_count': paper.citationCount if hasattr(paper, 'citationCount') else 0,
                        'url': paper.url if hasattr(paper, 'url') else None,
                        'venue': paper.venue if hasattr(paper, 'venue') else None,
                        'authors': [a.name for a in paper.authors] if hasattr(paper, 'authors') else []
                    }

                    # Save to cache
                    self._save_cache(cache_key, paper_info)

                    logger.info(f"Found paper in Semantic Scholar: {paper_info['title']} (ID: {paper_info['s2_id']}, Citations: {paper_info['citation_count']})")
                    return paper_info

        except Exception as e:
            logger.error(f"Semantic Scholar search failed: {e}")

        return None

    def fetch_citations_semanticscholar(self, s2_id: str, limit: int = 200) -> List[Dict]:
        """
        Fetch citations from Semantic Scholar.

        Args:
            s2_id: Semantic Scholar paper ID
            limit: Maximum number of citations to return

        Returns:
            List of citing papers with metadata
        """
        if not self.s2_client:
            logger.warning("Semantic Scholar not initialized")
            return []

        # Check cache
        cache_key = self._get_cache_key(f"s2_citations_{s2_id}")
        cached = self._get_cached(cache_key)
        if cached:
            return cached

        try:
            logger.info(f"Fetching citations from Semantic Scholar for: {s2_id}")
            paper = self.s2_client.get_paper(s2_id)

            if not paper or not hasattr(paper, 'citations'):
                logger.warning(f"No citations found for Semantic Scholar ID: {s2_id}")
                return []

            citations = []
            for citation in paper.citations[:limit]:
                cit_data = {
                    's2_id': citation.paperId if hasattr(citation, 'paperId') else None,
                    'title': citation.title if hasattr(citation, 'title') else None,
                    'year': citation.year if hasattr(citation, 'year') else None,
                    'authors': [a.name for a in citation.authors] if hasattr(citation, 'authors') else [],
                    'venue': citation.venue if hasattr(citation, 'venue') else None,
                    'citation_count': citation.citationCount if hasattr(citation, 'citationCount') else 0,
                    'doi': citation.externalIds.get('DOI') if hasattr(citation, 'externalIds') and citation.externalIds else None,
                    'url': citation.url if hasattr(citation, 'url') else None,
                    'source': 'semantic_scholar'
                }
                citations.append(cit_data)

            # Save to cache
            self._save_cache(cache_key, citations)

            logger.info(f"Found {len(citations)} citations from Semantic Scholar")
            return citations

        except Exception as e:
            logger.error(f"Semantic Scholar citations fetch failed: {e}")
            return []

    def fetch_citations_opencitations(self, doi: str) -> List[Dict]:
        """
        Fetch citations from OpenCitations.

        Args:
            doi: Paper DOI

        Returns:
            List of citing papers with metadata
        """
        if not doi:
            logger.warning("DOI required for OpenCitations query")
            return []

        # Check cache
        cache_key = self._get_cache_key(f"opencitations_{doi}")
        cached = self._get_cached(cache_key)
        if cached:
            return cached

        try:
            # OpenCitations API endpoint
            url = f"{self.opencitations_base}/citations/{doi}"
            logger.info(f"Fetching citations from OpenCitations for DOI: {doi}")

            response = requests.get(url, timeout=30)
            response.raise_for_status()

            data = response.json()

            citations = []
            for item in data:
                citation = {
                    'citing_doi': item.get('citing'),
                    'cited_doi': item.get('cited'),
                    'creation_date': item.get('creation'),
                    'source': 'opencitations'
                }
                citations.append(citation)

            # Save to cache
            self._save_cache(cache_key, citations)

            logger.info(f"Found {len(citations)} citations from OpenCitations")
            return citations

        except requests.RequestException as e:
            logger.error(f"OpenCitations API error: {e}")
            return []
        except Exception as e:
            logger.error(f"OpenCitations fetch failed: {e}")
            return []

    def enrich_citation_with_metadata(self, doi: str) -> Optional[Dict]:
        """
        Enrich citation with metadata using DOI (via OpenAlex or Crossref).

        Args:
            doi: Paper DOI

        Returns:
            Dict with paper metadata
        """
        if not doi:
            return None

        # Check cache
        cache_key = self._get_cache_key(f"enrich_{doi}")
        cached = self._get_cached(cache_key)
        if cached:
            return cached

        # Try OpenAlex first (already integrated)
        try:
            import pyalex
            works = pyalex.Works().filter(doi=doi).get()

            if works and len(works) > 0:
                work = works[0]
                result = {
                    'title': work.get('title') or work.get('display_name'),
                    'year': work.get('publication_year'),
                    'authors': [a.get('author', {}).get('display_name', '') for a in work.get('authorships', []) if a.get('author')],
                    'venue': work.get('primary_location', {}).get('source', {}).get('display_name') if work.get('primary_location') else None,
                    'doi': doi,
                    'openalex_id': work.get('id', '').replace('https://openalex.org/', ''),
                    'source': 'openalex'
                }
                self._save_cache(cache_key, result)
                return result

        except Exception as e:
            logger.debug(f"OpenAlex enrichment failed for DOI {doi}: {e}")

        # Fallback to Crossref
        try:
            url = f"https://api.crossref.org/works/{doi}"
            response = requests.get(url, timeout=30)

            if response.ok:
                data = response.json()['message']
                result = {
                    'title': data.get('title', [''])[0] if data.get('title') else None,
                    'year': data.get('published-print', {}).get('date-parts', [[None]])[0][0] if data.get('published-print') else None,
                    'authors': [f"{a.get('given', '')} {a.get('family', '')}".strip() for a in data.get('author', [])],
                    'venue': data.get('container-title', [''])[0] if data.get('container-title') else None,
                    'doi': doi,
                    'source': 'crossref'
                }
                self._save_cache(cache_key, result)
                return result

        except Exception as e:
            logger.debug(f"Crossref enrichment failed for DOI {doi}: {e}")

        return None

    def cross_validate_citations(self, citations_by_source: Dict[str, List[Dict]], min_sources: int = 2) -> List[Dict]:
        """
        Cross-validate citations from multiple sources.

        Args:
            citations_by_source: Format {'openalex': [...], 'semantic_scholar': [...], 'opencitations': [...]}
            min_sources: Minimum number of sources required for verification

        Returns:
            List of verified citations with validation metadata
        """
        # Build index using (title, year) as unique identifier
        citation_index = {}

        for source, citations in citations_by_source.items():
            if not citations:
                continue

            for cit in citations:
                # Extract unique identifier
                title = cit.get('title', '').lower().strip() if cit.get('title') else None
                year = cit.get('year')

                if not title or not year:
                    # Try to enrich with metadata
                    if cit.get('citing_doi'):  # OpenCitations case
                        enriched = self.enrich_citation_with_metadata(cit['citing_doi'])
                        if enriched:
                            title = enriched.get('title', '').lower().strip()
                            year = enriched.get('year')
                            cit.update(enriched)

                if not title or not year:
                    continue

                key = f"{title}|{year}"

                if key not in citation_index:
                    citation_index[key] = {
                        'title': cit.get('title'),
                        'year': year,
                        'authors': cit.get('authors', []),
                        'venue': cit.get('venue'),
                        'doi': cit.get('doi'),
                        'url': cit.get('url'),
                        'sources': [],
                        'source_details': {}
                    }

                # Add source information
                if source not in citation_index[key]['sources']:
                    citation_index[key]['sources'].append(source)
                citation_index[key]['source_details'][source] = cit

                # Merge metadata (prefer more complete data)
                if not citation_index[key].get('doi') and cit.get('doi'):
                    citation_index[key]['doi'] = cit['doi']
                if not citation_index[key].get('url') and cit.get('url'):
                    citation_index[key]['url'] = cit['url']
                if not citation_index[key].get('authors') and cit.get('authors'):
                    citation_index[key]['authors'] = cit['authors']

        # Filter citations that appear in at least min_sources
        verified = []
        for key, data in citation_index.items():
            if len(data['sources']) >= min_sources:
                # Calculate verification score
                data['verification_score'] = len(data['sources']) / len(citations_by_source)
                data['verified_by'] = data['sources']
                verified.append(data)

        # Sort by year (newest first)
        verified.sort(key=lambda x: x.get('year', 0), reverse=True)

        logger.info(f"Cross-validation complete: {len(verified)} citations verified from {len(citation_index)} total unique citations")

        return verified

    def analyze_citations_multisource(self, paper_title: str, authors: str = None,
                                      year: int = None, min_sources: int = 2) -> Dict:
        """
        Enhanced multi-source citation analysis with cross-validation.

        Args:
            paper_title: Paper title
            authors: Author names (optional)
            year: Publication year (optional)
            min_sources: Minimum sources required for verification

        Returns:
            Dict with cross-validated citation analysis
        """
        logger.info(f"Starting multi-source analysis for: {paper_title}")

        # 1. Get paper IDs from different sources
        paper_ids = {}
        dois = []

        # OpenAlex
        oa_info = self.get_paper_id_openalex(paper_title, authors, year)
        if oa_info:
            paper_ids['openalex'] = oa_info.get('openalex_id')
            if oa_info.get('doi'):
                dois.append(oa_info['doi'])

        # Semantic Scholar
        if self.s2_client:
            s2_info = self.get_paper_id_semanticscholar(paper_title, authors, year)
            if s2_info:
                paper_ids['semantic_scholar'] = s2_info.get('s2_id')
                if s2_info.get('doi'):
                    dois.append(s2_info['doi'])

        # Use first available DOI for OpenCitations
        doi = dois[0] if dois else None

        # 2. Fetch citations from each source
        citations_by_source = {}

        if 'openalex' in paper_ids:
            citations_by_source['openalex'] = self.fetch_citations_openalex(paper_ids['openalex'])

        if 'semantic_scholar' in paper_ids:
            citations_by_source['semantic_scholar'] = self.fetch_citations_semanticscholar(
                paper_ids['semantic_scholar']
            )

        if doi:
            oc_citations = self.fetch_citations_opencitations(doi)
            # Enrich OpenCitations with metadata
            enriched = []
            for cit in oc_citations[:50]:  # Limit to avoid too many API calls
                if cit.get('citing_doi'):
                    meta = self.enrich_citation_with_metadata(cit['citing_doi'])
                    if meta:
                        meta['source'] = 'opencitations'
                        enriched.append(meta)
            citations_by_source['opencitations'] = enriched

        # 3. Cross-validate
        verified_citations = self.cross_validate_citations(citations_by_source, min_sources)

        # 4. Generate statistics
        result = {
            "total_citations": len(verified_citations),
            "total_raw": {
                source: len(cits) for source, cits in citations_by_source.items()
            },
            "citations": verified_citations[:20],  # Top 20 for preview
            "by_year": self._group_by_year(verified_citations),
            "by_source_coverage": {
                source: sum(1 for c in verified_citations if source in c['sources'])
                for source in citations_by_source.keys()
            },
            "sources_used": list(citations_by_source.keys()),
            "sources_available": self.sources,
            "min_sources_required": min_sources,
            "last_updated": datetime.now().isoformat(),
            "paper_ids": paper_ids,
            "doi": doi
        }

        logger.info(f"Multi-source analysis complete: {result['total_citations']} verified citations")
        return result
