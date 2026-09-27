from langchain_ollama import ChatOllama
from langchain_community.tools.tavily_search import TavilySearchResults  # Still works
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

# Setup (handles deprecation gracefully)
search = TavilySearchResults(max_results=3)
llm = ChatOllama(model="llama3", temperature=0.1)

def generate_plan(name, role, skills, education, experience, company):
    search_queries = [
        f"{company} {role} interview questions 2026",
        f"{company} {role} tech stack skills", 
        f"{company} {role} interview process"
    ]
    
    search_results = ""
    print("🔍 Web searches:")
    
    for query in search_queries:
        try:
            results = search.invoke({"query": query})
            print(f"   ✅ '{query}' → {len(results)} results")
            
            # FIXED: Handle result format correctly
            if isinstance(results, list):
                contents = [str(r)[:200] for r in results]  # ✅ Safe extraction
            else:
                contents = [str(results)[:200]]
            
            search_results += f"\n🔍 {query}:\n" + "\n".join(contents) + "\n\n"
        except Exception as e:
            print(f"   ❌ {query}: {e}")
            search_results += f"No results for: {query}\n\n"
    
    # LLM prompt
    prompt = f"""
You are an expert placement consultant. Use this web research:

{search_results}

Profile: {name}, {role}, Skills: {skills}, {education}, {experience}, {company}

Generate plan:

## 1. Company Overview
## 2. Resume Optimization
## 3. Skills Gap Analysis  
## 4. Interview Strategy
## 5. 5 Technical Questions
## 6. 3 HR Questions
## 7. Next Steps

Markdown format.
"""
    
    response = llm.invoke(prompt)
    return response.content

def create_pdf(content, name, role, company, skills):
    filename = f"{name.replace(' ', '_')}_{role}_{company}_plan.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4)
    
    styles = getSampleStyleSheet()
    elements = []
    
    title = Paragraph(f"<b>🚀 {name}'s Placement Plan</b><br/>"
                     f"<i>{role} at {company} | {skills}</i>", styles["Title"])
    elements.append(title)
    elements.append(Spacer(1, 20))
    
    for line in content.split("\n"):
        if line.strip():
            if line.startswith(("##", "###")):
                pstyle = styles["Heading2"]
            elif line.startswith("#"):
                pstyle = styles["Heading1"]
            else:
                pstyle = styles["Normal"]
            elements.append(Paragraph(line.strip(), pstyle))
        elements.append(Spacer(1, 8))
    
    doc.build(elements)
    return filename

# Clean main flow
inputs = [
    "Enter your name: ",
    "Enter your target role: ",
    "Enter your skills (comma separated): ", 
    "Enter your education: ",
    "Enter your experience (optional): ",
    "Enter target company: "
]

values = [input(prompt) for prompt in inputs]
name, role, skills, education, experience, company = values

print("Generating plan...")
plan_content = generate_plan(name, role, skills, education, experience, company)
pdf_filename = create_pdf(plan_content, name, role, company, skills)

print(f"✅ Saved: {pdf_filename}")