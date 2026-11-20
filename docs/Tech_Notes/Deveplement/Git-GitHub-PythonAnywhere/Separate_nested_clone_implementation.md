---
title: Separate Nested Clone Implementation
category: Tech_Notes
tags:
  - Tech_Notes
  - Deveplement
  - Git-GitHub-PythonAnywhere
status: in progress
created: 2026-11-16
updated: 2026-11-16
---
Setting up a **separate nested clone** is straightforward and keeps your public `FlaskApp` repository completely unaware of your private `AppAdmin` repository, while letting Python import `AppAdmin` seamlessly as a local module.

Here is the complete step-by-step guide covering local setup, Flask integration, PythonAnywhere deployment, and webhook automation.

---

## Phase 1: Local Machine Setup

First, configure your local development environment so Git keeps the two repositories separate.

1. **Ignore `AppAdmin` in `FlaskApp`.** Open the `.gitignore` file in the root of your `FlaskApp` folder and add `AppAdmin/` on a new line:
    
    text
    
    ```
    AppAdmin/
    ```
    
    Use code with caution.
    
    _If `AppAdmin` was previously tracked by `FlaskApp`, run `git rm -r --cached AppAdmin` once to stop tracking it without deleting your files._
2. **Clone `AppAdmin` inside `FlaskApp`.** Open your terminal inside your `FlaskApp` directory and clone the private repo:
    
    bash
    
    ```
    cd /path/to/FlaskApp
    git clone https://github.com
    ```
    
    Use code with caution.
    
3. **Commit the `.gitignore` change to `FlaskApp`.**
    
    bash
    
    ```
    git add .gitignore
    git commit -m "Ignore nested AppAdmin module"
    git push origin main
    ```
    
    Use code with caution.
    

---

## Phase 2: Flask Module Implementation

Make `AppAdmin` act as a clean Python package (usually via a Flask **Blueprint**) so `FlaskApp` can load it cleanly—or skip it gracefully if someone clones your public `FlaskApp` repo without having access to `AppAdmin`.

1. **Structure your folders** like this:
    
    text
    
    ```
    FlaskApp/
    ├── .git/
    ├── .gitignore          # Contains "AppAdmin/"
    ├── app.py
    └── AppAdmin/           # Nested private repo
        ├── .git/
        ├── __init__.py
        └── routes.py
    ```
    
    Use code with caution.
    
2. **Create a Blueprint in `AppAdmin/routes.py`:**
    
    python
    
    ```
    from flask import Blueprint
    
    admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
    
    @admin_bp.route('/')
    def dashboard():
        return 'Admin Dashboard'
    ```
    
    Use code with caution.
    
3. **Expose the Blueprint in `AppAdmin/__init__.py`:**
    
    python
    
    ```
    from .routes import admin_bp
    ```
    
    Use code with caution.
    
4. **Register it safely in `FlaskApp/app.py`.** Using a `try/except ImportError` block ensures your public `FlaskApp` still runs without crashing if `AppAdmin` isn't present:
    
    python
    
    ```
    from flask import Flask
    
    app = Flask(__name__)
    
    try:
        from AppAdmin import admin_bp
        app.register_blueprint(admin_bp)
    except ImportError:
        print("AppAdmin module not installed; running in public mode.")
    ```
    
    Use code with caution.
    

---

## Phase 3: PythonAnywhere Server Setup

Now mirror that exact folder structure on PythonAnywhere and set up the SSH deploy key for your private `AppAdmin` repo.

1. **Open a PythonAnywhere Bash console** and clone your public `FlaskApp`:
    
    bash
    
    ```
    cd ~
    git clone https://github.com
    ```
    
    Use code with caution.
    
2. **Generate an SSH deploy key for `AppAdmin`:**
    
    bash
    
    ```
    ssh-keygen -t ed25519 -f ~/.ssh/id_appadmin -N ""
    cat ~/.ssh/id_appadmin.pub
    ```
    
    Use code with caution.
    
