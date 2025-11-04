from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

import smtplib
from email.message import EmailMessage

from script.config import EMAIL_SENDER, EMAIL_PASSWORD


def create_file(boroughs_data, filename):
    # Create workbook
    wb = Workbook()
    wb.remove(wb.active)

    # Styles
    bold_font = Font(bold=True)
    header_fill = PatternFill(start_color="FFD9D9D9", end_color="FFD9D9D9", fill_type="solid")  # Light gray fill

    # Populate sheets
    for borough, data in boroughs_data.items():
        ws = wb.create_sheet(title=borough)
        ws.freeze_panes = "A2"

        if data:
            headers = list(data[0].keys())

            # Write headers with bold and background fill
            ws.append(headers)
            for col_num, _ in enumerate(headers, 1):
                cell = ws.cell(row=1, column=col_num)
                cell.font = bold_font
                cell.fill = header_fill

            # Write rows
            for row in data:
                ws.append(list(row.values()))

            # Auto-size columns
            for col in ws.columns:
                max_len = max(len(str(c.value)) for c in col if c.value is not None)
                ws.column_dimensions[get_column_letter(col[0].column)].width = max_len + 2

    # Save file
    wb.save(f"{filename}.xlsx")


def send_email(file_path, file_name, to_email):
    msg = EmailMessage()
    msg["Subject"] = "Zillow and Street Easy Listings"
    msg["From"] = EMAIL_SENDER
    msg["To"] = to_email
    msg.set_content("Hi,\n\nPlease find attached the file for Zillow and Street Easy listings.\n\nCheers!")

    # Attach file
    with open(file_path, "rb") as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype="application", subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename=f"{file_name}.xlsx")

    # Send
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.send_message(msg)

    print("✅ Email sent successfully!")
