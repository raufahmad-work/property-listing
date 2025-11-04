from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter


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
