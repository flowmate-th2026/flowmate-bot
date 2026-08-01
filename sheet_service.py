from datetime import datetime
import gspread
import os

from config import GOOGLE_CREDENTIALS_FILE, GOOGLE_SHEET_ID

def get_registry_worksheet():
    """
    เปิดชีตทะเบียนร้านค้ากลาง
    """

    registry_sheet_id = os.getenv("REGISTRY_SHEET_ID")

    if not registry_sheet_id:
        raise ValueError(
            "ไม่พบ REGISTRY_SHEET_ID ใน Environment"
        )

    google_client = gspread.service_account(
        filename=GOOGLE_CREDENTIALS_FILE
    )

    spreadsheet = google_client.open_by_key(
        registry_sheet_id
    )

    return spreadsheet.get_worksheet(0)
    
def get_shop_by_line_user_id(line_user_id):
    """
    ค้นหาข้อมูลร้านค้าจาก LINE User ID
    """

    worksheet = get_registry_worksheet()
    records = worksheet.get_all_records()

    target_line_user_id = str(line_user_id).strip()

    for row in records:
        row_line_user_id = str(
            row.get("line_user_id", "")
        ).strip()

        status = str(
            row.get("status", "")
        ).strip().lower()

        if (
            row_line_user_id == target_line_user_id
            and status == "active"
        ):
            return {
                "shop_id": str(
                    row.get("shop_id", "")
                ).strip(),
                "shop_name": str(
                    row.get("shop_name", "")
                ).strip(),
                "line_user_id": row_line_user_id,
                "sheet_id": str(
                    row.get("sheet_id", "")
                ).strip(),
                "status": status,
            }

    return None
    
def get_sales_worksheet(sheet_id=None):
    """
    เปิดชีตข้อมูลร้านค้า

    ถ้ามี sheet_id จะเปิดชีตของร้านนั้น
    ถ้าไม่มี จะใช้ชีตร้านต้นแบบเดิม
    """

    google_client = gspread.service_account(
        filename=GOOGLE_CREDENTIALS_FILE
    )

    target_sheet_id = sheet_id or GOOGLE_SHEET_ID

    spreadsheet = google_client.open_by_key(
        target_sheet_id
    )

    return spreadsheet.get_worksheet(0)

def append_sale_row(
    date_text,
    time_text,
    amount,
    sheet_id=None,
):
    worksheet = get_sales_worksheet(sheet_id)

    worksheet.append_row(
        [
            date_text,
            time_text,
            "ยอดขาย",
            amount,
            "",
            "",
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
    sheet_id=None,
):
    worksheet = get_sales_worksheet(sheet_id)

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

def append_expense_row(
    date_text,
    time_text,
    amount,
    description,
    sheet_id=None,
):
    worksheet = get_sales_worksheet(sheet_id)

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

def append_customer_row(
    date_text,
    time_text,
    customer_count,
    sheet_id=None,
):
    worksheet = get_sales_worksheet(sheet_id)

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

def get_sales_rows_by_date(
    date_text,
    sheet_id=None,
):
    worksheet = get_sales_worksheet(sheet_id)
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

def get_expense_rows_by_date(
    date_text,
    sheet_id=None,
):
    worksheet = get_sales_worksheet(sheet_id)
    records = worksheet.get_all_records()

    expense_rows = []

    for row in records:
        row_date = str(row.get("วันที่", "")).strip()
        row_type = str(row.get("ประเภท", "")).strip()

        if (
            row_date == date_text
            and row_type == "ค่าใช้จ่าย"
        ):
            expense_rows.append(row)

    return expense_rows
    
def get_customer_rows_by_date(
    date_text,
    sheet_id=None,
):
    worksheet = get_sales_worksheet(sheet_id)
    records = worksheet.get_all_records()

    customer_rows = []

    for row in records:
        row_date = str(row.get("วันที่", "")).strip()
        row_type = str(row.get("ประเภท", "")).strip()

        if (
            row_date == date_text
            and row_type == "ลูกค้า"
        ):
            customer_rows.append(row)

    return customer_rows

def get_product_rows_by_date(
    date_text,
    sheet_id=None,
):
    worksheet = get_sales_worksheet(sheet_id)
    records = worksheet.get_all_records()

    product_rows = []

    for row in records:
        row_date = str(row.get("วันที่", "")).strip()
        row_type = str(row.get("ประเภท", "")).strip()

        if (
            row_date == date_text
            and row_type == "ขายสินค้า"
        ):
            product_rows.append(row)

    return product_rows

def get_shop_product_rows_by_date(
    date_text,
    sheet_id=None,
):
    """
    ดึงรายการขายสินค้าตามวันที่และร้านค้า
    """

    worksheet = get_sales_worksheet(sheet_id)
    records = worksheet.get_all_records()

    product_rows = []

    for row in records:
        row_date = str(
            row.get("วันที่", "")
        ).strip()

        row_type = str(
            row.get("ประเภท", "")
        ).strip()

        if (
            row_date == date_text
            and row_type == "ขายสินค้า"
        ):
            product_rows.append(row)

    return product_rows
    
def get_rows_by_date_range(
    start_date,
    end_date,
    sheet_id=None,
):
    """
    อ่านข้อมูลทั้งหมดที่อยู่ในช่วงวันที่กำหนด

    start_date และ end_date ต้องเป็น date object
    """

    worksheet = get_sales_worksheet(sheet_id)
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
