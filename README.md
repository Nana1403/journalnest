## 📓 JournalNest

  *-------------------------------------Your notes, inside notebooks that feel like your own.----------------------------------------*
  
  
JournalNest is a cozy note-taking web app inspired by real notebooks. Users can create personalized notebooks, write labels on their covers, and organize their notes on notebook-style pages. It is designed for class notes, journals, project planning, creative ideas, and everyday thoughts—all in one private space.

## Current Features

JournalNest currently includes:

- **Private accounts:** Users can sign up, log in, and log out. Each user can only access their own notebooks and notes.
- **Notebook shelf:** Notebooks appear in a responsive grid with personalized covers and handwritten-style labels.
- **Cover customization:** Users can choose a cover color, pattern, label font, and notebook type while viewing a live preview.
- **Notebook templates:** Users can create a class notebook, journal, project notebook, idea book, or blank notebook.
- **Note management:** Notes can be created, edited, renamed, and moved to the trash.
- **Autosave:** Notes save automatically after the user pauses typing. A manual **Save** button is also available.
- **Save feedback:** The app displays `Unsaved`, `Saving`, `Saved`, and `Could not save` messages.
- **Conflict protection:** Revision numbers prevent one browser tab from silently overwriting changes made in another.
- **Validated requests:** Pydantic validates autosave and cover-customization data.
- **Railway support:** Production settings are included for PostgreSQL, WhiteNoise, Gunicorn, and environment variables.

## Planned Features

Future updates will include:

- Margin notes
- Sticky notes
- An unfinished-thought bookmark
- Search
- Favorite notebooks
- Trash restoration
- Draggable stickers
- Custom cover image uploads

Some supporting database fields and schemas already exist, making these features easier to add later.

## Run Locally

JournalNest requires Python 3.12 or newer.

```bash
git clone https://github.com/your-username/journalnest.git
cd journalnest

python3 -m venv .venv
source .venv/bin/activate

python -m pip install -r requirements.txt
cp .env.example .env

python manage.py migrate
python manage.py runserver
```

On Windows, activate the virtual environment with:

```bash
.venv\Scripts\activate
```

After starting the server, open:

[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

Create an account to begin using the app.

To create an administrator account, run:

```bash
python manage.py createsuperuser
```

Then visit:

```text
http://127.0.0.1:8000/admin/
```

Run the tests with:

```bash
python manage.py test
```

> If Homebrew reports that Python is externally managed, make sure the virtual environment is active before installing the requirements.

## How It Works

1. Create an account and open your notebook shelf.
2. Select **New notebook**.
3. Choose a notebook type.
4. Personalize the notebook cover and label.
5. Open the notebook and select **Add note**.
6. Start writing and follow the save-status message.
7. Return later and continue where you stopped.

For example, a notebook labeled **Machine Learning** could contain notes titled:

- Linear Regression
- Model Evaluation
- Neural Networks
- Project Brainstorming

## Anders!!,  Notebook Design

JournalNest uses cream paper, blush pink, sage green, lavender, soft blue, and burgundy accents to create a warm notebook-inspired style.

| Element | Design |
| --- | --- |
| Notebook shelf | Responsive grid of closed notebook covers |
| Front label | Editable handwritten-style label that also serves as the notebook name |
| Cover styles | Custom colors, patterns, rounded corners, and soft shadows |
| Open notebook | Cream paper, ruled lines, a colored margin, and spiral binding |
| Note navigation | Page-title list with previous and next controls |
| Writing area | Title field and comfortable, auto-expanding editor |
| Save feedback | Clear autosave and error-status messages |
| Mobile layout | Full-width writing page with a collapsible page list |

The interface also includes keyboard focus indicators, readable color contrast, and support for reduced-motion preferences.

## Notebook Templates

| Notebook Type | Starting Prompt |
| --- | --- |
| Class notebook | Topic, key concepts, examples, and questions |
| Journal | Date, thoughts, feelings, and reflections |
| Project notebook | Goal, tasks, progress, and next steps |
| Idea book | Idea, inspiration, possibilities, and first step |
| Blank notebook | An empty page without a starting prompt |

Templates are editable starting points, not required forms. Users can change the prompts or begin with a blank page.

## Tech Stack

| Technology | Purpose |
| --- | --- |
| Python and Django | Backend, authentication, database models, and page rendering |
| Pydantic | Validation for autosave and customization requests |
| HTML and CSS | Notebook covers, paper-style pages, and responsive layouts |
| JavaScript | Autosave, live previews, and interactive controls |
| SQLite | Local development database |
| PostgreSQL | Production database |
| Gunicorn | Production application server |
| WhiteNoise | Static-file serving |
| Railway | Application and database hosting |

## Data and Security

JournalNest uses three main models:

| Model | Main Data |
| --- | --- |
| `User` | Django account information |
| `Notebook` | Owner, label, font, cover design, stickers, type, favorite status, and timestamps |
| `Note` | Notebook, title, content, position, revision, deletion time, and timestamps |

Every request checks notebook ownership on the server. Pydantic helps validate submitted data, but it does not replace authentication or permission checks.

Notebook and note IDs use UUIDs. If someone tries to open another user's notebook by guessing its URL, the server returns a `404` response.

## Railway Deployment

1. Push the project to GitHub.
2. Create a new Railway service from the GitHub repository.
3. Add a PostgreSQL database.
4. Connect the PostgreSQL `DATABASE_URL` to the app service.
5. Add the required production environment variables.
6. Run the build and migration commands.
7. Generate a public Railway domain.
8. Add the domain to `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`.
9. Redeploy the application.

### Environment Variables

| Variable | Production Value |
| --- | --- |
| `DJANGO_SECRET_KEY` | A strong and unique secret |
| `DEBUG` | `False` |
| `DATABASE_URL` | Reference to the Railway PostgreSQL service |
| `ALLOWED_HOSTS` | Exact app hostname without `https://` |
| `CSRF_TRUSTED_ORIGINS` | Complete app origin including `https://` |

### Build Command

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput
```
### Pre-Deploy Command

```bash
python manage.py migrate --noinput

```
### Start Command

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

When `DEBUG=False`, the project enables secure session and CSRF cookies, HTTPS redirection, HSTS, and proxy SSL header handling.
Before launching the application, run:

```bash
python manage.py check --deploy
```

## Project Purpose

JournalNest was created for education and personal learning. It is also a portfolio project that demonstrates skills in Django, database design, authentication, validation, responsive design, security, and application deployment. The goal is to create a note-taking experience that feels more personal and comforting than a traditional notes app.

## License

This project was created for educational and personal learning purposes. Before releasing the code as an open-source project, add a separate license file that explains how others may use, modify, and share the project.
