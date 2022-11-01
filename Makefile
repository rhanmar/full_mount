run:
	uvicorn main:app --reload

test:
	pytest

generate_data:
	http get localhost:8000/create/data