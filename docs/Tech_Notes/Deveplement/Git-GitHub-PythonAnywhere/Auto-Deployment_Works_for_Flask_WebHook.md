By setting up a webhook between GitHub and your Flask app, every time you `git push` changes to GitHub, PythonAnywhere will automatically pull the new code and reload your web app—giving you hands-off continuous deployment.

### How Auto-Deployment Works for Flask

Unlike static files (which update immediately when overwritten), a Flask app runs in Python's memory. To make your new Python code go live, the webhook needs to perform two actions:

1. **Pull the code.** Run `git pull` in your project directory to download your latest commits.
2. **Reload the web app.** Trigger PythonAnywhere to restart your WSGI process so it loads the new Python code into memory.

---

## Step 1: Add the Auto-Deploy Route to Your Flask App

Add a dedicated route (like `/git_update`) to your existing Flask app. On PythonAnywhere, touching (`os.utime`) your WSGI file is the built-in shortcut that forces the server to reload your app automatically.

python

```
import os
import hmac
import hashlib
import subprocess
from flask import request, abort

# Store your secret in an environment variable or config file in production
GITHUB_SECRET = b'your-super-secret-token'
PROJECT_DIR = '/home/yourusername/your-flask-project'
WSGI_FILE = '/var/www/yourusername_pythonanywhere_com_wsgi.py'

@app.route('/git_update', methods=['POST'])
def git_update():
    # 1. Verify the signature from GitHub
    signature = request.headers.get('X-Hub-Signature-256')
    if not signature:
        abort(403)
    
    mac = hmac.new(GITHUB_SECRET, msg=request.data, digestmod=hashlib.sha256)
    expected_signature = 'sha256=' + mac.hexdigest()
    
    if not hmac.compare_digest(expected_signature, signature):
        abort(403)

    # 2. Pull the latest code from GitHub
    subprocess.run(['git', '-C', PROJECT_DIR, 'pull'], check=True)

    # 3. Touch the WSGI file to reload the PythonAnywhere web app
    os.utime(WSGI_FILE, None)

    return 'Updated and reloaded successfully!', 200
```

Use code with caution.

_Note: You can find the exact path to your `WSGI_FILE` by looking at the **WSGI configuration file** link on your PythonAnywhere **Web** tab._

---

## Step 2: Connect GitHub to Your Endpoint

1. Go to your Flask repository on GitHub and click **Settings** > **Webhooks** > **Add webhook**.
2. Set the **Payload URL** to `https://pythonanywhere.com`.
3. Set **Content type** to `application/json`.
4. Enter your `GITHUB_SECRET` into the **Secret** field.
5. Select **Just the push event** and click **Add webhook**.

---

## Key Things to Keep in Mind

- **Install new packages.** If you update `requirements.txt`, `git pull` alone won't install new libraries. You can add a line in your webhook to run your virtual environment's pip: `subprocess.run(['/home/yourusername/.virtualenvs/myenv/bin/pip', 'install', '-r', f'{PROJECT_DIR}/requirements.txt'])`.
- **Branch filtering.** By default, any push to _any_ branch triggers the webhook. If you only want pushes to `main` to deploy, check `if request.json.get('ref') != 'refs/heads/main': return 'Ignored branch', 200` right after verifying the signature.
- **Private repositories.** If your repo is private, set up an SSH deploy key on PythonAnywhere so `git pull` runs without asking for a username or password.

---
### Deploy two repos to PythonAnywhere

**FlaskApp** and **AppAdmin** run as **two separate PythonAnywhere web apps** or as **one combined web app** on the same domain.

## Scenario A: Two Separate PythonAnywhere Web Apps (Most Common)

If each repo has its own domain or subdomain (for example, `://yourdomain.com` and `://yourdomain.com`), you simply repeat the setup independently for each project.

- **Separate endpoints.** Add a `/git_update` route inside `FlaskApp` and a `/git_update` route inside `AppAdmin`.
- **Separate paths.** Each app's webhook points to its own `PROJECT_DIR` and touches its own specific `WSGI_FILE`.
- **Separate GitHub webhooks.** Configure a webhook in the `FlaskApp` GitHub repo pointing to `https://yourdomain.com`, and another in the `AppAdmin` GitHub repo pointing to `https://yourdomain.com`.

