from datetime import datetime

from blacksheep import Application


app = Application()


@app.route("/workload", methods=["GET", "POST"])
async def add_workload():
    return f"Hello, World! {datetime.utcnow().isoformat()}"


@app.route("/workload/<int:id>", methods=["PUT", "DELETE"])
async def change_workload():
    return f"Hello, World! {datetime.utcnow().isoformat()}"


@app.route("/migration", methods=["GET", "POST"])
async def add_migration():
    return f"Hello, World! {datetime.utcnow().isoformat()}"


@app.route("/migration/<int:id>", methods=["PUT", "DELETE"])
async def change_migration():
    return f"Hello, World! {datetime.utcnow().isoformat()}"


@app.route("/migration/<int:id>/run", methods=["GET"])
async def run_migration():
    return f"Hello, World! {datetime.utcnow().isoformat()}"


@app.route("/migration/<int:id>/status", methods=["GET"])
async def check_migration_status():
    return f"Hello, World! {datetime.utcnow().isoformat()}"
