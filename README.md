
## Team-24: Alpaca 3: A Custom GPT for Liminal Works

## Demo Video
<p>
    <a href="https://youtu.be/UY_XMJl0DD4" target="_blank">
        <img src="https://img.youtube.com/vi/UY_XMJl0DD4/0.jpg" alt="Alpaca 3 Demo Video">
    </a>
</p>
<p>Click the image above or <a href="https://youtu.be/UY_XMJl0DD4" target="_blank">Video Link</a> to watch the video.</p>

[Devpost](https://devpost.com/software/opportunity-hack-2024) | [Our Slack](https://opportunity-hack.slack.com/app_redirect?channel=alpaca_3_laminal_works) | [About Liminal Works](https://www.liminal-works.org/about)</br>

## Team Members
#### Justin Lee | [Github](https://github.com/justinzl1) | [LinkedIn](https://www.linkedin.com/in/justinzl)
  
#### Dheeraj Kallakuri | [Github](https://github.com/dheerajkallakuri) | [LinkedIn](https://www.linkedin.com/in/dheerajkallakuri/)

#### Ramy Bagaghayou | [Github](https://github.com/mcaramy) | [LinkedIn](https://www.linkedin.com/in/rbabagha/)

#### Umang Rajnikant Bid | [Github](https://github.com/UmangBid) | [LinkedIn](https://www.linkedin.com/in/umang-bid/)

## Problem Statement

Liminal Works currently enlists the help of its volunteers to develop theories of change for grassroot activists and organizations. 
This task can be very time-consuming and subjective. Using AI to facilitate this process, the time spent developing theories
of change is significantly reduced, allowing for volunteers and employees to allocate their time to more important tasks.

## Introduction

Alpaca 3 is an AI model trained on data about theory of change (TOC), what makes a good TIC, and how to craft a TOC. Users are able to 
directly ask Alpaca 3 questions they have, or they can upload pdfs that the AI will scan and respond to. </br>

<img width="1438" alt="Screenshot 2024-10-13 at 2 25 35 PM" src="https://github.com/user-attachments/assets/711dc571-671e-41f2-acbf-c54ee710813e">

## How it works

The user writes text or uploads a pdf, and this input is then sent as a query to the API gpt that generates a response. 
The response is filtered through a database containing data about TOC. If the response relates to TOC, the AI response
will let it through. If not, the AI responds with how the query is not relevant to TOC. Every conversation is collected and stored in the database for future reference and training where it learns from past conversations.

<img width="3136" alt="Flow Map" src="https://github.com/user-attachments/assets/52570d3a-185b-4f86-861a-5573b8be203b">


## File Structure
```
.
├── backend
│   ├── good data folder
│   ├── bad data folder
│   ├── answers.pdf
│   ├── output.pdf
│   ├── standard.pdf
│   ├── vector_index.faiss
│   ├── metadata.pkl
│   ├── createpdf.py
│   ├── fetchData.py
│   ├── main.py
│   ├── maindb.py
│   ├── mongoData.py
│   └── pdfcontentreader.py
│
├── src
│   └── app.py
│── requirements.txt
└── README.md
```
## Folder Description
- **backend/**: Contains data files, scripts, and modules related to backend processing.
  - **good data folder**: Folder contains pdf which talks about good examples of theory of change.
  - **bad data folder**: Folder contains pdf which talks about bad examples of theory of change.
  - **answers.pdf**: A sample Q/A collected by Liminal Works Volunteer.
  - **output.pdf**: A pdf file which has Q/A and some feedback of each question of answers.pdf
  - **standard.pdf**: Contains 17 questions asked by Liminal Works Volunteer.
  - **vector_index.faiss**: File for storing FAISS vector index data.
  - **metadata.pkl**: Pickle file for storing metadata.
  - **createpdf.py**: Script for creating PDF files.
  - **fetchData.py**: Script for fetching data from sources.
  - **main.py**: Main entry point for backend operations.
  - **maindb.py**: Database management script.
  - **mongoData.py**: Script for handling MongoDB operations.
  - **pdfcontentreader.py**: Script for reading content from PDFs.

- **src/**: Contains the main application file.
  - **app.py**: Main application logic of frontend.

## Required API Keys

Ensure you have the following API keys set up for the project:

- **OpenAI API Key**: Needed for accessing OpenAI's services.
- **Gemini API Key**: Required for interacting with Gemini's API.
- **MongoDB API Key**: Necessary for database connectivity and operations with MongoDB.


## Installation and Setup

### Prerequisites
Ensure you have Python installed and set up on your machine. You will also need the following API keys:
- OpenAI API Key
- Google Gemini API Key
- MongoDB API Key

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd <project-directory>
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
 
### Run the Project

1. Start the Flask backend by executing:
   ```bash
   python backend/main.py
   ```
   This will handle inputs from the frontend, and the application will be accessible at [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

2. Launch the frontend interface using Streamlit:
   ```bash
   streamlit run src/app.py
   ```
   This will start the frontend where users can input data, accessible at [http://localhost:8501](http://localhost:8501).

## Features

### Current Features
- **GPT-3.5 Turbo**: Utilized for generating responses during chat interactions.
- **Google Gemini**: Used for summarizing large document chunks effectively.
- **PDF Generation**: A suggestion file (`output.pdf`) is generated and saved in the `backend` folder.
- **Session Management**: Previous chat histories will not be retained and will reset upon refreshing the page.
- **MongoDB Storage**: All queries and responses related to the theory of change are stored in MongoDB for further analysis.
- **RAG Implementation**: Hallucinations are minimized using Retrieval-Augmented Generation (RAG) techniques.
- **API Keys Required**:
  - **OpenAI API Key**: For accessing GPT-3.5 Turbo services.
  - **Gemini API Key**: For document summarization.
  - **MongoDB API Key**: For storing and managing chat data.
 
## Enhancements

### Frontend and Backend:
- Standardizing the PDF parsing process for better consistency and accuracy.
- Adding a **Download PDF** button for easy access to generated documents.
- Implementing a feature to display **previous chat history** even after refreshing the page.
- Hosting the application on **AWS** for scalability and better availability.
- Adding additional features and design elements in the chat interface to improve user experience.
- Expanding document support to accept other file types beyond PDFs.

### AI Assistant:
- Fine-tuning the assistant using models such as **ChatGPT**, **Gemini**, or **Llama**. Note that fine-tuning costs may vary based on the model chosen.
- Implementing a process for fine-tuning the models at regular intervals to maintain accuracy and relevance.

### Code Review
- Refining the codebase to improve efficiency, readability, and maintainability.


## Challenges we ran into

We had some difficulties determining what makes a good theory of change and how to develop one and how an AI would be able to determine this as well. 
The data provided to train the model was very limited, so we had to solve this problem by manually training our model with other resources. For data collection, we had to scrape the internet for resources containing the keyword "Theory of Change". Our front-end and back-end could have used more communication because system integration proved to be a challenge.



## Accomplishments we are proud of

System integration was an accomplishment we are proud of. It was difficult to get the front-end and back-end to work together seamlessly, but 
once we got it working, we were all relieved and happy. In addition, all the answers to the questions are accurate an precise which means the project satisfies the problem statement.

## What we learned

It was some of our first times working with AI/machine learning and databses, and for one of us, it was our first time coding. We learned a lot about
creating programs with these features. The system uses multiple technologies in order to fulfill the problem statement. These technologies include, but not limited to :
1. MongoDB NoSQL Database
2. Natural Language Processing (NLP) and Artificial Intelligence (AI) techniques like Retrieval Augmented Generation (RAG) model
3. Open source python frontend framework like Streamlit
4. Web Scraping technologies and libraries like BeautifulSoup
5. Collaboration between teammates and getting things done in a time crunch
