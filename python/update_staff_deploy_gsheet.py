import argparse
import os
import gspread
import json
import github_pr_funcs


def update(app: str, pr_url: str, token: str):
    service_account = json.loads(os.getenv('GOOGLE_SERVICE_ACCOUNT'))
    auth = gspread.service_account_from_dict(service_account)
    sheet = auth.open_by_key("1-IQJ0kTyenqZFeS1qeUZvD6oKls2WnlYwSts9IwwtHQ")
    correct_col = sheet.sheet1.find('PR')
    if correct_col is None:
        raise ValueError("Column 'PR' not found in the sheet")

    correct_row = sheet.sheet1.find(app, case_sensitive=False)
    if correct_row is None:
        raise ValueError(f"App '{app}' not found in the sheet")

    pr_id = github_pr_funcs.get_pr_from_raw_pr_url(token, pr_url)

    sheet.sheet1.update_cell(correct_row.row, correct_col.col, pr_id)


parser = argparse.ArgumentParser(description='Update staff deployment Google Sheet')
parser.add_argument('--app', type=str, help='Dokku app name', required=True)
parser.add_argument('--pr_url', type=str, help='Pull request url', required=True)
parser.add_argument('--token', type=str, help='GitHub Token', required=True)
args = parser.parse_args()
if __name__ == "__main__":
    update(args.app, args.pr_url, args.token)