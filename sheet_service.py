from datetime import datetime
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

def append_product_row(
    date_text,
    time_text,
    product_name,
    quantity,
    amount,
):
    worksheet = get_sales_worksheet()

    worksheet.append_row(
        [
            date_text,
            time_text,
            "ขายสินค้า",
            amount,
            "",
            product_name,
            quantity,
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

        if (
            row_date == date_text
            and row_type in ["ยอดขาย", "ขายสินค้า"]
        ):
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

def get_product_rows_by_date(date_text):
    worksheet = get_sales_worksheet()
    records = worksheet.get_all_records()

    product_rows = []

    for row in records:
        row_date = str(row.get("วันที่", "")).strip()
        row_type = str(row.get("ประเภท", "")).strip()

        if row_date == date_text and row_type == "ขายสินค้า":
            product_rows.append(row)

    return product_rows

def get_rows_by_date_range(start_date, end_date):
    """
    อ่านข้อมูลทั้งหมดที่อยู่ในช่วงวันที่กำหนด

    start_date และ end_date ต้องเป็น date object
    """

    worksheet = get_sales_worksheet()
    records = worksheet.get_all_records()

    rows_in_range = []

    for row in records:
        row_date_text = str(
            row.get("วันที่", "")
        ).strip()

        try:
            row_date = datetime.strptime(
                row_date_text,
                "%d/%m/%Y",
            ).date()
        except (ValueError, TypeError):
            continue

        if start_date <= row_date <= end_date:
            rows_in_range.append(row)

    return rows_in_range   

def get_product_rows_by_date(date_text):
    """
    ดึงรายการขายสินค้าตามวันที่
    """

    worksheet = get_sales_worksheet()
    records = worksheet.get_all_records()

    product_rows = []

    for row in records:
        row_date = str(row.get("วันที่", "")).strip()
        row_type = str(row.get("ประเภท", "")).strip()

        if row_date == date_text and row_type == "ขายสินค้า":
            product_rows.append(row)

    return product_rows
