from langchain_community.llms import Ollama
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
import os

# Connect to local LLM
llm = Ollama(model="llama3")

print("🚀 Placement Preparation Agent")
print("----------------------------------")

# Take user input
name = input("Enter your name: ")
skills = input("Enter your skills (comma separated): ")
education = input("Enter your education: ")
experience = input("Enter your experience (optional): ")
company = input("Enter target company: ")

print("\nGenerating your personalized placement plan...\n")

def generate_plan():
   prompt = f"""
   You are an intelligent placement preparation assistant.

   Student Profile:
   Name: {name}
   Skills: {skills}
   Education: {education}
Experience: {experience}
   Target Company: {company}

   Generate a structured response with:

   1. Resume Improvement Suggestions
   2. Skills Gap Analysis
   3. Preparation Strategy for {company}
   4. 5 Technical Interview Questions
   5. 3 HR Interview Questions

   Keep it structured and professional.
   """

   response = llm.invoke(prompt)
   return response


def create_pdf(content):

   filename = "placement_plan.pdf"
   doc = SimpleDocTemplate(filename, pagesize=A4)

   styles = getSampleStyleSheet()
   elements = []

   for line in content.split("\n"):
       elements.append(Paragraph(line, styles["Normal"]))
       elements.append(Spacer(1, 10))

   doc.build(elements)

   return filename


# Run Agent
plan = generate_plan()

print(plan)

pdf_file = create_pdf(plan)

print("\n✅ Placement plan generated successfully!")
print(f"📄 File saved as: {pdf_file}")
print("\nYou just built a Local AI Agent 🎉")