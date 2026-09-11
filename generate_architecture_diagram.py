import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_rounded_card(ax, x, y, w, h, title, subtitle, items, bg_color, border_color, title_color, badge=None):
    # Background card
    card = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.03",
        facecolor=bg_color,
        edgecolor=border_color,
        linewidth=2,
        zorder=2
    )
    ax.add_patch(card)
    
    # Title
    ax.text(x + 0.02, y + h - 0.035, title, fontsize=12, fontweight='bold', color=title_color, zorder=3, va='top')
    
    # Subtitle / description
    if subtitle:
        ax.text(x + 0.02, y + h - 0.075, subtitle, fontsize=9, color='#475569', zorder=3, va='top', style='italic')
        curr_y = y + h - 0.115
    else:
        curr_y = y + h - 0.075
        
    # Badge (if any)
    if badge:
        b_box = patches.FancyBboxPatch(
            (x + w - 0.22, y + h - 0.045), 0.20, 0.032,
            boxstyle="round,pad=0.005,rounding_size=0.01",
            facecolor='#FFFFFF', edgecolor=border_color, linewidth=1, zorder=3
        )
        ax.add_patch(b_box)
        ax.text(x + w - 0.12, y + h - 0.030, badge, fontsize=7.5, fontweight='bold', color=title_color, ha='center', va='center', zorder=4)

    # Bullet items
    for item in items:
        # Mini bullet rectangle or pill
        pill = patches.FancyBboxPatch(
            (x + 0.02, curr_y - 0.042), w - 0.04, 0.045,
            boxstyle="round,pad=0.005,rounding_size=0.012",
            facecolor='#FFFFFF', edgecolor='#E2E8F0', linewidth=1, zorder=3
        )
        ax.add_patch(pill)
        ax.text(x + 0.035, curr_y - 0.020, item, fontsize=8.5, color='#1E293B', zorder=4, va='center')
        curr_y -= 0.055

