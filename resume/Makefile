IMAGE=tex-build
SRC=resume.source.tex

ifdef CI
	PDF=TylerLewis_resume.$(shell date -u +%Y-%m-%d).pdf
else
	PDF=TylerLewis_resume.local.pdf
endif

build:
	docker build -t $(IMAGE) . -f Dockerfile.tex

pdf:
	docker run --rm -v "$(PWD)":/work $(IMAGE) \
		-jobname=$(basename $(PDF)) $(SRC)

all: build pdf

watch:
	@echo "Watching $(SRC) for changes..."
	@while true; do \
		fswatch -1 $(SRC); \
		echo "Recompiling..."; \
		$(MAKE) pdf; \
	done

clean:
	rm -f *.aux *.log *.out *.toc *.pdf