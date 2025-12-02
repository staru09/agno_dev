from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class WebSearchResult(BaseModel):
    """Single web search hit."""

    title: str = Field(..., description="Title of the article or resource.")
    summary: str = Field(..., description="Short description of the findings.")
    url: str = Field(..., description="Canonical link to the source.")
    source: Optional[str] = Field(None, description="Site or publisher name.")


class WebSearchResults(BaseModel):
    """Structured output for the web search agent."""

    results: List[WebSearchResult] = Field(..., description="Ranked list of relevant links.")


class ArxivPaper(BaseModel):
    """Metadata for an ArXiv paper."""

    title: str = Field(..., description="Paper title.")
    arxiv_id: str = Field(..., description="Unique ArXiv identifier.")
    summary: str = Field(..., description="Concise abstract written for a general audience.")
    pdf_url: str = Field(..., description="Direct link to the PDF.")
    authors: List[str] = Field(..., description="List of authors.")
    primary_category: Optional[str] = Field(None, description="ArXiv primary category.")
    published: Optional[str] = Field(None, description="Publication date.")


class ArxivPapers(BaseModel):
    """Structured output for the ArXiv agent."""

    papers: List[ArxivPaper] = Field(..., description="Top relevant academic papers.")


class ResearchBrief(BaseModel):
    """Final structured brief returned by the writer."""

    overview: str = Field(..., description="Executive summary of the findings.")
    key_findings: List[str] = Field(..., description="Bulleted findings backed by citations.")
    next_steps: List[str] = Field(..., description="Actionable follow-ups for the reader.")
    cited_sources: List[str] = Field(..., description="Canonical links used in the brief.")
