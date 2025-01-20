def add_custom_sl_no(columns, data):
    """
    Adds a custom SL No. column to the report.

    Args:
        columns (list): List of report column definitions.
        data (list): List of report data rows.

    Returns:
        tuple: Updated columns and data with SL No. column added.
    """
    # Define the SL No. column
    sl_no_column = {"fieldname": "sl_no", "label": "SL No", "fieldtype": "Int", "width": 80}
    
    # Add the SL No. column to the beginning of the columns list if not already added
    if not any(col["fieldname"] == "sl_no" for col in columns):
        columns.insert(0, sl_no_column)

    # Add SL No. to each row in the data
    for idx, row in enumerate(data, start=1):
        row["sl_no"] = idx

    return columns, data
