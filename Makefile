.PHONY: clean
clean:
	rm -rf .tox

.PHONY: requirements
requirements:
	tox -e requirements-py36


.PHONY: develop
develop:
	tox -e test-py36 --notest
	bash -c "bash --init-file <(echo 'source .tox/test-py36/bin/activate')"


.PHONY: ingest
ingest:
	rm -f data/*
	tox -e test-py36 -- python -m pipeline ingest


.PHONY: elk
elk:
	cd containers/elk && docker-compose up


.PHONY: export
	tox -e test-py36 -- python -m pipeline export


.PHONY: notebook
notebook:
	tox -e test-py36 -- jupyter notebook --notebook-dir=notebooks

.PHONY: notebook-strip
notebook-strip:
	tox -e test-py36 -- nbstripout notebooks/playground.ipynb
