from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class LogEntry:
    type: str
    time: datetime
    elb: str
    client_address: str
    client_port: str
    target_address: str
    target_port: str
    request_processing_time: float
    target_processing_time: float
    response_processing_time: float
    elb_status_code: int
    target_status_code: Optional[int]
    received_bytes: int
    sent_bytes: int
    request: str
    user_agent: str
    ssl_cipher: str
    ssl_protocol: str
    target_group_arn: str
    trace_id: str
    domain_name: str
    chosen_cert_arn: str
    matched_rule_priority: int
    request_creation_time: str
    actions_executed: str
    redirect_url: str
    error_reason: str
    target_port_list: str
    target_status_code_list: str
    classification: str
    classification_reason: str