---

## Scenario B: Both Repos Inside One PythonAnywhere Web App

If both repositories live on your PythonAnywhere account and are served under the **same domain** (for example, `AppAdmin` is mounted at `/admin` or imported as a package inside `FlaskApp`), you only need **one webhook listener** inside your main `FlaskApp` that handles both repositories.

1. Update Your Webhook Route to Check the Repo Name

GitHub sends the repository's name inside the JSON payload (`request.json['repository']['name']`). You can use this to decide which folder to pull:

python

```
import os
import hmac
import hashlib
import subprocess
from flask import request, abort

GITHUB_SECRET = b'your-shared-secret-token'
WSGI_FILE = '/var/www/yourusername_pythonanywhere_com_wsgi.py'

REPOS = {
    'FlaskApp': '/home/yourusername/FlaskApp',
    'AppAdmin': '/home/yourusername/AppAdmin',
}

@app.route('/git_update', methods=['POST'])
def git_update():
    # 1. Verify signature
    signature = request.headers.get('X-Hub-Signature-256')
    if not signature:
        abort(403)
    
    mac = hmac.new(GITHUB_SECRET, msg=request.data, digestmod=hashlib.sha256)
    if not hmac.compare_digest('sha256=' + mac.hexdigest(), signature):
        abort(403)

    # 2. Identify which repo triggered the webhook
    payload = request.get_json(silent=True) or {}
    repo_name = payload.get('repository', {}).get('name')

    if repo_name not in REPOS:
        return f'Repository {repo_name} not configured', 400

    # 3. Pull the matching repo and reload the single WSGI file
    subprocess.run(['git', '-C', REPOS[repo_name], 'pull'], check=True)
    os.utime(WSGI_FILE, None)

    return f'{repo_name} updated and reloaded!', 200
```

Use code with caution.

2. Point Both GitHub Repos to the Same URL

- In **both** the `FlaskApp` and `AppAdmin` repositories on GitHub, add a webhook pointing to the **exact same Payload URL** (`https://pythonanywhere.com`) using the same `GITHUB_SECRET`.

---

One Extra Detail for Private Repos

If both repositories are **private** on GitHub and you use SSH keys to pull them, keep in mind that GitHub does not allow you to reuse the exact same SSH Deploy Key across two different repositories.

- **Option 1 (Easiest):** Generate one personal SSH key on PythonAnywhere (`ssh-keygen`) and add it to your **GitHub User Account Settings** (under _SSH and GPG keys_) instead of individual repo deploy keys. This grants PythonAnywhere pull access to all your repos.
- **Option 2:** Generate two separate deploy keys and configure `~/.ssh/config` on PythonAnywhere with host aliases so Git knows which key to use for each repo.

Since ==**AppAdmin** is a module inside **FlaskApp**==, both run under your single PythonAnywhere web app. You only need **one webhook route** inside `FlaskApp` to update whichever repository changed and reload your WSGI file.

Because `AppAdmin` is a **private repository**, you will also need to configure an SSH key on PythonAnywhere so `git pull` can authenticate automatically without asking for a password.

---

## Step 1: Set Up SSH Access for Your Private Repo (`AppAdmin`)

Because `FlaskApp` is public, it can pull without credentials, while `AppAdmin` needs authentication. Setting up a **Deploy Key** on `AppAdmin` is the safest way to grant read-only pull access to just that repository.

1. **Generate an SSH key on PythonAnywhere.** Open a **Bash console** on PythonAnywhere and run:
    
    bash
    
    ```
    ssh-keygen -t ed25519 -f ~/.ssh/id_appadmin -N ""
    ```
    
    Use code with caution.
    
2. **Copy the public key.** Run this command and copy the output line starting with `ssh-ed25519`:
    
    bash
    
    ```
    cat ~/.ssh/id_appadmin.pub
    ```
    
    Use code with caution.
    
