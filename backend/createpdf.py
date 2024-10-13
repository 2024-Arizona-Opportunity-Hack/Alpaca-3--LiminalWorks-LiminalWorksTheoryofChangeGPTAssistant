from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

tocpdfprompt="Validate response based on theory of change rules; suggest clarification/question. in 30 words "

def wrap_text(text, max_width, canvas, font_name="Helvetica", font_size=12):
    """Wraps text into lines that fit within max_width."""
    print(text)
    lines = []
    words = text.split(' ')
    current_line = ""

    # Set font for the canvas
    canvas.setFont(font_name, font_size)
    
    for word in words:
        # Check if adding the next word would exceed the max width
        if canvas.stringWidth(current_line + word + ' ', font_name, font_size) <= max_width:
            current_line += word + ' '
        else:
            # If the current line is not empty, save it
            if current_line:
                lines.append(current_line.strip())
            current_line = word + ' '  # Start a new line with the current word
    
    # Add any remaining text as the last line
    if current_line:
        lines.append(current_line.strip())
    
    return lines


def create_pdf(contentarr, filename="output.pdf"):
    canva = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Set initial position
    x = 72  # 1 inch from left
    y = height - 72  # Start from top
    line_height = 20  # Space between lines

    for content in contentarr:
        for con in content:
            # Wrap and draw the question text
            if tocpdfprompt in con:
                con=con.replace(tocpdfprompt,"")
            
            if "answer:" in con:
                # Split the content at "answer:"
                parts = con.split("answer:", 1)
                question_text = parts[0].strip()  
                answer_text = "\n" + parts[1].strip()
                con=question_text+answer_text
            
            question_lines = wrap_text(con, width - 144, canva)  # 72px padding on both sides
            for line in question_lines:
                canva.drawString(x, y, line)
                y -= line_height  # Move down for the next line
                
            y -= line_height  # Extra space between question and response

            # Check if we need to create a new page
            if y < 72:  # If y position is too low, create a new page
                canva.showPage()
                y = height - 72  # Reset y to top of the new page

    canva.save()