3. **Add the key to GitHub.** Copy the output from `cat`, go to your **AppAdmin** repo on GitHub > **Settings** > **Deploy keys** > **Add deploy key**, paste it, and save.
4. **Clone `AppAdmin` inside `FlaskApp` using that key:**
    
    bash
    
    ```
    cd ~/FlaskApp
    GIT_SSH_COMMAND="ssh -i ~/.ssh/id_appadmin -o IdentitiesOnly=yes" git clone git@github.com:yourusername/AppAdmin.git
    ```
    
    Use code with caution.
    
5. **Save the SSH key setting inside `AppAdmin`'s local Git config** so future `git pull` commands use it automatically:
    
    bash
    
    ```
    cd ~/FlaskApp/AppAdmin
    git config core.sshCommand "ssh -i ~/.ssh/id_appadmin -o IdentitiesOnly=yes"
    ```
    
    Use code with caution.
    

---

## Phase 4: Auto-Deploy Webhook Implementation

Finally, add the webhook route to `FlaskApp/app.py` so pushing to _either_ repository automatically updates that specific folder and reloads your site.

python

```
import os
import hmac
import hashlib
import subprocess
from flask import request, abort

GITHUB_SECRET = b'your-super-secret-token'
WSGI_FILE = '/var/www/yourusername_pythonanywhere_com_wsgi.py'

REPOS = {
    'FlaskApp': '/home/yourusername/FlaskApp',
    'AppAdmin': '/home/yourusername/FlaskApp/AppAdmin',
}

@app.route('/git_update', methods=['POST'])
def git_update():
    # 1. Verify GitHub signature
    signature = request.headers.get('X-Hub-Signature-256')
    if not signature:
        abort(403)
    
    mac = hmac.new(GITHUB_SECRET, msg=request.data, digestmod=hashlib.sha256)
    if not hmac.compare_digest('sha256=' + mac.hexdigest(), signature):
        abort(403)

    # 2. Only deploy on pushes to main
    payload = request.get_json(silent=True) or {}
    if payload.get('ref') != 'refs/heads/main':
        return 'Ignored non-main branch', 200

    # 3. Pull the matching repository folder
    repo_name = payload.get('repository', {}).get('name')
    if repo_name not in REPOS:
        return f'Unknown repository: {repo_name}', 400

    subprocess.run(['git', '-C', REPOS[repo_name], 'pull'], check=True)

    # 4. Reload PythonAnywhere web app
    os.utime(WSGI_FILE, None)

    return f'{repo_name} updated and reloaded!', 200
```

Use code with caution.

## Final Checklist

- **Reload once manually.** Go to your PythonAnywhere **Web** tab and click **Reload** so the new `/git_update` route goes live.
- **Add webhooks to both repos.** In both `FlaskApp` and `AppAdmin` on GitHub, go to **Settings** > **Webhooks** > **Add webhook**, set the Payload URL to `https://pythonanywhere.com`, Content type to `application/json`, and enter your `GITHUB_SECRET`.

---
## Environment variable handling (GITHUB_SECRET isn't hardcored in the public FlaskApp repository)
Since you are already using a `.env.key` file to keep your real secrets on PythonAnywhere and dummy values on GitHub, you can load your `GITHUB_SECRET` directly from `.env.key` and expand your webhook to automatically install updated dependencies and run database migrations.

## Step 1: Add `GITHUB_SECRET` to Your `.env.key` File

Add a new variable to both your dummy `.env.key` in GitHub and your real `.env.key` on PythonAnywhere.

1. **In GitHub (dummy `.env.key`):**
    
    text
    
    ```
    GITHUB_SECRET=dummy-secret-for-local-dev
    ```
    
    Use code with caution.
    
2. **On PythonAnywhere (real `.env.key`):**
    
    text
    
    ```
    GITHUB_SECRET=your-real-super-secret-token
    ```
    
    Use code with caution.
    
    _(Ensure your real `.env.key` on PythonAnywhere is ignored by Git—either via `.gitignore` or `git update-index --skip-worktree .env.key`—so `git pull` never overwrites it or fails with a merge conflict.)_

---

## Step 2: Load `.env.key` and Automate `pip` + Migrations

Assuming you use `python-dotenv` to load `.env.key`, your webhook can inspect the incoming GitHub payload to see **which files changed** (`commits` -> `modified`/`added`) and only run `pip install` or database migrations when needed. This keeps routine code deployments fast.

