import csv

def export_predictions(output_path,records):
    if not records:
        return
    with open(output_path,"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=records[0].keys())
        w.writeheader()
        w.writerows(records)
