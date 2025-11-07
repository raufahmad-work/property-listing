from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

import smtplib
from email.message import EmailMessage

from script.config import EMAIL_SENDER, EMAIL_PASSWORD
from script.database import SentListing


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


def send_email(file_paths, file_names, to_email):
    msg = EmailMessage()
    msg["Subject"] = "Zillow and Street Easy Listings"
    msg["From"] = EMAIL_SENDER
    msg["To"] = to_email
    msg.set_content("Hi,\n\nPlease find attached the files for Zillow and Street Easy listings.\n\nCheers!")

    # Attach files
    for i, path in enumerate(file_paths):
        with open(path, "rb") as f:
            file_data = f.read()
            msg.add_attachment(file_data, maintype="application", subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename=f"{file_names[i]}.xlsx")

    # Send
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.send_message(msg)

    print("✅ Email sent successfully!")


def filter_new_listings(listings):
    """
    Filters out listings already stored in the database (bulk check).
    """
    urls = [listing.get("URL") for listing in listings if listing.get("URL")]

    if not urls:
        return listings

    existing = (
        SentListing
        .select(SentListing.url)
        .where(SentListing.url.in_(urls))
        .dicts()
        .execute()
    )

    # Step 2: Convert dicts -> plain set of URLs
    existing_urls = {item["url"] for item in existing}

    # Step 3: Filter listings
    new_listings = [listing for listing in listings if listing.get("URL") not in existing_urls]

    return new_listings


def create_records_in_db(data):
    """
    Bulk-inserts new listings into the SentListing table.
    """
    records = []
    for borough, listings in data.items():
        for listing in listings:
            url = listing.get("URL")
            if not url:
                continue
            records.append({
                "url": url,
                "source": "streeteasy" if "streeteasy" in url else "zillow",
                "borough": borough,
            })

    if not records:
        print("No new listings to insert.")
        return

    try:
        with SentListing._meta.database.atomic():
            SentListing.insert_many(records).on_conflict_ignore().execute()
        print(f"Inserted {len(records)} new listings.")
    except Exception as e:
        print("Error inserting records:", e)