3. **Add it to GitHub.** Go to your **AppAdmin** repository on GitHub > **Settings** > **Deploy keys** > **Add deploy key**. Paste the key, give it a title (like `PythonAnywhere`), leave "Allow write access" unchecked, and save.
4. **Tell Git to use this key.** On PythonAnywhere, ensure `AppAdmin` uses the SSH URL (not HTTPS) and tell Git which key to use:
    
    bash
    
    ```
    cd /home/yourusername/FlaskApp/AppAdmin
    git remote set-url origin git@github.com:yourusername/AppAdmin.git
    git config core.sshCommand "ssh -i ~/.ssh/id_appadmin -o IdentitiesOnly=yes"
    ```
    
    Use code with caution.
    
5. **Test the connection.** Run `git pull` inside the `AppAdmin` folder once manually to accept GitHub's host fingerprint (`yes`) and confirm it pulls cleanly without a password prompt.

_(Note: If you linked `AppAdmin` as a **Git Submodule** inside `FlaskApp`, see the note at the bottom.)_

---

## Step 2: Add the Combined Webhook Route to `FlaskApp`

Add this route to `FlaskApp`. It checks the incoming GitHub payload to see whether `FlaskApp` or `AppAdmin` triggered the push, pulls the corresponding directory, and reloads the web app.

python

```
import os
import hmac
import hashlib
import subprocess
from flask import request, abort

GITHUB_SECRET = b'your-super-secret-token'
WSGI_FILE = '/var/www/yourusername_pythonanywhere_com_wsgi.py'

# Map exact GitHub repository names to their folders on PythonAnywhere
REPOS = {
    'FlaskApp': '/home/yourusername/FlaskApp',
    'AppAdmin': '/home/yourusername/FlaskApp/AppAdmin',
}

@app.route('/git_update', methods=['POST'])
def git_update():
    # 1. Verify the signature from GitHub
    signature = request.headers.get('X-Hub-Signature-256')
    if not signature:
        abort(403)
    
    mac = hmac.new(GITHUB_SECRET, msg=request.data, digestmod=hashlib.sha256)
    if not hmac.compare_digest('sha256=' + mac.hexdigest(), signature):
        abort(403)

    # 2. Only deploy on pushes to the main branch
    payload = request.get_json(silent=True) or {}
    if payload.get('ref') != 'refs/heads/main':
        return 'Ignored non-main branch', 200

    # 3. Identify which repo was pushed and pull its folder
    repo_name = payload.get('repository', {}).get('name')
    if repo_name not in REPOS:
        return f'Unknown repository: {repo_name}', 400

    subprocess.run(['git', '-C', REPOS[repo_name], 'pull'], check=True)

    # 4. Reload the PythonAnywhere web app
    os.utime(WSGI_FILE, None)

    return f'{repo_name} updated and reloaded!', 200
```

Use code with caution.

---

## Step 3: Add the Webhook to Both GitHub Repositories

Repeat these exact steps in **both** the `FlaskApp` and `AppAdmin` repositories on GitHub:

1. Go to **Settings** > **Webhooks** > **Add webhook**.
2. **Payload URL:** `https://pythonanywhere.com`
3. **Content type:** `application/json`
4. **Secret:** Your `GITHUB_SECRET` string
5. **Events:** Select **Just the push event** and save.

---

## One Quick Check: Are You Using a Git Submodule?

- **Nested Git Clone (Standard):** If you cloned `AppAdmin` inside `FlaskApp` as an independent folder (and listed `AppAdmin/` in `FlaskApp`'s `.gitignore`), the setup above works out of the box.
- **Git Submodule:** If you formally added `AppAdmin` via `git submodule add`, replace the `subprocess.run` line in Step 2 with this so Git updates both the parent repo and the submodule pointer cleanly:
    
    python
    
    ```
    subprocess.run(['git', '-C', REPOS['FlaskApp'], 'pull', '--recurse-submodules'], check=True)
    subprocess.run(['git', '-C', REPOS['FlaskApp'], 'submodule', 'update', '--remote'], check=True)
    ```
    
    Use code with caution.