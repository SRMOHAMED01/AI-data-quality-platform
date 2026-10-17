import logging
import os
from typing import Dict, Any, Optional

import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


def send_slack_alert(message: str, webhook_url: Optional[str] = None) -> bool:
    url = webhook_url or os.getenv('SLACK_WEBHOOK_URL')
    if not url:
        logger.warning('No Slack webhook URL configured')
        return False
    try:
        resp = requests.post(url, json={'text': message}, timeout=10)
        if resp.status_code in (200, 202):
            return True
        logger.warning('Slack alert failed with status %d: %s', resp.status_code, resp.text)
        return False
    except Exception as e:
        logger.exception('Error sending Slack alert: %s', e)
        return False


def send_teams_alert(message: str, webhook_url: Optional[str] = None) -> bool:
    url = webhook_url or os.getenv('TEAMS_WEBHOOK_URL')
    if not url:
        logger.warning('No Teams webhook URL configured')
        return False
    try:
        payload = {
            '@type': 'MessageCard',
            '@context': 'http://schema.org/extensions',
            'summary': 'Data Quality Alert',
            'text': message,
        }
        resp = requests.post(url, json=payload, timeout=10)
        if resp.status_code in (200, 202):
            return True
        logger.warning('Teams alert failed with status %d: %s', resp.status_code, resp.text)
        return False
    except Exception as e:
        logger.exception('Error sending Teams alert: %s', e)
        return False


def build_alert_message(quality_report: Dict[str, Any]) -> str:
    global_pct = quality_report.get('global_conformity_pct', 0)
    rules = quality_report.get('rules', [])
    critical = [r for r in rules if r.get('severity') == 'critical' and r.get('conformity_pct', 100) < 90]
    low = [r for r in rules if r.get('conformity_pct', 100) < 90]
    ml_total = quality_report.get('ml_anomalies', {}).get('total_detected', 0)
    not_covered = quality_report.get('ml_anomalies', {}).get('not_covered_by_rules', 0)
    parts = [f'Data Quality Alert — Global conformity: {global_pct}%']
    if low:
        parts.append(f'{len(low)} rule(s) below 90% conformity')
    if critical:
        parts.append(f'Critical rules affected: {len(critical)}')
    if ml_total:
        parts.append(f'{ml_total} ML anomalies detected ({not_covered} not covered by rules)')
    return '; '.join(parts)


def should_alert(quality_report: Dict[str, Any], threshold: float = 0.9) -> bool:
    global_pct = quality_report.get('global_conformity_pct', 100)
    if global_pct / 100.0 < threshold:
        return True
    for r in quality_report.get('rules', []):
        if r.get('severity') in ('high', 'critical') and r.get('conformity_pct', 100) / 100.0 < threshold:
            return True
    if quality_report.get('ml_anomalies', {}).get('not_covered_by_rules', 0) > 0:
        return True
    return False
