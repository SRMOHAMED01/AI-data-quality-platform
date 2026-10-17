import logging
import os
from pathlib import Path

from src.db.connection import init_db
from src.llm.rule_generator import load_schema, generate_rules, save_rules
from src.rules_engine.rule_engine import load_data, load_rules, run_all_rules
from src.ml.train_model import train_and_save
from src.ml.anomaly_detector import load_model, detect_anomalies, compare_with_rules
from src.report.report_generator import build_report, export_json, export_html
from src.alerting.notifier import should_alert, send_slack_alert, build_alert_message

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL')


def main():
    try:
        logger.info('Step 1/6 - Loading schema...')
        schema = load_schema('schema/table_schema.json')

        logger.info('Step 2/6 - Generating rules via LLM...')
        try:
            rules = generate_rules(schema)
            save_rules(rules, 'rules/generated_rules.json')
        except Exception as e:
            logger.warning('Rule generation failed (%s); trying to load existing rules', e)
            rules = load_rules('rules/generated_rules.json')

        logger.info('Step 3/6 - Applying rules to data...')
        df = load_data('data/sample_transactions.csv')
        rule_results = run_all_rules(df, rules)

        logger.info('Step 4/6 - Detecting anomalies with ML...')
        try:
            model = load_model('models/isolation_forest.joblib')
        except Exception as e:
            logger.warning('Model not found (%s); training model...', e)
            train_and_save('data/sample_transactions.csv', 'models/isolation_forest.joblib')
            model = load_model('models/isolation_forest.joblib')
        ml_results = detect_anomalies(df, model)

        logger.info('Step 5/6 - Building report...')
        report = build_report(rule_results, ml_results, total_rows=len(df))
        cmp = compare_with_rules(ml_results, rule_results)
        report['ml_anomalies']['not_covered_by_rules'] = cmp['not_covered_by_rules']
        export_json(report, 'report/latest_report.json')
        export_html(report, 'report/latest_report.html')

        logger.info('Step 6/6 - Checking alert conditions...')
        if should_alert(report):
            send_slack_alert(build_alert_message(report), SLACK_WEBHOOK_URL)

        logger.info('Pipeline completed successfully.')
    except Exception as e:
        logger.exception('Pipeline failed: %s', e)
        raise


if __name__ == '__main__':
    init_db()
    main()
