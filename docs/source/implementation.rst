==========================
Implementation
==========================

This section outlines the features developed, implementation issues encountered, and how they were resolved.

Demo Video
------------------
A 3–5 minute demo has been recorded showcasing core features:
- User login and registration system
- Pantry interface with add/remove ingredient functionality
- Real-time recipe matching based on pantry contents
- Recipe detail pages (with steps, images, servings, and nutritional info)
- Shopping list and timer components
- Styled frontend using HTML/CSS with consistent UI theme

🎥 Demo link: [Insert video link here, e.g. YouTube or Google Drive]

Technologies Used
------------------

- **Python (Flask):** for backend server and routing
- **HTML/CSS:** frontend design and structure
- **Jinja2:** template rendering
- **JavaScript (minimal):** for frontend interactivity
- **SQLite + SQLAlchemy:** user management and future persistence
- **Read the Docs + Sphinx:** for documentation
- **Git + GitHub:** for version control

Implementation Challenges & Solutions
----------------------------------------

**1. Environment issues across systems**  
Team members experienced inconsistent setups (e.g. virtualenv path issues, Python not in PATH). Solved using absolute paths and `Set-ExecutionPolicy RemoteSigned` for PowerShell.

**2. Merge conflicts in requirements.txt**  
Due to multiple branches and feature merging, conflicts in dependencies arose. Resolved manually by consolidating package lists and re-committing after cleanup.

**3. Abandoning scraping for local recipes**  
Web scraping was more complex and time-consuming than expected. Replaced with a curated local JSON file of 15+ recipes including full metadata (ingredients, steps, calories, image links).

**4. Styling the pantry to match the main app**  
Pantry UI lacked integration. Resolved by importing and reusing the main `style.css` and unifying HTML structure.

Lessons Learned
------------------

- Technical scope needs to match time constraints
- Clear division of tasks makes collaboration smoother
- Version control must be used responsibly to avoid chaos
- Sometimes simple JSON is better than scraping the entire internet
