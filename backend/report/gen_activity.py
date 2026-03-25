import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(12, 9))
ax.set_xlim(0, 12)
ax.set_ylim(0, 9)
ax.axis('off')
ax.set_facecolor('white')
fig.patch.set_facecolor('white')

# Colors
C_ACTION   = '#2E86AB'   # user action
C_ASYNC    = '#F4A261'   # async/celery task
C_SYSTEM   = '#57CC99'   # system process
C_EXT      = '#9B59B6'   # chrome extension
C_DECISION = '#F6C90E'   # decision
C_HITL     = '#E76F51'   # human in the loop
C_START    = '#222222'
C_SWIM     = '#F0F4F8'

# Lane definitions
lanes = [
    (0.2,  3.0,  'User'),
    (3.2,  2.8,  'Backend\n(FastAPI + Celery)'),
    (6.2,  2.8,  'Groq API\n+ Apify'),
    (9.2,  2.5,  'Chrome\nExtension'),
]

# Draw swim lanes
lane_colors = ['#EBF5FB', '#EAFAF1', '#FDF9E3', '#F5EEF8']
for i, (x, w, name) in enumerate(lanes):
    rect = FancyBboxPatch((x, 0.3), w, 8.1,
                          boxstyle="square,pad=0",
                          facecolor=lane_colors[i], edgecolor='#BBBBBB',
                          linewidth=1.0, zorder=1)
    ax.add_patch(rect)
    ax.text(x + w/2, 8.25, name, ha='center', va='center',
            fontsize=8.5, fontweight='bold', color='#333333',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                      edgecolor='#BBBBBB', alpha=0.9))

def draw_action(ax, x, y, w, h, label, color, fontsize=7.8, text_color='white',
                sublabel=None):
    box = FancyBboxPatch((x, y), w, h,
                         boxstyle="round,pad=0.07,rounding_size=0.12",
                         facecolor=color, edgecolor='#333333', linewidth=1.2, zorder=3)
    ax.add_patch(box)
    if sublabel:
        ax.text(x + w/2, y + h/2 + 0.12, label,
                ha='center', va='center', fontsize=fontsize,
                fontweight='bold', color=text_color, zorder=4, multialignment='center')
        ax.text(x + w/2, y + h/2 - 0.14, sublabel,
                ha='center', va='center', fontsize=6.8,
                color=text_color, zorder=4, style='italic', multialignment='center')
    else:
        ax.text(x + w/2, y + h/2, label,
                ha='center', va='center', fontsize=fontsize,
                fontweight='bold', color=text_color, zorder=4, multialignment='center')

def draw_diamond(ax, cx, cy, w, h, label, color=C_DECISION):
    pts = [(cx, cy+h/2), (cx+w/2, cy), (cx, cy-h/2), (cx-w/2, cy)]
    poly = plt.Polygon(pts, facecolor=color, edgecolor='#333333', lw=1.2, zorder=3)
    ax.add_patch(poly)
    ax.text(cx, cy, label, ha='center', va='center', fontsize=7.2,
            fontweight='bold', color='#333333', zorder=4, multialignment='center')

def draw_circle(ax, cx, cy, r, color):
    c = plt.Circle((cx, cy), r, facecolor=color, edgecolor='white',
                   linewidth=2, zorder=4)
    ax.add_patch(c)

def arr(ax, x1, y1, x2, y2, label='', color='#444444', lw=1.3, loff=(0,0),
        rad=0.0):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=lw,
                                connectionstyle=f'arc3,rad={rad}'), zorder=5)
    if label:
        mx = (x1+x2)/2 + loff[0]
        my = (y1+y2)/2 + loff[1]
        ax.text(mx, my, label, ha='center', va='center', fontsize=6.8,
                color='#222222', zorder=6,
                bbox=dict(boxstyle='round,pad=0.1', facecolor='white',
                          edgecolor='#CCCCCC', alpha=0.85))

# Title
ax.text(6, 8.75, 'Activity Diagram — End-to-End User Workflow',
        ha='center', fontsize=13, fontweight='bold', color='#222222')

# --- START ---
draw_circle(ax, 1.7, 7.85, 0.22, '#222222')

