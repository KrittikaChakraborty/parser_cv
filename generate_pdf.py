
from fpdf import FPDF

def generate_pdf(data: dict, match_score: float, output_path: str = "output.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Resume Parsing Result", ln=True, align='C')
    pdf.ln(10)

    pdf.cell(200, 10, txt=f"Name: {data['name']}", ln=True)
    pdf.cell(200, 10, txt=f"Email: {data['email']}", ln=True)
    pdf.cell(200, 10, txt=f"Phone: {data['phone']}", ln=True)
    pdf.ln(5)

    pdf.cell(200, 10, txt="Skills:", ln=True)
    for skill in data["skills"]:
        pdf.cell(200, 10, txt=f" - {skill}", ln=True)

    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Match Score: {match_score}", ln=True)

    pdf.output(output_path)
    return output_path
