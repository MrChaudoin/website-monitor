from scraper import check_for_new_filings

new_data = check_for_new_filings()

if new_data:
    print(f"[✓] Found {len(new_data)} new filings")
else:
    print("[✓] No new filings found")