# --- Step 1: Upload PDF Resume ---
draw_action(ax, 0.5, 7.25, 2.4, 0.55, 'Upload PDF Resume',
            C_ACTION, sublabel='POST /resumes/upload')
arr(ax, 1.7, 7.85, 1.7, 7.8)

# --- Step 2: parse_resume_task (async) ---
draw_action(ax, 3.5, 7.25, 2.5, 0.55, '[async] parse_resume_task',
            C_ASYNC, sublabel='Docling: PDF → Markdown\n~5 seconds')
arr(ax, 2.9, 7.52, 3.5, 7.52, 'task enqueued', color='#888888')

# --- Step 3: Poll until parsed ---
draw_diamond(ax, 1.7, 6.6, 1.4, 0.48, 'Parsed?')
arr(ax, 1.7, 7.25, 1.7, 6.84)
ax.text(2.45, 6.6, 'No → poll', fontsize=6.8, color='#888888')
ax.annotate('', xy=(1.7, 6.84), xytext=(2.5, 6.6),
            arrowprops=dict(arrowstyle='->', color='#888888', lw=1.0,
                            connectionstyle='arc3,rad=-0.4'), zorder=5)
ax.text(0.6, 6.5, 'Yes', fontsize=6.8, color='#555555')

# --- Step 4: Search Jobs ---
draw_action(ax, 0.5, 5.85, 2.4, 0.55, 'Search Jobs',
            C_ACTION, sublabel='POST /jobs/discover\n(title, location)')
arr(ax, 1.7, 6.36, 1.7, 6.4)

# Step 5: discover_jobs_task
draw_action(ax, 3.5, 5.85, 2.5, 0.55, '[async] discover_jobs_task',
            C_ASYNC, sublabel='Apify: LinkedIn scrape')
draw_action(ax, 6.5, 5.85, 2.5, 0.55, 'Apify Actor runs',
            C_SYSTEM, sublabel='curious_coder/\nlinkedin-jobs-scraper')
arr(ax, 2.9, 6.12, 3.5, 6.12, 'task enqueued', color='#888888')
arr(ax, 6.0, 6.12, 6.5, 6.12, 'HTTP trigger', color='#888888')

# Poll discover
draw_diamond(ax, 1.7, 5.2, 1.4, 0.48, 'Jobs\nfound?')
arr(ax, 1.7, 5.85, 1.7, 5.44)
ax.text(2.45, 5.2, 'No → poll', fontsize=6.8, color='#888888')
ax.annotate('', xy=(1.7, 5.44), xytext=(2.5, 5.2),
            arrowprops=dict(arrowstyle='->', color='#888888', lw=1.0,
                            connectionstyle='arc3,rad=-0.4'), zorder=5)
ax.text(0.6, 5.1, 'Yes', fontsize=6.8, color='#555555')

# Step 6: Score Jobs
draw_action(ax, 0.5, 4.45, 2.4, 0.55, 'Trigger Batch Scoring',
            C_ACTION, sublabel='POST /jobs/score/batch')
arr(ax, 1.7, 4.96, 1.7, 5.0)

# score_jobs_task
draw_action(ax, 3.5, 4.45, 2.5, 0.55, '[async] score_jobs_task',
            C_ASYNC, sublabel='Groq Llama 3.1-8b\ntruncated inputs')
draw_action(ax, 6.5, 4.45, 2.5, 0.55, 'Groq scoring\nLlama 3.1-8b-instant',
            C_SYSTEM, sublabel='score 1-10\n+ fit_reasoning')
arr(ax, 2.9, 4.72, 3.5, 4.72, 'task enqueued', color='#888888')
arr(ax, 6.0, 4.72, 6.5, 4.72, 'API call', color='#888888')

# Rate limit note
ax.text(4.2, 4.15, 'RateLimitError → smart retry\n(max_retries=10, parse_retry_after)',
        ha='center', fontsize=6.5, color='#E76F51',
        bbox=dict(boxstyle='round,pad=0.1', facecolor='#FFF3F0',
                  edgecolor='#E76F51', alpha=0.9))

