python3=python3
venv_dir=venv
nginx=nginx

wheel: chat_web/frontend_static
	python3 setup.py bdist_wheel

chat_web/frontend_static: frontend/pages/* frontend/components/*
	make build-frontend

$(venv_dir)/packages-installed: setup.py
	test -d $(venv_dir) || $(python3) -m venv $(venv_dir)
	$(venv_dir)/bin/pip install -U pip wheel
	$(venv_dir)/bin/pip install -e .
	touch $@

run-backend: $(venv_dir)/packages-installed
	$(venv_dir)/bin/chat-web

run-frontend:
	cd frontend && npm install
	cd frontend && npm run dev

build-frontend:
	cd frontend && npm install
	cd frontend && npm run build
	rm -rf chat_web/frontend_static
	mv -vi frontend/out chat_web/frontend_static

run-nginx:
	$(nginx) -c $(PWD)/nginx.conf

.PHONY: build-frontend
