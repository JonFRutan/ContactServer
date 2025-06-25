VENV := .venv

setup:
	Setup/venv_setup.sh
	$(VENV)/bin/python3 Setup/init_db.py 
	sudo Setup/radicale_user.sh