def create_diagram(output_path):
    fig, ax = plt.subplots(figsize=(16, 9.5), dpi=300)
    ax.set_facecolor('#F8FAFC')
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Header Banner
    header_bg = patches.FancyBboxPatch(
        (0.02, 0.90), 0.96, 0.08,
        boxstyle="round,pad=0.01,rounding_size=0.02",
        facecolor='#0F172A', edgecolor='#1E293B', linewidth=1.5, zorder=2
    )
    ax.add_patch(header_bg)
    ax.text(0.04, 0.952, "FITNESS BUDDY — MULTI-AGENT SYSTEM ARCHITECTURE", fontsize=16, fontweight='bold', color='#FFFFFF', zorder=3)
    ax.text(0.04, 0.922, "AICTE-2026 Problem Statement No. 13 | Agentic AI Personal Fitness Coach | Powered by IBM Granite & IBM Bob", fontsize=10, color='#94A3B8', zorder=3)
    
    # IBM & Tech Badges on Header
    badges = [("IBM Granite 4", "#10B981"), ("IBM watsonx.ai", "#3B82F6"), ("IBM Db2 Lite", "#8B5CF6"), ("React + FastAPI", "#06B6D4")]
    bx = 0.96
    for b_text, b_col in reversed(badges):
        bx -= 0.115
        p = patches.FancyBboxPatch((bx, 0.925), 0.105, 0.032, boxstyle="round,pad=0.005,rounding_size=0.01", facecolor='#1E293B', edgecolor=b_col, linewidth=1.5, zorder=3)
        ax.add_patch(p)
        ax.text(bx + 0.0525, 0.941, b_text, fontsize=8, fontweight='bold', color='#F8FAFC', ha='center', va='center', zorder=4)

    # 1. PRESENTATION LAYER
    draw_rounded_card(
        ax, x=0.02, y=0.48, w=0.22, h=0.39,
        title="1. Presentation Layer",
        subtitle="React 18 + Vite + Tailwind CSS",
        items=[
            "• Minimalist White/Green UI",
            "• User Onboarding & Goal Hub",
            "• Interactive Streak Tracker (7-day)",
            "• Modular WorkoutCard (Checkboxes)",
            "• MealCard (Calories & Macros)",
            "• MotivationCard (Daily Habits)"
        ],
        bg_color="#F0F9FF", border_color="#0284C7", title_color="#0369A1", badge="Frontend"
    )

    # 2. FASTAPI BACKEND GATEWAY
    draw_rounded_card(
        ax, x=0.27, y=0.48, w=0.20, h=0.39,
        title="2. API Gateway Layer",
        subtitle="Python 3.11 + FastAPI",
        items=[
            "• POST /api/chat (Session Chat)",
            "• GET/POST /api/profile (Onboarding)",
            "• GET /api/dashboard (Streak & Tips)",
            "• GET /health (Liveness Probe)",
            "• CORS Middleware & Security",
            "• Pydantic Strict Validation"
        ],
        bg_color="#ECFDF5", border_color="#059669", title_color="#047857", badge="REST API"
    )

    # 3. ORCHESTRATOR & MEMORY
    draw_rounded_card(
        ax, x=0.50, y=0.52, w=0.21, h=0.35,
        title="3. Multi-Agent Core",
        subtitle="Intent-Based Router Pattern",
        items=[
            "• OrchestratorAgent (Intent Classifier)",
            "  -> Classifies: WORKOUT | NUTRITION",
            "  -> MOTIVATION | PROFILE | GENERAL",
            "• MemoryAgent (Context Coordinator)",
            "• Turn History & State Tracker",
            "• Zero Prompt Contamination"
        ],
        bg_color="#FFFBEB", border_color="#D97706", title_color="#B45309", badge="Agentic AI"
    )

    # 4. SPECIALIZED DOMAIN AGENTS
    draw_rounded_card(
        ax, x=0.74, y=0.48, w=0.24, h=0.39,
        title="4. Specialized Agents",
        subtitle="Task-Dedicated Domain Specialists",
        items=[
            "• WorkoutAgent (Temp=0.2)",
            "  Zero-equipment home workout splits",
            "• NutritionAgent (Temp=0.2)",
            "  High-protein Indian/Global meal plans",
            "• MotivationAgent (Temp=0.7)",
            "  Empathetic habit-building challenges",
            "• ProfileAgent (Preferences & Goals)"
        ],
        bg_color="#FAF5FF", border_color="#7C3AED", title_color="#6D28D9", badge="Specialists"
    )

    # 5. FOUNDATION MODEL (IBM GRANITE)
    draw_rounded_card(
        ax, x=0.50, y=0.05, w=0.48, h=0.40,
        title="5. Foundation Model Layer (IBM watsonx.ai)",
        subtitle="IBM Granite & Resilient Inference Engine",
        items=[
            "• GraniteClient Wrapper: Centralized SDK interfacing us-south.ml.cloud.ibm.com",
            "• Model: ibm/granite-4-h-small (Dual-temperature structured inference: 0.2 / 0.7)",
            "• IAM Token Exchange: Secure OAuth token lifecycle management",
            "• Token Usage Metering: Session tracking to protect Cloud Lite quota (<50k tokens)",
            "• Resilient Fallback Engine: Built-in local generator for zero-downtime offline demo",
            "• Exponential Backoff & Retry on transient rate-limits (429/503)"
        ],
        bg_color="#FFF1F2", border_color="#E11D48", title_color="#BE123C", badge="IBM Cloud"
    )

    # 6. PERSISTENCE LAYER
    draw_rounded_card(
        ax, x=0.02, y=0.05, w=0.45, h=0.40,
        title="6. Data & Persistence Layer",
        subtitle="IBM Db2 on Cloud Lite & In-Memory Fallback",
        items=[
            "• Primary Database: IBM Db2 on Cloud Lite (ibm_db async client)",
            "• Table 1: users (user_id, name, age, fitness_goal, level, streak)",
            "• Table 2: chat_history (turn history, message role, type, structured JSON)",
            "• Table 3: daily_logs (date, completed_habits, workout_done, calories)",
            "• In-Memory Fast Cache: High-performance dictionary store for local dev",
            "• Strict Schema: Validated DDL migrations via backend/db/schema.sql"
        ],
        bg_color="#F1F5F9", border_color="#475569", title_color="#334155", badge="Storage"
    )

    # CONNECTING ARROWS
    arrow_style = dict(arrowstyle="->", lw=2.2, mutation_scale=15)
    
    # 1. UI -> FastAPI
    ax.annotate("", xy=(0.27, 0.67), xytext=(0.24, 0.67),
                arrowprops=dict(**arrow_style, color="#0284C7"))
    ax.text(0.255, 0.69, "HTTP/JSON", fontsize=7.5, fontweight='bold', color='#0284C7', ha='center')

    # 2. FastAPI -> Orchestrator
    ax.annotate("", xy=(0.50, 0.67), xytext=(0.47, 0.67),
                arrowprops=dict(**arrow_style, color="#059669"))
    ax.text(0.485, 0.69, "Dispatch", fontsize=7.5, fontweight='bold', color='#059669', ha='center')

    # 3. Orchestrator -> Specialized Agents
    ax.annotate("", xy=(0.74, 0.67), xytext=(0.71, 0.67),
                arrowprops=dict(**arrow_style, color="#D97706"))
    ax.text(0.725, 0.69, "Intent Route", fontsize=7.5, fontweight='bold', color='#D97706', ha='center')

    # 4. Specialized Agents -> IBM Granite
    ax.annotate("", xy=(0.74, 0.45), xytext=(0.80, 0.48),
                arrowprops=dict(**arrow_style, color="#7C3AED", connectionstyle="arc3,rad=-0.2"))
    ax.text(0.81, 0.46, "Prompt (temp=0.2/0.7)", fontsize=7.5, fontweight='bold', color='#7C3AED', ha='left')

    # 5. FastAPI / Memory -> Storage
    ax.annotate("", xy=(0.25, 0.45), xytext=(0.35, 0.48),
                arrowprops=dict(**arrow_style, color="#475569", connectionstyle="arc3,rad=0.2"))
    ax.text(0.33, 0.46, "Async Db2 / In-Memory", fontsize=7.5, fontweight='bold', color='#475569', ha='center')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Architecture diagram successfully saved to: {output_path}")

if __name__ == "__main__":
    create_diagram("docs/architecture_diagram.png")
    create_diagram("docs/screenshots/architecture_diagram.png")
    create_diagram("architecture_diagram.png")
