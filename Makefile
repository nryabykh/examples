GENERATE_VERSION = $(shell cat version.py | grep __version__ | head -n 1 | sed -re 's/[^"]+//' | sed -re 's/"//g' )
GENERATE_BRANCH = $(shell git name-rev $$(git rev-parse HEAD) | cut -d\  -f2 | sed -re 's/^(remotes\/)?origin\///' | tr '/' '_')
SET_VERSION = $(eval VERSION=$(GENERATE_VERSION))
SET_BRANCH = $(eval BRANCH=$(GENERATE_BRANCH))

.SILENT:

pack:
	$(SET_VERSION)
	$(SET_BRANCH)
	rm -f asum-*.tgz
	echo Remove __pycache__...
	find common data models pages reporting -name __pycache__ -type d -exec rm -rf {} +

	echo Pack asum...
	tar czf asum-$(VERSION)-$(BRANCH).tgz --exclude=*.pickle --exclude=*.pdf --exclude=reports/*.png .streamlit common data images models pages reporting storage *.py *.md Makefile
