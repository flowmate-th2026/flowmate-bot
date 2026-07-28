import gspread

from config import GOOGLE_CREDENTIALS_FILE, GOOGLE_SHEET_ID


def get_sales_worksheet():
    google_client = gspread.service_account(
        filename=GOOGLE_CREDENTIALS_FILE
    )

    spreadsheet = google_client.open_by_key(GOOGLE_SHEET_ID)
    worksheet = spreadsheet.get_worksheet(0)

    return worksheet


def append_sale_row(date_text, time_text, amount):
    worksheet = get_sales_worksheet()

    worksheet.append_row(
        [
            date_text,
            time_text,
            "ยอดขาย",
            amount,
            "",
        ],
        value_input_option="USER_ENTERED",
    )


def append_expense_row(date_text, time_text, amount, description):
    worksheet = get_sales_worksheet()

    worksheet.append_row(
        [
            date_text,
            time_text,
            "ค่าใช้จ่าย",
            amount,
            description,
        ],
        value_input_option="USER_ENTERED",
    )

def append_customer_row(date_text, time_text, customer_count):
    worksheet = get_sales_worksheet()

    worksheet.append_row(
        [
            date_text,
            time_text,
            "ลูกค้า",
            customer_count,
            "",
        ],
        value_input_option="USER_ENTERED",
    )
def get_sales_rows_by_date(date_text):
    worksheet = get_sales_worksheet()
    records = worksheet.get_all_records()

    sales_rows = []

    for row in records:
        row_date = str(row.get("วันที่", "")).strip()
        row_type = str(row.get("ประเภท", "")).strip()

        if row_date == date_text and row_type == "ยอดขาย":
            sales_rows.append(row)

    return sales_rows


def get_expense_rows_by_date(date_text):
    worksheet = get_sales_worksheet()
    records = worksheet.get_all_records()

    expense_rows = []

    for row in records:
        row_date = str(row.get("วันที่", "")).strip()
        row_type = str(row.get("ประเภท", "")).strip()

        if row_date == date_text and row_type == "ค่าใช้จ่าย":
            expense_rows.append(row)

    return expense_rows
    
def get_customer_rows_by_date(date_text):
    worksheet = get_sales_worksheet()
    records = worksheet.get_all_records()

    customer_rows = []

    for row in records:
        row_date = str(row.get("วันที่", "")).strip()
        row_type = str(row.get("ประเภท", "")).strip()

        if row_date == date_text and row_type == "ลูกค้า":
            customer_rows.append(row)

    return customer_rows
    
