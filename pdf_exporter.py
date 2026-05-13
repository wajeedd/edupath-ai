from fpdf import FPDF


def export_plan_pdf(plan: list, student_name: str) -> bytes:

    pdf = FPDF()

    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", "B", 16)

    pdf.cell(
        0,
        10,
        f"EduPath AI - Study Plan for {student_name}",
        ln=True
    )

    pdf.ln(5)

    # Content
    for item in plan:

        pdf.set_font("Helvetica", "B", 12)

        pdf.cell(
            0,
            8,
            f"{item['date']} - {item['concept']} "
            f"(Score: {item['score']:.0f}%)",
            ln=True
        )

        pdf.set_font("Helvetica", "", 11)

        for res in item['resources']:

            if res['resource_type'] == 'youtube':

                pdf.multi_cell(
                    0,
                    7,
                    f"Watch: {res['title']}"
                )

            elif res['resource_type'] == 'ncert':

                pdf.multi_cell(
                    0,
                    7,
                    f"Read: {res['title']}"
                )

        pdf.ln(3)

    # Return PDF as bytes
    return bytes(pdf.output(dest='S'))