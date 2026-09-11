import os
import shutil
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

PPT_PATH = r"D:\DOWNLOAD\AICTE_IBM_BOB_Project_Submission_Template_for_EduentFoundation_.pptx"
ONBOARDING_IMG = r"C:\Users\shail\.gemini\antigravity-ide\brain\bc6ab32f-af46-4f62-8f31-30a654ca4f1c\onboarding_page_1789123435612.png"
FINAL_APP_IMG = r"C:\Users\shail\.gemini\antigravity-ide\brain\bc6ab32f-af46-4f62-8f31-30a654ca4f1c\final_app_state_1789124650659.png"
GREETING_IMG = r"C:\Users\shail\.gemini\antigravity-ide\brain\bc6ab32f-af46-4f62-8f31-30a654ca4f1c\chat_greeting_response_1789116771628.png"
SKILLS_PROFILE_IMG = r"D:\DOWNLOAD\AICTE_profile.png"

prs = Presentation(PPT_PATH)
print(f"Loaded presentation with {len(prs.slides)} slides.")

# Slide 1: Title
slide1 = prs.slides[0]
for shape in slide1.shapes:
    if shape.has_text_frame:
        text = shape.text_frame.text
        if "Exploring the Power of Agentic AI" in text or "“" in text:
            for p in shape.text_frame.paragraphs:
                p.text = "Fitness Buddy — AI-Powered Personal Fitness Coach\nPowered by IBM Granite and IBM Bob"

# Slide 2: Domain & Title
slide2 = prs.slides[1]
for shape in slide2.shapes:
    if shape.has_text_frame:
        text = shape.text_frame.text
        if "Domain of  Project" in text or "Domain of Project" in text:
            for p in shape.text_frame.paragraphs:
                p.text = "Domain of Project: Healthcare / Fitness & Wellness"
        elif "Project Tile" in text or "Project Title" in text:
            for p in shape.text_frame.paragraphs:
                p.text = "Project Title: Fitness Buddy — AI-Powered Personal Fitness Coach"
        elif "Recommended font style" in text:
            shape.text_frame.clear()
            p = shape.text_frame.paragraphs[0]
            p.text = "AICTE-2026 Problem Statement No. 13\nTeam: Ronak-webdev\nTech: IBM Granite (ibm/granite-4-h-small), Python FastAPI, React 18, IBM Db2 on Cloud Lite"

# Slide 3: Problem Statement
slide3 = prs.slides[2]
for shape in slide3.shapes:
    if shape.has_text_frame:
        text = shape.text_frame.text
        if "Problem Statement : Nutrition Agent" in text:
            shape.text_frame.clear()
            p = shape.text_frame.paragraphs[0]
            p.text = "Problem Statement No. 13 : Fitness Buddy\n"
            p.font.bold = True
            
            p2 = shape.text_frame.add_paragraph()
            p2.text = "The Challenge:\nIn today's fast-paced world, individuals struggle to maintain a healthy lifestyle due to lack of personalized guidance, time constraints, and inconsistent motivation. Traditional fitness solutions require expensive subscriptions, in-person trainers, or rigid schedules that fail to adapt to personal routines. Without accessible, real-time guidance, people struggle with home workout planning, healthy eating, and building daily consistency.\n"
            
            p3 = shape.text_frame.add_paragraph()
            p3.text = "The Objective:\nBuild an Agentic AI personal fitness coach that delivers on-demand guidance, healthy lifestyle suggestions, and basic nutrition advice tailored to individual needs:\n• Personalized Home Workouts – Tailored routines based on fitness level, available time, and no-equipment constraints.\n• Nutritious Meal Ideas – Wholesome Indian & international meal ideas with approximate calories, macros, and practical cooking tips.\n• Habit-Building & Daily Motivation – Consistency tracking, streak gamification, and daily encouragement.\n• Agentic Multi-Agent System – Orchestrator, WorkoutAgent, NutritionAgent, MotivationAgent, and ProfileAgent.\n• Interactive Web App – Clean, responsive UI with streak tracking, quick action prompts, and modular card rendering."

# Slide 4: Proposed Solution
slide4 = prs.slides[3]
for s_idx, shape in enumerate(slide4.shapes):
    if shape.has_text_frame:
        text = shape.text_frame.text
        if s_idx == 0 or "Proposed Solution:" in text:
            for p in shape.text_frame.paragraphs:
                p.text = "Proposed Solution: Fitness Buddy Multi-Agent Coach"
        elif s_idx == 1 or "Proposed Solution -" in text:
            shape.text_frame.clear()
            p = shape.text_frame.paragraphs[0]
            p.text = "Proposed Solution – Key Pillars:\n\n1. Agentic AI Personal Coach: Uses an intelligent OrchestratorAgent to classify user intent and route queries to specialized agents (Workout, Nutrition, Motivation, Profile).\n\n2. Low-Temperature Structured AI Generation: IBM Granite produces precise, validated JSON routines for workouts and meals (temperature=0.2), while motivational guidance uses conversational warmth (temperature=0.7).\n\n3. Daily Habit & Consistency Engine: Integrates a streak counter and daily habit challenges to reinforce fitness consistency.\n\n4. Resilient Cloud Architecture: Optimized for IBM Cloud Lite with token budget tracking and automatic in-memory fallback for local development."

