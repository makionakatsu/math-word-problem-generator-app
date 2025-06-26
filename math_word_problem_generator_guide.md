# Math Word Problem Generator – Implementation Guide

## 0. Goal
**Math Word Problem Generator**  
- **Input**: Grade (1–12) and Difficulty (1–5)  
- **Output**: Word problems aligned with the Japanese curriculum, with grade‑dependent counts and 7‑stage hints  
- **UI**: Single‑page, responsive, printable on one A4 page  
- **Language**: Japanese only

---

## 1. Directory & File Structure

```text
math-word-problem-generator/
├── backend/
│   ├── __init__.py
│   ├── app.py                # FastAPI entry point
│   ├── generator.py          # Problem & hint generator logic
│   ├── curriculum_map.py     # Curriculum mapping definitions
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── tests/
│   └── test_generator.py
├── README.md
└── .gitignore
```

---

## 2. File Responsibilities & Implementation Points

| File | Role | Implementation Guide |
| --- | --- | --- |
| **backend/app.py** | FastAPI app definition | * Endpoints: `/health`, `/generate`  <br>* CORS: `["http://localhost:5500", "https://example.com"]` |
| **backend/curriculum_map.py** | Curriculum mapping | `CURRICULUM = { grade:int: { "topics": [...], "templates": [...] } }` |
| **backend/generator.py** | Problem & hint generation | ```python
def generate_problems(grade:int, diff:int)->list[Problem]:
    n = 5 if grade<=6 else 3 if grade<=9 else 1
    # random topic/template selection and placeholder filling
    # hints[0-2]=light, 3-5=core, 6=solution
    return problems
``` |
| **backend/requirements.txt** | Dependencies | `fastapi`, `uvicorn[standard]`, `pydantic>=2`, `pytest` |
| **frontend/index.html** | UI skeleton | Two `<select>` for grade/difficulty, buttons for Generate/Print, div for problems |
| **frontend/css/style.css** | Responsive & print styles | Mobile‑first flex layout; `@media print` header/footer with page counters |
| **frontend/js/main.js** | Front‑end logic | Fetch `/generate`, render problems, toggle hints, `window.print()` |
| **tests/test_generator.py** | Unit tests | Validate problem counts, 7 hints, error conditions |
| **README.md** | Setup guide | Virtualenv, install, run `uvicorn`, launch front‑end server |
| **.gitignore** | Ignore patterns | `.venv/`, `__pycache__/`, `*.log` |

---

## 3. Design Choices (任せる部分)

| Aspect | Decision |
| --- | --- |
| **Grade × Topic assignment** | Mapping based on latest curriculum; see `curriculum_map.py`. |
| **Hint text generation** | Seven‑layer hints: keywords → approach → full solution. |
| **Difficulty scaling** | Adjust numbers, extraneous info, and steps based on `diff` 1–5. |

---

## 4. Security & QA

* Input validation with pydantic  
* CORS restricted to allowed domains  
* Dependency scanning (`pip-audit`)  
* CI: pytest, ruff, black  
* No file I/O or `eval` in runtime

---

## 5. Delivery Checklist

1. `pytest -q` passes  
2. `uvicorn backend.app:app` serves `/docs` correctly  
3. Front‑end can generate problems, display 7 hints, print on one page  
4. A newcomer can reproduce the environment in ≤10 minutes following README
