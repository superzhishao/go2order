"""
Auto-seed database with demo data on first startup.

Usage:
  python -m scripts.seed          # run standalone
  Called automatically via app lifespan if tables are empty.

Checks if go2run_store_shop table has any rows.
If empty, imports scripts/init-db.sql via mysql CLI.
"""
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse, parse_qs

# Allow running as `python -m scripts.seed` from project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SQL_FILE = PROJECT_ROOT / "scripts" / "init-db.sql"


def parse_db_url(url: str) -> dict:
    """Parse DATABASE_URL into mysql CLI connection args."""
    # Strip async driver prefix: mysql+aiomysql:// -> mysql://
    url = url.replace("mysql+aiomysql://", "mysql://").replace("mysql+asyncmy://", "mysql://")
    p = urlparse(url)
    params = parse_qs(p.query)
    return {
        "host": p.hostname or "localhost",
        "port": p.port or 3306,
        "user": p.username or "root",
        "password": p.password or "",
        "database": p.path.lstrip("/").split("?")[0],
        "charset": params.get("charset", ["utf8mb4"])[0],
    }


def is_empty(db: dict) -> bool:
    """Check if seed table has zero rows."""
    cmd = [
        "mysql",
        f"-h{db['host']}", f"-P{db['port']}",
        f"-u{db['user']}", f"-p{db['password']}",
        "--skip-ssl",
        db["database"],
        "-sNe", "SELECT COUNT(*) FROM go2run_store_shop",
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        count = int(result.stdout.strip())
        return count == 0
    except Exception:
        # Table doesn't exist or DB not reachable — needs seeding
        return True


def seed(db: dict) -> bool:
    """Import init-db.sql into the database. Returns True on success."""
    if not SQL_FILE.exists():
        print(f"[seed] SQL file not found: {SQL_FILE}")
        return False

    cmd = [
        "mysql",
        f"-h{db['host']}", f"-P{db['port']}",
        f"-u{db['user']}", f"-p{db['password']}",
        "--skip-ssl",
        f"--default-character-set={db['charset']}",
    ]
    print(f"[seed] Importing {SQL_FILE.name} into {db['database']}...")
    with open(SQL_FILE) as f:
        result = subprocess.run(cmd, stdin=f, capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        print(f"[seed] ERROR: {result.stderr.strip()}")
        return False
    print("[seed] Done — demo data loaded successfully.")
    return True


def run():
    """Main entry point."""
    # Load DATABASE_URL from .env or environment
    sys.path.insert(0, str(PROJECT_ROOT))
    from app.config import settings
    db = parse_db_url(settings.DATABASE_URL)

    if is_empty(db):
        print("[seed] Database is empty, seeding with demo data...")
        seed(db)
    else:
        print("[seed] Database already has data, skipping seed.")


if __name__ == "__main__":
    run()