# Slide 5: Technology Used
slide5 = prs.slides[4]
for shape in slide5.shapes:
    if shape.has_text_frame:
        text = shape.text_frame.text
        if "IBM Bob platform" in text or "IBM Grainte model" in text:
            shape.text_frame.clear()
            p = shape.text_frame.paragraphs[0]
            p.text = "• IBM Bob platform - For designing, orchestrating, and scaffolding multi-agent workflows\n\n• IBM Granite model - ibm/granite-4-h-small via IBM watsonx.ai for natural language reasoning, structured JSON generation, and conversational coaching\n\n• IBM Cloud Lite & Db2 - Infrastructure for user profile persistence, chat history, and session management\n\n• Python 3.11 & FastAPI & Pydantic - High-performance backend with asynchronous request handling and strict data validation\n\n• React 18, Vite & Tailwind CSS - Responsive, minimalist white-and-green theme with modular card rendering"

# Slide 14: Role of Agentic AI
slide14 = prs.slides[13]
for shape in slide14.shapes:
    if shape.has_text_frame:
        text = shape.text_frame.text
        if "Role of Agentic AI in Nutrition Agent" in text:
            shape.text_frame.clear()
            p = shape.text_frame.paragraphs[0]
            p.text = "Role of Agentic AI in Fitness Buddy\n\n"
            p.font.bold = True
            p2 = shape.text_frame.add_paragraph()
            p2.text = "Agentic AI enables Fitness Buddy to operate as an intelligent, autonomous coaching system rather than a generic chatbot. Using IBM watsonx.ai and IBM Granite models, it coordinates multiple specialized agents:\n\n• Orchestrator Agent: Classifies intent (WORKOUT, NUTRITION, MOTIVATION, PROFILE, GENERAL) and routes requests to the right specialist agent.\n• Workout Agent: Generates structured home workout routines with warm-up, main exercises, cool-down, sets, and rest intervals.\n• Nutrition Agent: Delivers high-protein meal suggestions with calories, macros, and practical preparation tips.\n• Motivation Agent: Provides daily habit-building challenges and positive reinforcement based on the user's streak.\n• Profile & Memory Agent: Manages user preferences, fitness goals, experience level, and conversation history.\n\nThis multi-agent architecture guarantees zero prompt contamination, high reliability, and domain-specialized responses."

# Helper to add image to slide replacing or covering placeholder
def replace_or_add_picture(slide, img_path, left_in=1.0, top_in=1.5, width_in=11.0, height_in=5.5):
    if not os.path.exists(img_path):
        print(f"Image not found: {img_path}")
        return
    # Remove existing picture if present
    for shape in list(slide.shapes):
        if shape.shape_type == pptx.enum.shapes.MSO_SHAPE_TYPE.PICTURE and "Picture" in shape.name:
            sp = shape._element
            sp.getparent().remove(sp)
    slide.shapes.add_picture(img_path, Inches(left_in), Inches(top_in), Inches(width_in), Inches(height_in))
    print(f"Added picture {img_path} to slide")

# Slide 15: Output Screenshot 1 (Onboarding & User Setup)
slide15 = prs.slides[14]
for shape in slide15.shapes:
    if shape.has_text_frame:
        text = shape.text_frame.text
        if "Project Output Screenshot" in text:
            for p in shape.text_frame.paragraphs:
                p.text = "Project Output Screenshot: User Onboarding & Profile Setup"
        elif "Please put IBM Bob" in text or "·" in text:
            shape.text_frame.clear()
replace_or_add_picture(slide15, ONBOARDING_IMG, left_in=1.2, top_in=1.3, width_in=10.8, height_in=5.6)

# Slide 16: Output Screenshot 2 (Core Prompts & Multi-Agent Responses)
slide16 = prs.slides[15]
for shape in slide16.shapes:
    if shape.has_text_frame:
        text = shape.text_frame.text
        if "Project Output Screenshot" in text:
            for p in shape.text_frame.paragraphs:
                p.text = "Project Output Screenshot: Home Workout & Nutrition Recommendations"
        elif "Please put IBM Bob" in text or "·" in text:
            shape.text_frame.clear()
replace_or_add_picture(slide16, FINAL_APP_IMG, left_in=1.0, top_in=1.3, width_in=11.2, height_in=5.7)

# Slide 17: Output Screenshot 3 (Live Chat & Streak Tracking)
slide17 = prs.slides[16]
for shape in slide17.shapes:
    if shape.has_text_frame:
        text = shape.text_frame.text
        if "Project Output Screenshot" in text:
            for p in shape.text_frame.paragraphs:
                p.text = "Project Output Screenshot: Interactive Dashboard & Motivation Flow"
        elif "Please put IBM Bob" in text or "·" in text:
            shape.text_frame.clear()
replace_or_add_picture(slide17, GREETING_IMG, left_in=1.2, top_in=1.3, width_in=10.8, height_in=5.6)

