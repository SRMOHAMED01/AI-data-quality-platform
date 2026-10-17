import json
from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(page_title='Data Quality Dashboard', layout='wide')

def load_report(path='report/latest_report.json'):
    p = Path(path)
    if not p.exists():
        return None
    with p.open('r', encoding='utf-8') as f:
        return json.load(f)


def main():
    st.title('Data Quality Dashboard')
    report = load_report()
    if report is None:
        st.warning('No report found. Run pipeline first (python main.py)')
        return
    st.sidebar.header('Run info')
    st.sidebar.write(f"Timestamp: {report.get('run_timestamp')}")
    col1, col2, col3 = st.columns(3)
    col1.metric('Global Conformity', f"{report.get('global_conformity_pct')}%")
    col2.metric('Total Rows', report.get('total_rows'))
    col3.metric('ML Anomalies', report['ml_anomalies'].get('total_detected', 0))
    st.subheader('Rules (LLM generated)')
    rules_df = pd.DataFrame(report.get('rules', []))
    if not rules_df.empty:
        st.dataframe(rules_df)
    else:
        st.info('No rules in report')
    st.subheader('ML Anomalies')
    st.write(f"Total detected: {report['ml_anomalies'].get('total_detected')}")
    st.write(f"Not covered by rules: {report['ml_anomalies'].get('not_covered_by_rules')}")
    st.subheader('Top suspicious rows')
    top = pd.DataFrame(report['ml_anomalies'].get('top_suspicious_rows', []))
    if not top.empty:
        st.dataframe(top)
    st.subheader('Raw report (JSON)')
    st.json(report)


if __name__ == '__main__':
    main()
