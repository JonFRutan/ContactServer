VENV := .venv

setup:
	venv_setup.sh
	../$(VENV)/bin/python3 init_db.py 
	sudo radicale_user.sh
