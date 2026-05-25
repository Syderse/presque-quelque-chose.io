from __future__ import annotations

import hashlib
import re
from datetime import date, datetime
from enum import Enum
from typing import Any
from urllib.parse import parse_qsl, unquote, urlencode, urlsplit, urlunsplit

from pydantic import BaseModel, ConfigDict, Field, field_validator


class SourceType(str, Enum):
    journal_article = "journal_article"
    cfp = "cfp"
    thesis = "thesis"
    book = "book"
    chapter = "chapter"
    blog = "blog"
    archive = "archive"
    unknown = "unknown"


class WatchStatus(str, Enum):
    new = "new"
    candidate = "candidate"
    to_read = "to_read"
    ignored = "ignored"
    exported = "exported"


DOI_PREFIX_RE = re.compile(r"^(?:doi:\s*|https?://(?:dx\.)?doi\.org/)", re.IGNORECASE)
DOI_VALUE_RE = re.compile(r"\b10\.\d{4,9}/[^\s\"<>#?]+", re.IGNORECASE)
TRACKING_QUERY_PREFIXES = ("utm_",)
TRACKING_QUERY_KEYS = {"fbclid", "gclid", "mc_cid", "mc_eid"}


def _stable_hash(namespace: str, value: str) -> str:
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:20]
    return f"{namespace}:{digest}"


def _compact_text(value: Any) -> str | None:
    if value is None:
        return None

    compacted = " ".join(str(value).strip().split())
    return compacted or None


def normalize_doi(doi: str | None) -> str | None:
    compacted = _compact_text(doi)
    if compacted is None:
        return None

    normalized = DOI_PREFIX_RE.sub("", compacted).strip()
    parsed = urlsplit(compacted)
    if parsed.scheme.lower() in {"http", "https"}:
        path = unquote(parsed.path.lstrip("/"))
        if parsed.netloc.lower() in {"doi.org", "dx.doi.org"}:
            normalized = path
        else:
            match = DOI_VALUE_RE.search(path)
            if match:
                normalized = match.group(0)

    if not normalized.lower().startswith("10."):
        match = DOI_VALUE_RE.search(normalized)
        if match:
            normalized = match.group(0)
        else:
            return None

    normalized = normalized.strip().lower()
    normalized = normalized.rstrip(".,;)")
    return normalized or None


def normalize_url(url: str | None) -> str | None:
    compacted = _compact_text(url)
    if compacted is None:
        return None

    parsed = urlsplit(compacted)
    if not parsed.scheme and not parsed.netloc:
        parsed = urlsplit(f"https://{compacted}")

    scheme = (parsed.scheme or "https").lower()
    netloc = parsed.netloc.lower()
    path = parsed.path.rstrip("/") or "/"

    query_pairs = [
        (key, value)
        for key, value in parse_qsl(parsed.query, keep_blank_values=True)
        if key not in TRACKING_QUERY_KEYS and not key.startswith(TRACKING_QUERY_PREFIXES)
    ]
    query = urlencode(sorted(query_pairs), doseq=True)

    return urlunsplit((scheme, netloc, path, query, ""))


def _date_key(value: date | datetime | str | None) -> str:
    if value is None:
        return "unknown-date"
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()

    return _compact_text(value) or "unknown-date"


def generate_stable_id(
    *,
    doi: str | None = None,
    url: str | None = None,
    title: str | None = None,
    published_at: date | datetime | str | None = None,
    source_name: str | None = None,
) -> str:
    normalized_doi = normalize_doi(doi) or normalize_doi(url)
    if normalized_doi:
        return _stable_hash("doi", normalized_doi)

    normalized_url = normalize_url(url)
    if normalized_url:
        return _stable_hash("url", normalized_url)

    fallback_parts = [
        _compact_text(title) or "untitled",
        _date_key(published_at),
        _compact_text(source_name) or "unknown-source",
    ]
    return _stable_hash("fallback", "|".join(fallback_parts).lower())


class RadioWatchItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    source_name: str = Field(min_length=1)
    source_type: SourceType
    language: str = Field(min_length=2)
    status: WatchStatus
    discovered_at: datetime

    title_original: str | None = None
    container_title: str | None = None
    authors: list[str] = Field(default_factory=list)
    published_at: datetime | None = None
    url: str | None = None
    doi: str | None = None
    abstract: str | None = None
    tags: list[str] = Field(default_factory=list)
    keywords_matched: list[str] = Field(default_factory=list)
    negative_keywords_matched: list[str] = Field(default_factory=list)
    relevance_score: float | None = None
    score_explanation: str | None = None
    source_feed: str | None = None
    source_api: str | None = None
    raw: dict[str, Any] = Field(default_factory=dict)

    @field_validator(
        "id",
        "title",
        "source_name",
        "language",
        "title_original",
        "container_title",
        "abstract",
        "score_explanation",
        "source_feed",
        "source_api",
        mode="before",
    )
    @classmethod
    def strip_text(cls, value: Any) -> Any:
        if value is None:
            return None
        if isinstance(value, str):
            return value.strip()
        return value

    @field_validator("doi", mode="before")
    @classmethod
    def normalize_doi_field(cls, value: str | None) -> str | None:
        return normalize_doi(value)

    @field_validator("url", mode="before")
    @classmethod
    def normalize_url_field(cls, value: str | None) -> str | None:
        return normalize_url(value)