# Slide 18: The Wow Factor
slide18 = prs.slides[17]
for shape in slide18.shapes:
    if shape.has_text_frame:
        text = shape.text_frame.text
        if "The Wow Factor" in text:
            shape.text_frame.clear()
            p = shape.text_frame.paragraphs[0]
            p.text = "The Wow Factor Behind Fitness Buddy\n"
            p.font.bold = True
            p2 = shape.text_frame.add_paragraph()
            p2.text = "1. Multi-Agent Intelligent Routing:\nInstead of a monolithic prompt, an Orchestrator classifies user intent and delegates to domain-specialized agents. Workout plans, diet suggestions, and mindset advice never interfere with one another.\n\n2. Dual-Temperature Precision Architecture:\nStructured JSON generation for workouts and meals is executed at temperature 0.2 for strict schema adherence, while motivational coaching runs at temperature 0.7 for warm, empathetic human-like tone.\n\n3. Habit-Building & Streak Gamification:\nBuilt-in consistency tracking with dynamic streak badges and daily habit challenges reinforces real-world adherence and long-term wellness.\n\n4. Cloud-Lite & Offline Resiliency:\nEngineered for zero-downtime demonstration: seamlessly operates on IBM Cloud Lite or in-memory fallback if credentials/quotas fluctuate."

# Slide 19: Novelty and Uniqueness
slide19 = prs.slides[18]
for shape in slide19.shapes:
    if shape.has_text_frame:
        text = shape.text_frame.text
        if "The proposed Nutrition Agent" in text:
            shape.text_frame.clear()
            p = shape.text_frame.paragraphs[0]
            p.text = "Fitness Buddy stands out by combining Agentic AI, structured LLM reasoning, and habit science:\n\n• Multi-Agent Coordination: Specialized agents for workouts, meals, motivation, and user memory.\n• Zero-Equipment Accessibility: Home workout generation requiring no gym membership or equipment.\n• Culturally-Aware Nutrition: Realistic meal recommendations with practical Indian and global options.\n• Behavior-Driven Motivation: Micro-challenges to overcome workout resistance and build sustainable routines.\n• Privacy & Lightweight Architecture: Client-side session management with secure backend APIs.\n• Enterprise Foundation: Built on IBM Granite and watsonx.ai enterprise AI infrastructure."

# Slide 20: Future Scope
slide20 = prs.slides[19]
for shape in slide20.shapes:
    if shape.has_text_frame:
        text = shape.text_frame.text
        if "1.Integration with Wearables" in text or "Future Scope" in text:
            shape.text_frame.clear()
            p = shape.text_frame.paragraphs[0]
            p.text = "Future Scope & Roadmap\n\n"
            p.font.bold = True
            p2 = shape.text_frame.add_paragraph()
            p2.text = "1. Wearable & Smart Device Integration:\nSyncing with smartwatches (Apple Watch, WearOS, Fitbit) to ingest real-time biometric metrics (steps, heart rate, active calories, sleep) for dynamic plan adjustments.\n\n2. Computer Vision Form Analysis:\nUsing camera feeds to provide real-time pose estimation and posture correction during home exercises (squats, pushups, planks).\n\n3. Voice Assistant & Multilingual Support:\nEnabling hands-free voice coaching in English, Hindi, Gujarati, and other regional languages during workouts.\n\n4. Community Fitness Challenges:\nSocial streak sharing and peer group challenges to enhance accountability and engagement."

# Slide 21: GitHub Link
slide21 = prs.slides[20]
for shape in slide21.shapes:
    if shape.has_text_frame:
        shape.text_frame.clear()
        p = shape.text_frame.paragraphs[0]
        p.text = "GitHub Repository Link\n\n"
        p.font.bold = True
        p2 = shape.text_frame.add_paragraph()
        p2.text = "Working Repository URL:\nhttps://github.com/Ronak-webdev/Fitness-Buddy.git\n\n"
        p2.font.size = Pt(22)
        p2.font.bold = True
        p3 = shape.text_frame.add_paragraph()
        p3.text = "Repository Contents:\n1. All Agent relevant files of IBM Cloud (.bob/ rules, backend/agents/, backend/llm/)\n2. Official AICTE Problem Statement PDF (Problem Statement No. 13)\n3. Official Project Presentation PPTX\n4. Complete FastAPI Backend & React Frontend Source Code\n5. Test Suite (17/17 passing) & Comprehensive Project Documentation"

# Slide 22: Skillsbuild profile screenshot
slide22 = prs.slides[21]
for shape in slide22.shapes:
    if shape.has_text_frame:
        text = shape.text_frame.text
        if "Skills build" in text:
            for p in shape.text_frame.paragraphs:
                p.text = "IBM SkillsBuild Profile Screenshot"
if os.path.exists(SKILLS_PROFILE_IMG):
    replace_or_add_picture(slide22, SKILLS_PROFILE_IMG, left_in=1.5, top_in=1.5, width_in=10.0, height_in=5.4)

prs.save(PPT_PATH)
print("Successfully populated and saved presentation to:", PPT_PATH)