# Poll scoring
draw_diamond(ax, 1.7, 3.75, 1.4, 0.48, 'Scored?')
arr(ax, 1.7, 4.45, 1.7, 3.99)
ax.text(2.45, 3.75, 'No → poll', fontsize=6.8, color='#888888')
ax.annotate('', xy=(1.7, 3.99), xytext=(2.5, 3.75),
            arrowprops=dict(arrowstyle='->', color='#888888', lw=1.0,
                            connectionstyle='arc3,rad=-0.4'), zorder=5)
ax.text(0.6, 3.65, 'Yes', fontsize=6.8, color='#555555')

# Step 7: View ranked jobs
draw_action(ax, 0.5, 3.0, 2.4, 0.55, 'View Ranked Job List',
            C_ACTION, sublabel='GET /jobs/ (sorted by score)')
arr(ax, 1.7, 3.51, 1.7, 3.55)

# Step 8: Select job
draw_action(ax, 0.5, 2.25, 2.4, 0.55, 'Select Job &\nOpen Application',
            C_ACTION, sublabel='Browser: navigate to URL')
arr(ax, 1.7, 3.0, 1.7, 2.8)

# Step 9: Chrome Extension
draw_action(ax, 9.4, 2.25, 2.3, 0.55, 'Scrape Application\nQuestions',
            C_EXT, sublabel='DOM scraping\n(form fields)')
arr(ax, 2.9, 2.52, 9.4, 2.52, 'Open application form', color='#888888')

# Step 10: Send to backend
draw_action(ax, 3.5, 1.5, 2.5, 0.55, 'Generate Answers\n(ExtensionService)',
            C_ASYNC, sublabel='Groq Llama 3.3-70b\nfull resume, no truncation')
draw_action(ax, 6.5, 1.5, 2.5, 0.55, 'Groq answer gen\nLlama 3.3-70b-versatile',
            C_SYSTEM, sublabel='per question\n(streaming)')
arr(ax, 9.4, 2.25, 5.1, 2.05, 'questions + JD\n(POST /extension/answers)', color='#888888')
arr(ax, 6.0, 1.77, 6.5, 1.77, 'API call', color='#888888')

# WebSocket stream
arr(ax, 5.1, 1.5, 9.4, 1.77, 'WS stream\nanswers', color='#9B59B6')

# HITL
draw_action(ax, 9.4, 0.85, 2.3, 0.55, '[HITL] Review &\nEdit Answers',
            C_HITL, sublabel='Human in the loop\nbefore submit')
arr(ax, 10.55, 1.5, 10.55, 1.4)

# Submit
draw_action(ax, 0.5, 0.55, 2.4, 0.55, 'Submit Application',
            C_ACTION, sublabel='status → "applied" in DB')
arr(ax, 9.4, 1.12, 2.9, 0.82, 'Approved answers\n(submit form)', color='#888888')

# END
draw_circle(ax, 1.7, 0.35, 0.15, '#E74C3C')
draw_circle(ax, 1.7, 0.35, 0.22, 'none')
c2 = plt.Circle((1.7, 0.35), 0.22, facecolor='none', edgecolor='#E74C3C', lw=2, zorder=4)
ax.add_patch(c2)
arr(ax, 1.7, 0.55, 1.7, 0.5)

# Legend
legend_elements = [
    mpatches.Patch(facecolor=C_ACTION,   edgecolor='#333', label='User Action'),
    mpatches.Patch(facecolor=C_ASYNC,    edgecolor='#333', label='Async Task (Celery)'),
    mpatches.Patch(facecolor=C_SYSTEM,   edgecolor='#333', label='External Service'),
    mpatches.Patch(facecolor=C_EXT,      edgecolor='#333', label='Chrome Extension'),
    mpatches.Patch(facecolor=C_HITL,     edgecolor='#333', label='Human-in-the-Loop'),
    mpatches.Patch(facecolor=C_DECISION, edgecolor='#333', label='Decision'),
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=7.5,
          framealpha=0.9, bbox_to_anchor=(11.9, 0.0), ncol=2)

plt.tight_layout()
plt.savefig('/home/mehrin/repo/mini-project/backend/report/activity.png',
            dpi=100, bbox_inches='tight', facecolor='white')
print("activity.png saved")
