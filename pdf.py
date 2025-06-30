from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
text = """
John Doe
 123 Main Street, San Francisco, CA 94105
 (555) 123-4567
 john.doe@example.com
 linkedin.com/in/johndoe

Professional Summary
Results-driven Software Engineer with 3+ years of experience in Python, Machine Learning, and Web Development.
 Passionate about building scalable applications and solving complex problems. Strong background in team leadership and Agile methodologies.

Technical Skills
Programming Languages: Python (Pandas, NumPy, Scikit-learn), Java, SQL, JavaScript

Machine Learning: Deep Learning (TensorFlow, Keras), Natural Language Processing (NLP), Computer Vision

Web Development: HTML5, CSS3, React, Node.js, Django

Databases: MySQL, MongoDB, PostgreSQL

DevOps & Tools: Docker, Git, AWS, CI/CD pipelines

Professional Experience
Software Engineer
Tech Solutions Inc., San Francisco | Jan 2021 - Present

Developed RESTful APIs using Python and Django, improving system efficiency by 30%

Implemented machine learning models for customer behavior prediction (AUC: 0.92)

Led a team of 4 engineers in an Agile environment, delivering projects 20% faster

Data Science Intern
DataWorks Corp., New York | Jun 2020 - Dec 2020

Built NLP pipelines for sentiment analysis using spaCy and NLTK

Created SQL queries to optimize data retrieval (reduced latency by 40%)

Education
B.Sc. in Computer Science
Stanford University | 2016 - 2020

Thesis: "Deep Learning for Image Recognition in Medical Diagnostics"

Projects
Stock Market Predictor (Python/ML): LSTM model with 85% accuracy

E-commerce Website (React/Node.js): Handled 10k+ monthly users

Certifications
AWS Certified Developer - Associate

Google Professional Data Engineer

Languages
English (Native)

French (Fluent)

Spanish (Intermediate)

Interests
Teamwork: Volunteer lead at local coding bootcamp

Communication: Public speaking at tech meetups

AI Ethics: Member of "Responsible AI" discussion group



"""
for line in text.split('\n'):
    pdf.cell(0, 10, txt=line, ln=True)
pdf.output("cv_test5.pdf")
