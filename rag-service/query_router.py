"""
QueryRouter - Classify queries and determine search strategy

This module analyzes queries and routes them to the appropriate search strategy:
- LIST_ALL: "What are all the artworks?" → Metadata filter only
- FIND_SIMILAR: "Files like this one" → Pure semantic search
- FILTER: "Files in Characters folder" → Metadata filter
- SEARCH: "Files about dragons" → Hybrid search
- SPECIFIC: "Who is Captain Novák?" → Focused semantic + keyword
"""

import re
from typing import Dict, Any, Optional, List
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QueryType(Enum):
    """Types of queries the system can handle"""
    LIST_ALL = "list_all"           # List all X (metadata filter)
    FILTER = "filter"                # Filter by metadata
    SEARCH = "search"                # General search (hybrid)
    SPECIFIC = "specific"            # Specific entity lookup
    FIND_SIMILAR = "find_similar"    # Find similar to X


class QueryRouter:
    """Classify queries and extract search parameters"""

    # Patterns for different query types
    LIST_ALL_PATTERNS = [
        r'(?:list|show|what are|get|find)\s+(?:all|every)(?:\s+the)?\s+(\w+)',
        r'all\s+(?:of\s+)?(?:the\s+)?(\w+)',
        r'(?:how many|count)\s+(\w+)',
    ]

    FILTER_PATTERNS = [
        r'(?:in|from|under)\s+(?:the\s+)?(\w+)\s+(?:folder|directory|path)',
        r'(?:tagged|with tag)\s+[#]?(\w+)',
        r'(?:created|modified|updated)\s+(?:on|after|before|in)\s+(.+)',
    ]

    SPECIFIC_PATTERNS = [
        r'(?:who|what)\s+is\s+(.+)',
        r'(?:tell me about|explain|describe)\s+(.+)',
        r'(?:show me|find)\s+(?:the\s+)?file\s+(?:about|for|on)\s+(.+)',
    ]

    SIMILAR_PATTERNS = [
        r'(?:similar to|like|related to)\s+(.+)',
        r'(?:files|documents|notes)\s+(?:similar to|like)\s+(.+)',
        r'more\s+(?:files\s+)?like\s+(.+)',
    ]

    def __init__(self):
        """Initialize query router"""
        logger.info("QueryRouter initialized")

    def classify_query(self, query: str) -> QueryType:
        """
        Classify the type of query

        Args:
            query: User's query string

        Returns:
            QueryType enum
        """
        query_lower = query.lower().strip()

        # Check LIST_ALL patterns
        for pattern in self.LIST_ALL_PATTERNS:
            if re.search(pattern, query_lower):
                logger.debug(f"Classified as LIST_ALL: {query}")
                return QueryType.LIST_ALL

        # Check FILTER patterns
        for pattern in self.FILTER_PATTERNS:
            if re.search(pattern, query_lower):
                logger.debug(f"Classified as FILTER: {query}")
                return QueryType.FILTER

        # Check SPECIFIC patterns
        for pattern in self.SPECIFIC_PATTERNS:
            if re.search(pattern, query_lower):
                logger.debug(f"Classified as SPECIFIC: {query}")
                return QueryType.SPECIFIC

        # Check SIMILAR patterns
        for pattern in self.SIMILAR_PATTERNS:
            if re.search(pattern, query_lower):
                logger.debug(f"Classified as FIND_SIMILAR: {query}")
                return QueryType.FIND_SIMILAR

        # Default to SEARCH (hybrid)
        logger.debug(f"Classified as SEARCH: {query}")
        return QueryType.SEARCH

    def extract_entity(self, query: str, query_type: QueryType) -> Optional[str]:
        """
        Extract the main entity/subject from the query

        Args:
            query: User's query string
            query_type: Classified query type

        Returns:
            Extracted entity or None
        """
        query_lower = query.lower().strip()

        if query_type == QueryType.LIST_ALL:
            # Extract the noun being listed
            for pattern in self.LIST_ALL_PATTERNS:
                match = re.search(pattern, query_lower)
                if match:
                    entity = match.group(1)
                    # Pluralize if needed for better matching
                    return entity

        elif query_type == QueryType.SPECIFIC:
            # Extract the subject
            for pattern in self.SPECIFIC_PATTERNS:
                match = re.search(pattern, query_lower)
                if match:
                    return match.group(1).strip()

        elif query_type == QueryType.FIND_SIMILAR:
            # Extract reference document/topic
            for pattern in self.SIMILAR_PATTERNS:
                match = re.search(pattern, query_lower)
                if match:
                    return match.group(1).strip()

        return None

    def extract_folder_filter(self, query: str) -> Optional[str]:
        """
        Extract folder filter from query

        Args:
            query: User's query string

        Returns:
            Folder name or None
        """
        query_lower = query.lower().strip()

        # Pattern: "in/from/under <folder> folder"
        pattern = r'(?:in|from|under)\s+(?:the\s+)?(\w+)\s+(?:folder|directory)'
        match = re.search(pattern, query_lower)

        if match:
            folder = match.group(1).capitalize()  # Capitalize folder name
            return folder

        return None

    def extract_tag_filter(self, query: str) -> Optional[List[str]]:
        """
        Extract tag filters from query

        Args:
            query: User's query string

        Returns:
            List of tags or None
        """
        query_lower = query.lower().strip()

        # Pattern: "tagged <tag>" or "with tag <tag>"
        tags = []

        # Find hashtags
        hashtag_matches = re.findall(r'#(\w+)', query_lower)
        tags.extend(hashtag_matches)

        # Find "tagged X" or "with tag X"
        tag_pattern = r'(?:tagged|with tag)\s+[#]?(\w+)'
        tag_matches = re.findall(tag_pattern, query_lower)
        tags.extend(tag_matches)

        return tags if tags else None

    def route_query(self, query: str) -> Dict[str, Any]:
        """
        Analyze query and return routing information

        Args:
            query: User's query string

        Returns:
            Dictionary with routing information:
            - query_type: QueryType enum
            - entity: Extracted entity/subject
            - folder: Folder filter (if any)
            - tags: Tag filters (if any)
            - search_strategy: Recommended search strategy
            - parameters: Strategy-specific parameters
        """
        # Classify query type
        query_type = self.classify_query(query)

        # Extract components
        entity = self.extract_entity(query, query_type)
        folder = self.extract_folder_filter(query)
        tags = self.extract_tag_filter(query)

        # Determine search strategy and parameters
        if query_type == QueryType.LIST_ALL:
            search_strategy = "metadata_only"
            parameters = {
                "entity": entity,
                "folder": folder,
                "tags": tags,
                "use_semantic": False,
                "use_keyword": False,
                "limit": 100  # Return all matches
            }

        elif query_type == QueryType.FILTER:
            search_strategy = "metadata_filter"
            parameters = {
                "folder": folder,
                "tags": tags,
                "use_semantic": False,
                "use_keyword": False,
                "limit": 50
            }

        elif query_type == QueryType.SPECIFIC:
            search_strategy = "semantic_keyword"
            parameters = {
                "entity": entity,
                "use_semantic": True,
                "use_keyword": True,
                "semantic_weight": 0.6,
                "keyword_weight": 0.4,
                "limit": 10
            }

        elif query_type == QueryType.FIND_SIMILAR:
            search_strategy = "semantic_only"
            parameters = {
                "reference": entity,
                "use_semantic": True,
                "use_keyword": False,
                "limit": 15
            }

        else:  # SEARCH (hybrid)
            search_strategy = "hybrid"
            parameters = {
                "use_semantic": True,
                "use_keyword": True,
                "use_metadata": True,
                "semantic_weight": 0.5,
                "keyword_weight": 0.3,
                "metadata_weight": 0.2,
                "folder": folder,
                "tags": tags,
                "limit": 20
            }

        result = {
            "query_type": query_type,
            "entity": entity,
            "folder": folder,
            "tags": tags,
            "search_strategy": search_strategy,
            "parameters": parameters
        }

        logger.info(f"Query routed: type={query_type.value}, strategy={search_strategy}")

        return result

    def explain_routing(self, routing: Dict[str, Any]) -> str:
        """
        Generate human-readable explanation of routing decision

        Args:
            routing: Output from route_query()

        Returns:
            Explanation string
        """
        query_type = routing['query_type']
        strategy = routing['search_strategy']
        entity = routing.get('entity')
        folder = routing.get('folder')
        tags = routing.get('tags')

        explanation = f"Query Type: {query_type.value}\n"
        explanation += f"Search Strategy: {strategy}\n"

        if entity:
            explanation += f"Entity: {entity}\n"
        if folder:
            explanation += f"Folder Filter: {folder}\n"
        if tags:
            explanation += f"Tag Filters: {', '.join(tags)}\n"

        explanation += f"\nParameters: {routing['parameters']}"

        return explanation
