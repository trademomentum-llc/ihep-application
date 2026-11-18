"""
Audit Logging Utility
Logs all PHI access and security events to Google Cloud Logging
"""

import os
import re
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from google.cloud import logging as cloud_logging
from flask import request


_CONTROL_CHARS = re.compile(r"[\x00-\x1f\x7f]")


def _sanitize_log_value(value: Any, max_len: int = 64) -> str:
    """Strip CR/LF and other control characters so a value cannot forge log lines."""
    text = str(value).replace("\r", "").replace("\n", "")
    return _CONTROL_CHARS.sub("", text)[:max_len]


class AuditLogger:
    """
    Audit Logger for HIPAA Compliance
    
    Properties:
    - P(log) = 1.0 (every access logged)
    - Tamper-resistant (Cloud Logging immutable)
    - Retention: 7 years minimum
    """
    
    def __init__(self):
        self.client = cloud_logging.Client()
        self.logger = self.client.logger('ihep-audit-log')
        self.local_logger = logging.getLogger(__name__)
    
    def log(
        self,
        user_id: str,
        action: str,
        resource: str,
        outcome: str,
        details: Optional[Dict[str, Any]] = None
    ):
        """
        Log audit event
        
        Args:
            user_id: ID of user performing action
            action: Action type (LOGIN, VIEW_PHI, UPDATE_PHI, etc.)
            resource: Resource accessed
            outcome: SUCCESS or FAILURE
            details: Additional context
        """
        ip_address = request.remote_addr if request else 'unknown'
        user_agent = request.headers.get('User-Agent', 'unknown') if request else 'unknown'
        
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'user_id': user_id,
            'action': action,
            'resource': resource,
            'outcome': outcome,
            'ip_address': ip_address,
            'user_agent': user_agent,
            'details': details or {}
        }
        
        # Log to Cloud Logging
        self.logger.log_struct(log_entry, severity='INFO')
        
        # Also log locally for development. The full record (including the
        # user and resource identifiers) lives only in the Cloud Logging audit
        # trail above; the local log line carries no identifiers, only the
        # sanitized action and outcome.
        self.local_logger.info(
            "AUDIT: action=%s outcome=%s (identifiers recorded in ihep-audit-log only)",
            _sanitize_log_value(action),
            _sanitize_log_value(outcome),
        )
