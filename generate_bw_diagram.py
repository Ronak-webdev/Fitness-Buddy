import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_dark_sequence_diagram(output_path):
    # Dimensions: 18 x 7.5 inches, 200 dpi -> 3600 x 1500 px
    fig, ax = plt.subplots(figsize=(18, 7.5), dpi=200)
    
    # Background
    bg_color = "#121314"
    box_bg = "#1F2022"
    box_border = "#4F535A"
    text_color = "#FFFFFF"
    subtext_color = "#C8CCD2"
    line_color = "#5A5E66"
    arrow_color = "#DCE0E6"
    
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Participant Columns (x coordinates)
    # Box 1: User
    # Box 2: Agent (fitness_agent.py)
    # Box 3: Granite (watsonx.ai)
    # Box 4: Tool (fitness_tools.py)
    # Box 5: Agent
    # Box 6: Granite
    # Box 7: Tool
    cols = [
        {"x": 0.08, "w": 0.095, "title": "User"},
        {"x": 0.215, "w": 0.125, "title": "Agent (fitness_agent.py)"},
        {"x": 0.36, "w": 0.11, "title": "Granite (watsonx.ai)"},
        {"x": 0.495, "w": 0.115, "title": "Tool (fitness_tools.py)"},
        {"x": 0.63, "w": 0.09, "title": "Agent"},
        {"x": 0.81, "w": 0.09, "title": "Granite"},
        {"x": 0.935, "w": 0.08, "title": "Tool"}
    ]

    top_y = 0.88
    bot_y = 0.04
    box_h = 0.09

    # Draw Top & Bottom Participant Boxes and Lifelines
    for col in cols:
        cx = col["x"]
        w = col["w"]
        title = col["title"]
        
        # Top Box
        top_box = patches.FancyBboxPatch(
            (cx - w/2, top_y), w, box_h,
            boxstyle="round,pad=0.01,rounding_size=0.018",
            facecolor=box_bg, edgecolor=box_border, linewidth=1.5, zorder=3
        )
        ax.add_patch(top_box)
        ax.text(cx, top_y + box_h/2, title, color=text_color, fontsize=10.5,
                ha='center', va='center', fontweight='medium', zorder=4)

        # Bottom Box
        bot_box = patches.FancyBboxPatch(
            (cx - w/2, bot_y), w, box_h,
            boxstyle="round,pad=0.01,rounding_size=0.018",
            facecolor=box_bg, edgecolor=box_border, linewidth=1.5, zorder=3
        )
        ax.add_patch(bot_box)
        ax.text(cx, bot_y + box_h/2, title, color=text_color, fontsize=10.5,
                ha='center', va='center', fontweight='medium', zorder=4)

        # Lifeline (vertical dashed line)
        ax.plot([cx, cx], [bot_y + box_h, top_y], color=line_color,
                linestyle=(0, (4, 4)), linewidth=1.2, zorder=1)

    # 1. User -> Agent (Box 5) Initial Request
    y1 = 0.79
    ax.annotate(
        "", xy=(cols[4]["x"], y1), xytext=(cols[0]["x"], y1),
        arrowprops=dict(arrowstyle="-|>", color=arrow_color, lw=1.5, mutation_scale=12),
        zorder=2
    )
    ax.text(0.35, y1 + 0.025, '"Create a 30-min beginner home workout for no equipment"',
            color=subtext_color, fontsize=10, ha='center', va='bottom', zorder=5)

    # 2. ReAct Loop Box (around Agent, Granite, Tool: cols 4, 5, 6)
    loop_x = cols[4]["x"] - 0.06
    loop_w = cols[6]["x"] - loop_x + 0.05
    loop_y = 0.28
    loop_h = 0.48

    loop_rect = patches.FancyBboxPatch(
        (loop_x, loop_y), loop_w, loop_h,
        boxstyle="square,pad=0.0",
        facecolor="none", edgecolor=line_color, linestyle=":", linewidth=1.5, zorder=1
    )
    ax.add_patch(loop_rect)

    # Loop Tag tab
    tag_w = 0.045
    tag_h = 0.035
    tag_box = patches.FancyBboxPatch(
        (loop_x, loop_y + loop_h - tag_h), tag_w, tag_h,
        boxstyle="round,pad=0.003,rounding_size=0.008",
        facecolor="#18191B", edgecolor=line_color, linewidth=1.2, zorder=3
    )
    ax.add_patch(tag_box)
    ax.text(loop_x + tag_w/2, loop_y + loop_h - tag_h/2, "loop",
            color=subtext_color, fontsize=9.5, ha='center', va='center', zorder=4)
    ax.text(loop_x + tag_w + 0.12, loop_y + loop_h - tag_h/2, "[ReAct iterations]",
            color=subtext_color, fontsize=10, ha='center', va='center', zorder=4)

    # Interactions inside Loop
    # Message 2: Agent -> Granite (Prompt)
    y2 = 0.69
    ax.annotate(
        "", xy=(cols[5]["x"], y2), xytext=(cols[4]["x"], y2),
        arrowprops=dict(arrowstyle="-|>", color=arrow_color, lw=1.4, mutation_scale=12),
        zorder=2
    )
    ax.text((cols[4]["x"] + cols[5]["x"])/2, y2 + 0.02, "Prompt (System + Tools + History)",
            color=subtext_color, fontsize=9.5, ha='center', va='bottom', zorder=5)

    # Message 3: Granite -> Agent (Thought / Action)
    y3 = 0.61
    ax.annotate(
        "", xy=(cols[4]["x"], y3), xytext=(cols[5]["x"], y3),
        arrowprops=dict(arrowstyle="-|>", color=arrow_color, lw=1.4, mutation_scale=12, linestyle="--"),
        zorder=2
    )
    ax.text((cols[4]["x"] + cols[5]["x"])/2, y3 + 0.02, "Thought / Action / Action Input",
            color=subtext_color, fontsize=9.5, ha='center', va='bottom', zorder=5)

    # Message 4: Agent -> Tool (Call selected tool)
    y4 = 0.52
    ax.annotate(
        "", xy=(cols[6]["x"], y4), xytext=(cols[4]["x"], y4),
        arrowprops=dict(arrowstyle="-|>", color=arrow_color, lw=1.4, mutation_scale=12),
        zorder=2
    )
    ax.text((cols[4]["x"] + cols[6]["x"])/2, y4 + 0.02, "Call selected tool with args",
            color=subtext_color, fontsize=9.5, ha='center', va='bottom', zorder=5)

    # Message 5: Tool -> Agent (Observation)
    y5 = 0.44
    ax.annotate(
        "", xy=(cols[4]["x"], y5), xytext=(cols[6]["x"], y5),
        arrowprops=dict(arrowstyle="-|>", color=arrow_color, lw=1.4, mutation_scale=12, linestyle="--"),
        zorder=2
    )
    ax.text((cols[4]["x"] + cols[6]["x"])/2, y5 + 0.02, "Observation (result)",
            color=subtext_color, fontsize=9.5, ha='center', va='bottom', zorder=5)

    # Message 6: Agent -> Granite (Append Observation)
    y6 = 0.36
    ax.annotate(
        "", xy=(cols[5]["x"], y6), xytext=(cols[4]["x"], y6),
        arrowprops=dict(arrowstyle="-|>", color=arrow_color, lw=1.4, mutation_scale=12),
        zorder=2
    )
    ax.text((cols[4]["x"] + cols[5]["x"])/2, y6 + 0.02, "Append Observation, ask again",
            color=subtext_color, fontsize=9.5, ha='center', va='bottom', zorder=5)

    # Message 7: Granite -> Agent (Final Answer)
    y7 = 0.23
    ax.annotate(
        "", xy=(cols[4]["x"], y7), xytext=(cols[5]["x"], y7),
        arrowprops=dict(arrowstyle="-|>", color=arrow_color, lw=1.4, mutation_scale=12, linestyle="--"),
        zorder=2
    )
    ax.text((cols[4]["x"] + cols[5]["x"])/2, y7 + 0.02, "Final Answer",
            color=subtext_color, fontsize=9.5, ha='center', va='bottom', zorder=5)

    # Message 8: Agent -> User (Formatted markdown answer)
    y8 = 0.16
    ax.annotate(
        "", xy=(cols[0]["x"], y8), xytext=(cols[4]["x"], y8),
        arrowprops=dict(arrowstyle="-|>", color=arrow_color, lw=1.5, mutation_scale=12, linestyle="--"),
        zorder=2
    )
    ax.text(0.35, y8 + 0.022, "Formatted markdown answer",
            color=subtext_color, fontsize=10, ha='center', va='bottom', zorder=5)

    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor=bg_color, edgecolor='none')
    plt.close()
    print(f"Saved black and white sequence diagram to: {output_path}")

if __name__ == "__main__":
    generate_dark_sequence_diagram("architecture_diagram_bw.png")
    generate_dark_sequence_diagram("docs/architecture_diagram_bw.png")
    generate_dark_sequence_diagram("docs/screenshots/architecture_diagram_bw.png")
