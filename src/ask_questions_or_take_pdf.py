import pdfplumber
import re  # Import the re module for regex

# Define the questions and headers
questions = {
    "AUTHOR’S PURPOSE": [
        "What cause or causes do you attribute your activism or organizing to?",
        "Who are your inspirations, role models, or forebearers that inspire or inform your activism/organizing?",
    ],
    "ASSUMPTIONS: PROGRAM PURPOSE": [
        "What is the mission of this work?",
        "What is the problem you want to address?",
        "What do you see as the underlying causes of the issue or problem?",
        "At what depth of the underlying problem do you intend to work?",
    ],
    "ASSUMPTIONS: IMPACT AND TEMPORALITY": [
        "What immediate (<1 week) impact do you want to achieve through your program or plan of action? What does that immediate solution look like?",
        "What medium-term (weeks a few months) impact do you want to achieve through your program or plan of action? What does that solution look like?",
        "What long-term (a few months to years) impact do you want to achieve through your program or plan of action? What does that solution look like?",
    ],
    "TARGET GROUPS AND VEHICLES": [
        "Who or what are you trying to impact?",
        "How do you reach/influence/impact your focus groups/structures?",
    ],
    "STRATEGIES": [
        "What tools do you use to impact these groups/structures?",
        "What resources do you need to employ these tools to influence the target groups?",
        "Which resources do you already have? What skills, knowledge, or other resources do you need to develop?",
        "Who else is doing similar work that you know of? Are you already collaborating or partnering? Is the space competitive?",
    ],
    "OUTCOMES AWARENESS": [
        "How will you know when you have succeeded? What would you count as a win, short, medium, and long-term?",
    ],
    "INTANGIBLE INPUT": [
        "What is a reason why somebody working along the same lines as you, in a similar environment may fail simply because they aren’t YOU? What is your superpower, special sauce?",
    ],
}

def process_pdf(pdf_path):
    """Function to process the PDF and extract questions and answers."""
    qa_dict = {}

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                # Split text into lines for easier processing
                lines = text.splitlines()
                current_question = None
                current_answer = []

                for line in lines:
                    line = line.strip()  # Clean up whitespace

                    # Check for any of the questions using regex
                    matched_question = None
                    for question in [q for qs in questions.values() for q in qs]:
                        # Match with question numbers (1., 2., etc.)
                        question_pattern = r"^\d*\.\s*" + question
                        if re.match(question_pattern, line, re.IGNORECASE):
                            matched_question = question
                            break

                    if matched_question:
                        if current_question:  # If there's an ongoing question, save the answer
                            qa_dict[current_question] = ' '.join(current_answer).strip()
                        current_question = matched_question  # Update the current question
                        current_answer = []  # Reset current answer
                    elif current_question:  # If we're in a question context, keep adding lines to the answer
                        if line:  # Only add non-empty lines
                            current_answer.append(line)

                # Add the last question and answer after finishing the loop
                if current_question:
                    qa_dict[current_question] = ' '.join(current_answer).strip()

    return qa_dict

def manual_input():
    """Function to allow the user to answer questions manually."""
    qa_dict = {}

    for category, qs in questions.items():
        for question in qs:
            answer = input(f"{question} ")
            qa_dict[question] = answer

    return qa_dict

def main():
    """Main function to either process a PDF or get manual input."""
    choice = input("Would you like to answer the questions manually or upload a PDF? (manual/pdf): ").strip().lower()
    
    if choice == "pdf":
        pdf_path = input("Please provide the path to the PDF file: ")
        qa_dict = process_pdf(pdf_path)
    elif choice == "manual":
        qa_dict = manual_input()
    else:
        print("Invalid choice. Please enter 'manual' or 'pdf'.")
        return

    # The qa_dict now contains the stored answers, and you can use it for further processing.
    print("\nResponses have been stored successfully.")

if __name__ == "__main__":
    main()
