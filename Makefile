.PHONY: build validate test check clean demo outreach

build:
	python3 scripts/compile.py

validate:
	python3 scripts/validate.py

test:
	python3 -m unittest discover -s tests -q

check: build validate test

demo:
	@python3 -m afr.cli coverage
	@echo
	@python3 -m afr.cli gaps
	@echo
	@python3 -m afr.cli profile examples/agent-xray-counts.json -s agent-xray

clean:
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
	rm -rf .pytest_cache

outreach:
	python3 scripts/export_mapping.py agentrx    > outreach/01-agentrx/afr-mapping.yaml
	python3 scripts/export_mapping.py agent-xray > outreach/02-agent-xray/afr-mapping.yaml
	@echo "regenerated vendor mapping files from index $$(python3 -c 'import afr;print(afr.version())')"