Here is the complete, updated webhook route for `FlaskApp/app.py`:

python

```
import os
import hmac
import hashlib
import subprocess
from dotenv import load_dotenv
from flask import request, abort

# Load variables from .env.key
BASE_DIR = '/home/yourusername/FlaskApp'
load_dotenv(os.path.join(BASE_DIR, '.env.key'))

# Encode the loaded secret to bytes for HMAC verification
GITHUB_SECRET = os.environ.get('GITHUB_SECRET', '').encode('utf-8')

WSGI_FILE = '/var/www/yourusername_pythonanywhere_com_wsgi.py'
VENV_BIN = '/home/yourusername/.virtualenvs/myenv/bin'

REPOS = {
    'FlaskApp': BASE_DIR,
    'AppAdmin': os.path.join(BASE_DIR, 'AppAdmin'),
}

@app.route('/git_update', methods=['POST'])
def git_update():
    # 1. Verify secret is configured and matches GitHub's signature
    if not GITHUB_SECRET:
        abort(500)

    signature = request.headers.get('X-Hub-Signature-256')
    if not signature:
        abort(403)
    
    mac = hmac.new(GITHUB_SECRET, msg=request.data, digestmod=hashlib.sha256)
    if not hmac.compare_digest('sha256=' + mac.hexdigest(), signature):
        abort(403)

    # 2. Only deploy on pushes to main
    payload = request.get_json(silent=True) or {}
    if payload.get('ref') != 'refs/heads/main':
        return 'Ignored non-main branch', 200

    # 3. Pull the matching repository
    repo_name = payload.get('repository', {}).get('name')
    if repo_name not in REPOS:
        return f'Unknown repository: {repo_name}', 400

    repo_path = REPOS[repo_name]
    subprocess.run(['git', '-C', repo_path, 'pull'], check=True)

    # 4. Collect all changed files across commits in this push
    changed_files = set()
    for commit in payload.get('commits', []):
        changed_files.update(commit.get('added', []))
        changed_files.update(commit.get('modified', []))

    # 5. Install dependencies if requirements.txt changed
    if 'requirements.txt' in changed_files:
        subprocess.run(
            [f'{VENV_BIN}/pip', 'install', '-r', os.path.join(repo_path, 'requirements.txt')],
            check=True
        )

    # 6. Run database migrations if migration files changed (Flask-Migrate / Alembic)
    if any(f.startswith('migrations/') for f in changed_files):
        env = os.environ.copy()
        env['FLASK_APP'] = 'app.py'
        subprocess.run(
            [f'{VENV_BIN}/flask', 'db', 'upgrade'],
            cwd=BASE_DIR,
            env=env,
            check=True
        )

    # 7. Reload PythonAnywhere web app
    os.utime(WSGI_FILE, None)

    return f'{repo_name} updated and reloaded!', 200
```

Use code with caution.

---

## Important Configuration Details

- **Virtual environment path (`VENV_BIN`).** Replace `myenv` in `/home/yourusername/.virtualenvs/myenv/bin` with the actual name of your PythonAnywhere virtual environment. Calling `pip` and `flask` directly from `VENV_BIN` ensures packages install into the right environment without needing `workon`.
- **Keeping `.env.key` safe from `git pull`.** Since a dummy `.env.key` is tracked in your public GitHub repo, editing `.env.key` on PythonAnywhere would normally cause `git pull` to abort with _"Your local changes to .env.key would be overwritten by merge."_ To prevent this, run this command once in your PythonAnywhere Bash console inside `FlaskApp`:
    
    bash
    
    ```
    git update-index --skip-worktree .env.key
    ```
    
    Use code with caution.
    
    This tells Git on PythonAnywhere to ignore local edits to `.env.key` while keeping the dummy version intact on GitHub.
- **Database migration tool.** Step 6 assumes you use **Flask-Migrate** (`flask db upgrade`) with a `migrations/` folder. If you use raw Alembic (`alembic upgrade head`) or a custom migration script, replace that `subprocess.run` command with your migration command.