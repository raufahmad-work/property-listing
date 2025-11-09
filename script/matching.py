import re
from openpyxl import load_workbook


search_type_mapping = {"rent": "FOR_RENT", "sale": "FOR_SALE"}


ABBR_MAP = {
    r"\bE\b": "EAST",
    r"\bW\b": "WEST",
    r"\bN\b": "NORTH",
    r"\bS\b": "SOUTH",
    r"\bST\b": "STREET",
    r"\bRD\b": "ROAD",
    r"\bAVE\b": "AVENUE",
    r"\bAV\b": "AVENUE",
    r"\bBLVD\b": "BOULEVARD",
    r"\bPL\b": "PLACE",
    r"\bCTR\b": "CENTER",
    r"\bLN\b": "LANE",
    r"\bHWY\b": "HIGHWAY",
    r"\bPKWY\b": "PARKWAY",
}


ORDINAL_RE = re.compile(r"(\d+)(ST|ND|RD|TH)\b", flags=re.IGNORECASE)
MULTI_WS_RE = re.compile(r"\s+")
UNIT_RE = re.compile(r"\b(?:APT|APARTMENT|UNIT|#|STE|SUITE|FL|FLOOR)\b\.?\s*\w*\b.*$", flags=re.IGNORECASE)
PUNCT_RE = re.compile(r"[\.]")  # remove periods but keep commas for splitting if needed


def normalize_component(text: str) -> str:
    """Upper-case, remove periods, expand abbreviations, remove ordinal suffixes, normalize spaces."""
    if not text:
        return ""
    s = str(text).upper()
    # Remove periods (E.g., "ST." -> "ST")
    s = PUNCT_RE.sub("", s)
    # Remove apartment/unit tail if any
    s = UNIT_RE.sub("", s).strip()
    # Replace ordinals like 33RD -> 33
    s = ORDINAL_RE.sub(r"\1", s)
    # Replace abbreviations with full words
    for pat, repl in ABBR_MAP.items():
        s = re.sub(pat, repl, s, flags=re.IGNORECASE)
    # Collapse whitespace
    s = MULTI_WS_RE.sub(" ", s).strip()
    # Remove stray commas/spaces around commas and normalize them to single comma + space
    s = re.sub(r"\s*,\s*", ", ", s)
    return s


def canonicalize_combined_address(raw_combined: str, expect_city_handling=False) -> str:
    """
    Turn an address like:
      "429 E 52ND ST APT 31C, NEW YORK, NY, 10022"
    into canonical form:
      "429 EAST 52 STREET, NEW YORK, NY, 10022"
    Or if expect_city_handling=True, it tries to keep borough normalization intact.
    """
    if not raw_combined:
        return ""
    # Split on commas to get pieces (street, city/borough, state, zip)
    parts = [p.strip() for p in raw_combined.split(",")]
    # Ensure at least street, city, state, zip positions exist
    # We'll safely index from the right so missing commas still work
    parts_rev = list(reversed(parts))
    zip_part = parts_rev[0] if len(parts_rev) >= 1 else ""
    state_part = parts_rev[1] if len(parts_rev) >= 2 else ""
    city_part = parts_rev[2] if len(parts_rev) >= 3 else ""
    # The rest (everything left of these) is street address
    street_part = ", ".join(reversed(parts_rev[3:])) if len(parts_rev) > 3 else parts[0]

    street_norm = normalize_component(street_part)
    city_norm = normalize_component(city_part)
    state_norm = normalize_component(state_part)
    zip_norm = normalize_component(zip_part)

    # Special handling: some input uses 'MANHATTAN' but the file uses 'NEW YORK' -> unify
    if city_norm == "MANHATTAN":
        city_norm = "NEW YORK"

    # Reassemble in a consistent format (commas + single spaces)
    canonical = ", ".join([p for p in (street_norm, city_norm, state_norm, zip_norm) if p])
    return canonical


def get_combined_addresses(file_path="script/addresses.xlsx"):
    """Return a set of canonical combined addresses (normalized) across all sheets (headers on 6th row)."""
    wb = load_workbook(file_path, data_only=True)
    combined_addresses = set()

    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        # read header row (6th row)
        headers = [str(c.value).strip().upper() if c.value else "" 
                   for c in next(ws.iter_rows(min_row=6, max_row=6))]
        
        # If the sheet provides a 'COMBINED ADDRESS' column, use it; otherwise skip.
        if "COMBINED ADDRESS" not in headers:
            continue

        address_idx = headers.index("COMBINED ADDRESS")  # 0-based index for values_only rows

        for row in ws.iter_rows(min_row=7, values_only=True):
            raw_val = row[address_idx] if address_idx < len(row) else None
            if not raw_val:
                continue
            canonical = canonicalize_combined_address(str(raw_val))
            if canonical:
                combined_addresses.add(canonical)

    return combined_addresses


def filter_streeteasy_addresses_from_file(items, type):
    file_addresses = get_combined_addresses()
    filtered = []
    email_data = []
    for item in items:
        if item.get("status", -100) == 1:
            street = item.get("addr_street", "") or ""
            borough = item.get("addr_city", "") or ""
            state = item.get("addr_state", "") or ""
            zip_code = item.get("addr_zip") or ""
            # Build the same combined format you used before, then canonicalize
            if borough.upper() == "MANHATTAN":
                combined_address = f"{street}, NEW YORK, {state}, {zip_code}"
            else:
                combined_address = f"{street}, {borough}, {state}, {zip_code}"

            print("Scraped Combined Address (raw): ", combined_address)
            canonical = canonicalize_combined_address(combined_address)
            print("Scraped Combined Address (canonical): ", canonical)
            if canonical in file_addresses:
                print("---------------------- Found ----------------------")
                email_data.append({
                    "Address": canonical,
                    "Type": search_type_mapping.get(type),
                    "URL": item.get("url"),
                    "Date Listed": item.get("created_at"),
                })
                filtered.append(item)

    return email_data


def filter_zillow_addresses_from_file(items):
    file_addresses = get_combined_addresses()
    filtered = []
    email_data = []
    for item in items:
        home_status = (item.get("homeStatus") or "").upper()
        if home_status in list(search_type_mapping.values()):
            address = item.get("address", {}) or {}
            street = address.get("streetAddress", "") or ""
            borough = address.get("city", "") or ""
            state = address.get("state", "") or ""
            zip_code = address.get("zipcode") or ""
            if borough.upper() == "MANHATTAN":
                combined_address = f"{street}, NEW YORK, {state}, {zip_code}"
            else:
                combined_address = f"{street}, {borough}, {state}, {zip_code}"

            print("Scraped Combined Address (raw): ", combined_address)
            canonical = canonicalize_combined_address(combined_address)
            print("Scraped Combined Address (canonical): ", canonical)
            if canonical in file_addresses:
                print("---------------------- Found ----------------------")
                email_data.append({
                    "Address": canonical,
                    "Type": item.get("homeStatus"),
                    "URL": item.get("url"),
                    "Date Listed": item.get("datePostedString"),
                })
                filtered.append(item)

    return email_data
