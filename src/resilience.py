"""
Resilience Module for PaperReader

Provides retry logic and error handling for API calls
"""

import time
import logging
from typing import Optional, Callable, Any
from functools import wraps
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class RetryConfig:
    """Configuration for retry behavior"""
    max_retries: int = 3
    initial_delay: float = 1.0
    max_delay: float = 60.0
    exponential_base: float = 2.0
    retryable_errors: tuple = (Exception,)


class RetryableError(Exception):
    """Error that can be retried"""
    pass


class MaxRetriesExceededError(Exception):
    """Maximum retries exceeded"""
    pass


def exponential_backoff(func: Callable) -> Callable:
    """
    Decorator for exponential backoff retry

    Retries the function with exponential backoff on failure
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Extract retry config from kwargs, don't pass it to the wrapped function
        config = kwargs.pop('retry_config', RetryConfig())

        last_exception = None

        for attempt in range(config.max_retries):
            try:
                return func(*args, **kwargs)

            except config.retryable_errors as e:
                last_exception = e

                if attempt == config.max_retries - 1:
                    # Last attempt failed
                    logger.error(f"All {config.max_retries} attempts failed for {func.__name__}")
                    raise MaxRetriesExceededError(
                        f"Max retries ({config.max_retries}) exceeded for {func.__name__}"
                    ) from e

                # Calculate delay with exponential backoff
                delay = min(
                    config.initial_delay * (config.exponential_base ** attempt),
                    config.max_delay
                )

                logger.warning(
                    f"Attempt {attempt + 1}/{config.max_retries} failed for {func.__name__}: {e}. "
                    f"Retrying in {delay:.1f}s..."
                )

                time.sleep(delay)

        # Should not reach here, but just in case
        raise MaxRetriesExceededError(
            f"Unexpected error in retry logic for {func.__name__}"
        ) from last_exception

    return wrapper


class ResilientAIAnalyzer:
    """
    Wrapper for AI analyzer with resilience features

    Provides:
    - Automatic retry on failure
    - Fallback to cheaper models
    - Cost tracking
    """

    def __init__(self, analyzer, config: Optional[RetryConfig] = None):
        """
        Initialize resilient analyzer

        Args:
            analyzer: AIAnalyzer instance
            config: Retry configuration
        """
        self.analyzer = analyzer
        self.config = config or RetryConfig()
        self.call_count = 0
        self.total_cost = 0.0
        self.failure_count = 0

    def analyze_with_retry(self, paper_text: str, **kwargs) -> Any:
        """
        Analyze paper with retry logic

        Args:
            paper_text: Text to analyze
            **kwargs: Additional arguments for analyzer

        Returns:
            Analysis result
        """
        @exponential_backoff
        def _analyze():
            self.call_count += 1
            try:
                result = self.analyzer.analyze_paper(paper_text, **kwargs)
                return result
            except Exception as e:
                self.failure_count += 1
                logger.error(f"AI analysis failed: {e}")
                raise RetryableError(f"Analysis failed: {e}") from e

        return _analyze(retry_config=self.config)

    def quick_analysis_with_retry(self, paper_text: str, **kwargs) -> Any:
        """
        Quick analysis with retry (uses cheaper model)

        Args:
            paper_text: Text to analyze
            **kwargs: Additional arguments

        Returns:
            Quick analysis result
        """
        @exponential_backoff
        def _quick_analyze():
            self.call_count += 1
            try:
                result = self.analyzer.quick_analysis(paper_text, **kwargs)
                return result
            except Exception as e:
                self.failure_count += 1
                logger.error(f"Quick analysis failed: {e}")
                raise RetryableError(f"Quick analysis failed: {e}") from e

        return _quick_analyze(retry_config=self.config)

    def get_stats(self) -> dict:
        """Get resilience statistics"""
        return {
            'total_calls': self.call_count,
            'failures': self.failure_count,
            'success_rate': (self.call_count - self.failure_count) / self.call_count if self.call_count > 0 else 0,
            'total_cost': self.total_cost,
        }


class FallbackAnalyzer:
    """
    Analyzer with fallback to cheaper models

    Tries primary model first, falls back to cheaper model on failure
    """

    def __init__(self, primary_analyzer, fallback_analyzer):
        """
        Initialize fallback analyzer

        Args:
            primary_analyzer: Primary (expensive) analyzer
            fallback_analyzer: Fallback (cheaper) analyzer
        """
        self.primary = primary_analyzer
        self.fallback = fallback_analyzer
        self.primary_calls = 0
        self.fallback_calls = 0

    def analyze(self, paper_text: str, **kwargs) -> Any:
        """
        Analyze with fallback

        Args:
            paper_text: Text to analyze
            **kwargs: Additional arguments

        Returns:
            Analysis result
        """
        # Try primary first
        try:
            self.primary_calls += 1
            result = self.primary.analyze_paper(paper_text, **kwargs)
            return result
        except Exception as e:
            logger.warning(f"Primary analyzer failed: {e}. Falling back to cheaper model.")

            # Fall back to cheaper model
            try:
                self.fallback_calls += 1
                result = self.fallback.analyze_paper(paper_text, **kwargs)
                return result
            except Exception as fallback_error:
                logger.error(f"Fallback analyzer also failed: {fallback_error}")
                raise

    def get_stats(self) -> dict:
        """Get statistics"""
        return {
            'primary_calls': self.primary_calls,
            'fallback_calls': self.fallback_calls,
            'fallback_rate': self.fallback_calls / (self.primary_calls + self.fallback_calls)
                            if (self.primary_calls + self.fallback_calls) > 0 else 0,
        }
