import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

import pandas as pd


def build_report(rule_results: Dict[str, Any], ml_results: pd.DataFrame, total_rows: int = None) -> Dict[str, Any]:
    if total_rows is None:
        if ml_results is not None and not ml_results.empty:
            total_rows = len(ml_results)
        else:
            total_rows = 0

    rules_list: List[Dict[str, Any]] = []
    global_pass = 0
    global_fail = 0
    for rule_name, info in rule_results.items():
        pass_c = info.get('pass', 0)
        fail_c = info.get('fail', 0)
        rules_list.append({
            'rule': rule_name,
            'column': info.get('column'),
            'conformity_pct': info.get('conformity_pct', 0.0),
            'severity': info.get('severity'),
            'failed_count': fail_c,
            'pass_count': pass_c,
        })
        global_pass += pass_c
        global_fail += fail_c

    global_conformity_pct = round((global_pass / (global_pass + global_fail)) * 100.0, 2) if (global_pass + global_fail) > 0 else 0.0

    ml_anomalies_total = 0
    top_suspicious_rows = []
    if ml_results is not None and not ml_results.empty:
        if 'is_anomaly' in ml_results.columns:
            ml_anomalies_total = int(ml_results['is_anomaly'].sum())
        if 'anomaly_score' in ml_results.columns:
            sorted_df = ml_results.sort_values('anomaly_score').head(10)
        else:
            sorted_df = ml_results.head(10)
        top_suspicious_rows = sorted_df.to_dict(orient='records')

    report = {
        'run_timestamp': datetime.utcnow().isoformat() + 'Z',
        'total_rows': total_rows,
        'global_conformity_pct': global_conformity_pct,
        'rules': rules_list,
        'ml_anomalies': {
            'total_detected': ml_anomalies_total,
            'not_covered_by_rules': 0,
            'top_suspicious_rows': top_suspicious_rows,
        },
    }
    return report


def export_json(report: Dict[str, Any], path: str = 'report/latest_report.json') -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)


def export_html(report: Dict[str, Any], path: str = 'report/latest_report.html') -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    html = []
    html.append('<html><head><meta charset="utf-8"><title>Data Quality Report</title></head><body>')
    html.append(f"<h1>Data Quality Report</h1>")
    html.append(f"<p>Timestamp: {report.get('run_timestamp')}</p>")
    html.append(f"<p>Total rows: {report.get('total_rows')}</p>")
    html.append(f"<p>Global conformity: {report.get('global_conformity_pct')}%</p>")
    html.append('<h2>Rules</h2><table border="1"><tr><th>Column</th><th>Rule</th><th>Conformity %</th><th>Severity</th><th>Failed</th></tr>')
    for r in report.get('rules', []):
        html.append(f"<tr><td>{r.get('column') or ''}</td><td>{r.get('rule') or ''}</td><td>{r.get('conformity_pct')}</td><td>{r.get('severity') or ''}</td><td>{r.get('failed_count')}</td></tr>")
    html.append('</table>')
    html.append(f"<h2>ML Anomalies</h2><p>Total detected: {report['ml_anomalies'].get('total_detected')}</p>")
    html.append('</body></html>')
    p.write_text('\n'.join(html), encoding='utf-8')
