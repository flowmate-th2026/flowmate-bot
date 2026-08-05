import gspread
import os

from config import GOOGLE_CREDENTIALS_FILE, GOOGLE_SHEET_ID
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

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

    คืนข้อมูลร้านทุกสถานะ:
    active, pending และ inactive
    """

    worksheet = get_registry_worksheet()
    records = worksheet.get_all_records()

    target_line_user_id = str(line_user_id).strip()

    for row in records:
        row_line_user_id = str(
            row.get("line_user_id", "")
        ).strip()

        if row_line_user_id == target_line_user_id:
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
                "status": str(
                    row.get("status", "")
                ).strip().lower(),
                "trial_start": str(
                    row.get("trial_start", "")
                ).strip(),
                "trial_end": str(
                    row.get("trial_end", "")
                ).strip(),
                "plan_name": str(
                row.get("plan_name", "")
                ).strip(),
            }

    return None

def register_shop_request(
    line_user_id,
    shop_name,
):
    """
    เพิ่มคำขอลงทะเบียนร้านใหม่ใน Shop Registry

    ร้านที่เพิ่งลงทะเบียนจะมีสถานะ pending
    และยังไม่มี sheet_id
    """

    worksheet = get_registry_worksheet()
    records = worksheet.get_all_records()

    target_line_user_id = str(
        line_user_id
    ).strip()

    cleaned_shop_name = str(
        shop_name
    ).strip()

    # ตรวจสอบว่า LINE User ID นี้เคยลงทะเบียนหรือยัง
    for row in records:
        existing_line_user_id = str(
            row.get("line_user_id", "")
        ).strip()

        if existing_line_user_id == target_line_user_id:
            return {
                "success": False,
                "reason": "already_registered",
                "shop_id": str(
                    row.get("shop_id", "")
                ).strip(),
                "shop_name": str(
                    row.get("shop_name", "")
                ).strip(),
                "status": str(
                    row.get("status", "")
                ).strip().lower(),
            }

    # หาเลขร้านลำดับถัดไป
    highest_number = 0

    for row in records:
        shop_id = str(
            row.get("shop_id", "")
        ).strip().upper()

        if shop_id.startswith("SHOP"):
            number_text = shop_id.replace(
                "SHOP",
                "",
                1,
            )

            try:
                shop_number = int(number_text)
                highest_number = max(
                    highest_number,
                    shop_number,
                )
            except ValueError:
                continue

    new_shop_id = f"SHOP{highest_number + 1:03d}"

    worksheet.append_row(
        [
            new_shop_id,
            cleaned_shop_name,
            target_line_user_id,
            "",
            "pending",
        ],
        value_input_option="USER_ENTERED",
    )

    return {
        "success": True,
        "reason": "created",
        "shop_id": new_shop_id,
        "shop_name": cleaned_shop_name,
        "status": "pending",
    }

def get_pending_shops():
    """
    คืนรายการร้านที่อยู่ในสถานะ pending
    """

    worksheet = get_registry_worksheet()
    records = worksheet.get_all_records()

    pending_shops = []

    for row in records:
        status = str(
            row.get("status", "")
        ).strip().lower()

        if status == "pending":
            pending_shops.append(
                {
                    "shop_id": str(
                        row.get("shop_id", "")
                    ).strip(),
                    "shop_name": str(
                        row.get("shop_name", "")
                    ).strip(),
                    "line_user_id": str(
                        row.get("line_user_id", "")
                    ).strip(),
                    "sheet_id": str(
                        row.get("sheet_id", "")
                    ).strip(),
                    "status": status,
                }
            )

    return pending_shops

def activate_shop(
    shop_id,
    sheet_id,
):
    """
    เปิดใช้งานร้านโดยใส่ Sheet ID
    และเปลี่ยนสถานะเป็น active
    """

    worksheet = get_registry_worksheet()
    records = worksheet.get_all_records()

    target_shop_id = str(shop_id).strip().upper()
    target_sheet_id = str(sheet_id).strip()

    if not target_shop_id:
        return {
            "success": False,
            "reason": "missing_shop_id",
        }

    if not target_sheet_id:
        return {
            "success": False,
            "reason": "missing_sheet_id",
        }

    for row_index, row in enumerate(
        records,
        start=2,
    ):
        current_shop_id = str(
            row.get("shop_id", "")
        ).strip().upper()

        if current_shop_id == target_shop_id:
            shop_name = str(
                row.get("shop_name", "")
            ).strip()

            worksheet.update_cell(
                row_index,
                4,
                target_sheet_id,
            )

            worksheet.update_cell(
                row_index,
                5,
                "active",
            )

            return {
                "success": True,
                "reason": "activated",
                "shop_id": target_shop_id,
                "shop_name": shop_name,
                "sheet_id": target_sheet_id,
                "status": "active",
            }

    return {
        "success": False,
        "reason": "shop_not_found",
        "shop_id": target_shop_id,
    }

def renew_shop_plan(
    shop_id,
    days,
    plan_name,
):
    """
    ต่ออายุสิทธิ์ใช้งานร้าน และเปลี่ยนชื่อแพ็กเกจ
    """

    worksheet = get_registry_worksheet()
    records = worksheet.get_all_records()

    target_shop_id = str(shop_id).strip().upper()
    cleaned_plan_name = str(plan_name).strip()

    try:
        renewal_days = int(days)
    except (ValueError, TypeError):
        return {
            "success": False,
            "reason": "invalid_days",
        }

    if renewal_days <= 0:
        return {
            "success": False,
            "reason": "invalid_days",
        }

    if not cleaned_plan_name:
        return {
            "success": False,
            "reason": "missing_plan_name",
        }

    today = datetime.now(
        ZoneInfo("Asia/Bangkok")
    ).date()

    for row_index, row in enumerate(
        records,
        start=2,
    ):
        current_shop_id = str(
            row.get("shop_id", "")
        ).strip().upper()

        if current_shop_id != target_shop_id:
            continue

        shop_name = str(
            row.get("shop_name", "")
        ).strip()

        current_end_text = str(
            row.get("trial_end", "")
        ).strip()

        try:
            current_end = datetime.strptime(
                current_end_text,
                "%d/%m/%Y",
            ).date()
        except ValueError:
            current_end = today

        base_date = max(
            today,
            current_end,
        )

        new_end_date = base_date + timedelta(
            days=renewal_days
        )

        new_end_text = new_end_date.strftime(
            "%d/%m/%Y"
        )

        worksheet.update_cell(
            row_index,
            7,
            new_end_text,
        )

        worksheet.update_cell(
            row_index,
            8,
            cleaned_plan_name,
        )

        worksheet.update_cell(
            row_index,
            5,
            "active",
        )

        return {
            "success": True,
            "reason": "renewed",
            "shop_id": target_shop_id,
            "shop_name": shop_name,
            "plan_name": cleaned_plan_name,
            "days_added": renewal_days,
            "new_end_date": new_end_text,
            "status": "active",
        }

    return {
        "success": False,
        "reason": "shop_not_found",
        "shop_id": target_shop_id,
    }

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

def get_shop_spreadsheet(sheet_id):
    """
    เปิด Google Spreadsheet ของแต่ละร้าน
    """

    google_client = gspread.service_account(
        filename=GOOGLE_CREDENTIALS_FILE
    )

    return google_client.open_by_key(sheet_id)

def get_shop_sales_worksheet(sheet_id):
    """
    เปิดชีต Sales ของร้าน
    """

    spreadsheet = get_shop_spreadsheet(sheet_id)

    return spreadsheet.worksheet("Sales")

def get_shop_expense_worksheet(sheet_id):
    """
    เปิดชีต Expense ของร้าน
    """

    spreadsheet = get_shop_spreadsheet(sheet_id)

    return spreadsheet.worksheet("Expense")
