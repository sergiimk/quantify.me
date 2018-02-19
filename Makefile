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
