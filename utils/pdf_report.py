from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf_report(
    filename,
    dataset_name,
    rows,
    columns,
    operation_history,
    ai_summary,
    report=None,
):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("<b>KINTSUGI AI Data Report</b>", styles["Title"]))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph(f"<b>Dataset:</b> {dataset_name}", styles["BodyText"]))
    elements.append(Paragraph(f"<b>Rows:</b> {rows}", styles["BodyText"]))
    elements.append(Paragraph(f"<b>Columns:</b> {columns}", styles["BodyText"]))

    elements.append(Spacer(1, 20))

    if report is not None:

        elements.append(
            Paragraph("<b>Data Quality Report</b>", styles["Heading2"])
        )

        for key, value in report.items():
            elements.append(
                Paragraph(f"{key}: {value}", styles["BodyText"])
            )

    elements.append(Spacer(1, 20))

    elements.append(Paragraph("<b>Operations Performed</b>", styles["Heading2"]))

    for op in operation_history:
        elements.append(
            Paragraph(f"• {op}", styles["BodyText"])
        )

    elements.append(Spacer(1, 20))

    elements.append(Paragraph("<b>AI Summary</b>", styles["Heading2"]))
    elements.append(Paragraph(ai_summary, styles["BodyText"]))

    doc.build(elements)