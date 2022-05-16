from django.core.management import execute_from_command_line

def my_scheduled_job_save_db():
    execute_from_command_line(["manage.py", "dumpdata", ">", "db.json"])