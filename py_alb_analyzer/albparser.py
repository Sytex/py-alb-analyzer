import re
from datetime import datetime

from py_alb_analyzer.log_entry import LogEntry


def parse_log_entry(log_entry_line: str) -> LogEntry:
    parts = re.findall(r'(?:[^\s,"]|"(?:\\.|[^"])*")+', log_entry_line.strip())
    parts = [p[1:-1] if p.startswith('"') and p.endswith('"') else p for p in parts]

    try:
        client_address, client_port = (
            ("", "") if parts[3] == "-" else parts[3].split(":")
        )
        target_addres, target_port = (
            ("", "") if parts[4] == "-" else parts[4].split(":")
        )
    except ValueError as e:
        raise ValueError(f"Error address and port: {parts[3]} {parts[4]}") from e

    try:
        log_entry = LogEntry(
            type=parts[0],
            # Fromat is 2023-09-18T23:55:00.399201Z convert to datetime
            time=datetime.strptime(parts[1], "%Y-%m-%dT%H:%M:%S.%fZ"),
            elb=parts[2],
            client_address=client_address,
            client_port=client_port,
            target_address=target_addres,
            target_port=target_port,
            request_processing_time=float(parts[5]),
            target_processing_time=float(parts[6]),
            response_processing_time=float(parts[7]),
            elb_status_code=int(parts[8]),
            target_status_code=int(parts[9]) if parts[9] != "-" else None,
            received_bytes=int(parts[10]),
            sent_bytes=int(parts[11]),
            request=parts[12],
            user_agent=parts[13],
            ssl_cipher=parts[14],
            ssl_protocol=parts[15],
            target_group_arn=parts[16],
            trace_id=parts[17],
            domain_name=parts[18],
            chosen_cert_arn=parts[19],
            matched_rule_priority=None if parts[20] == "-" else int(parts[20]),
            request_creation_time=parts[21],
            actions_executed=parts[22],
            redirect_url=parts[23],
            error_reason=parts[24],
            target_port_list=parts[25],
            target_status_code_list=parts[26],
            classification=parts[27],
            classification_reason=parts[28],
        )
    except ValueError as e:
        raise ValueError(f"Error parsing log entry: {log_entry_line}") from e

    return log_entry
