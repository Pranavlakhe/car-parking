# Railway Deployment Fix Plan

## Status: Step 1 & 2 DONE

**Step 1: [DONE] Update app.py**
- Confirmed PyMySQL (pure Python, no libmariadb issue).
- Added DATABASE_URL parsing with urllib.parse for Railway MySQL.
- Fixed UPLOAD_FOLDER to /app/static/uploads for prod.
- Added MYSQL_PORT support.

**Step 2: [DONE] Update requirements.txt**
- No flask-mysqldb (cause of prod crash).
- Has PyMySQL==1.1.0, gunicorn==21.2.0, python-dotenv==1.0.1, Flask.

**Step 3: [PENDING] Commit & Push**
- `git add .`
- `git commit -m \"Fix prod crash: PyMySQL + Railway DB URL support\"`
- `git push`

**Step 4: [PENDING] Railway Actions**
- Add/confirm MySQL service in Railway project.
- Set Variables: SECRET_KEY (generate strong one).
- Railway auto-deploys on push.
- Connect to Railway MySQL (phpMyAdmin or CLI), run deploy-db.sql.
- Test https://car-parking-production-736c.up.railway.app

**Step 5: [PENDING] Verify**
- Check Deploy Logs (should boot gunicorn without ImportError).
- Test site functionality (register, login, book parking).

Next: Run git commands below, then check Railway.
