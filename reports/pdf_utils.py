from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_prediction_report(output_path,data):
    styles=getSampleStyleSheet()
    doc=SimpleDocTemplate(output_path)
    story=[Paragraph("Cancer Risk Prediction Report",styles["Heading1"])]
    for k,v in data.items():
        story.append(Paragraph(f"<b>{k}</b>: {v}",styles["BodyText"]))
    doc.build(story)
