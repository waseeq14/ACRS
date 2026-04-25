# ACRS — Automated Cyber Reasoning System

ACRS (Automated Cyber Reasoning System) is a Final Year Project (FYP) focused on automated vulnerability discovery, analysis, and remediation support for C/C++-oriented security workflows. The project combines static analysis, symbolic execution, fuzzing, and large language model (LLM) reasoning into a single research-oriented framework.

**Demonstration (YouTube):** https://youtu.be/ym0mpNBknpw

---

## 1. Project Overview

ACRS is designed as an automated vulnerability analysis and remediation framework that supports two complementary operating modes:

1. **Analysis Mode** (source-code driven)
2. **Pentesting Mode** (SSH-driven host assessment)

Rather than relying on a single detection technique, ACRS orchestrates multiple tools and reasoning stages to improve practical vulnerability triage and reporting.

---

## 2. Core Techniques and Tooling

The framework integrates the following major methods used throughout the project:

- **Semgrep static analysis** for pattern-based vulnerability discovery.
- **KLEE symbolic execution** for path exploration and bug-triggering inputs.
- **Segment-based symbolic execution** to focus symbolic analysis on vulnerable or suspicious regions.
- **AFL++ fuzzing** for coverage-guided dynamic testing.
- **AddressSanitizer (ASan)** for memory-safety crash detection during execution/fuzzing workflows.
- **LLM-based vulnerability reasoning** for contextual interpretation and prioritization.
- **LLM-based fuzzing seed generation** to improve fuzzing initialization.
- **LLM-based crash analysis** to translate crash artifacts into actionable explanations.
- **LLM-based patch generation** to propose remediation code and mitigation guidance.
- **SSH-based Pentesting Mode** for authorized remote host enumeration.
- **GTFOBins and Exploit-DB integration** for mapping findings to known exploitation techniques.

> **Research note:** Outputs are intended to assist analysts and students, not replace expert manual validation.

---

## 3. Operating Modes

### 3.1 Analysis Mode

Analysis Mode focuses on source-level and execution-level software assessment:

- Runs static checks using Semgrep rules.
- Performs symbolic execution with KLEE.
- Supports **segment-based symbolic execution** for targeted analysis.
- Executes AFL++ fuzzing and captures crash artifacts.
- Uses LLM components for:
  - reasoning over detected issues,
  - fuzzing seed generation,
  - crash interpretation,
  - patch and exploit-path assistance.

### 3.2 Pentesting Mode

Pentesting Mode targets authorized Linux systems over SSH:

- Connects to a host with provided credentials.
- Runs enumeration scripts (e.g., LinPEAS-based workflow).
- Classifies and summarizes discovered issues.
- References **GTFOBins** and **Exploit-DB** techniques for exploitability context.
- Generates exploit and patch-oriented recommendations for review.

---

## 4. Repository Structure

The following structure reflects the current repository layout:

```text
ACRS/
├── README.md
├── report-template.html
├── pentest-report-template.html
├── semgrep-rules/                 # Local Semgrep rule sets and examples
├── backend/
│   ├── manage.py                  # Django entry point
│   ├── requirements.txt           # Python dependencies
│   ├── backend/                   # Django project settings/urls
│   ├── api/                       # REST endpoints, models, report generation
│   ├── vulnerability_analysis/    # Analysis pipeline (Semgrep/KLEE/AFL/ASan/LLM)
│   └── pentest/                   # SSH pentesting helpers and scripts
└── frontend/
    ├── package.json               # React app scripts/dependencies
    ├── public/
    └── src/                       # UI routes/components for analysis & pentest flows
```

---

## 5. Setup

Because ACRS integrates multiple external security tools, environment configuration can vary by OS/distribution. The steps below are **typical setup instructions** based on repository files and may require path/tool adjustments.

### 5.1 Backend Setup (Django)

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Apply migrations and run the backend:

```bash
python manage.py migrate
python manage.py runserver
```

Default Django development server:

- Backend URL: `http://127.0.0.1:8000`

#### Database note

Current settings configure PostgreSQL by default (`fyp` database on localhost). If your local environment differs, update `backend/backend/settings.py` accordingly before running migrations.

#### Toolchain note

Analysis workflows may require local installations/paths for:

- `semgrep`
- `klee` / LLVM toolchain
- `afl-fuzz` (AFL++)
- ASan-capable compiler toolchain (e.g., `clang` with `-fsanitize=address`)

### 5.2 Frontend Setup (React)

```bash
cd frontend
npm install
npm start
```

Default frontend URL:

- Frontend URL: `http://localhost:3000`

The frontend is configured to communicate with the Django backend running locally.

---

## 6. Usage

### 6.1 Start services

Run backend and frontend in separate terminals.

**Terminal A (backend):**

```bash
cd backend
source .venv/bin/activate
python manage.py runserver
```

**Terminal B (frontend):**

```bash
cd frontend
npm start
```

### 6.2 Analysis workflow (typical)

1. Open the frontend dashboard.
2. Create/load a project and submit source code.
3. Execute vulnerability analysis stages (Semgrep / KLEE / advanced KLEE / fuzzer).
4. Review generated vulnerability, exploitability, and patch outputs.
5. Export/read generated reports from the reporting views.

### 6.3 Pentesting workflow (typical)

1. Open **Pentester Mode** in the frontend.
2. Provide authorized SSH target credentials.
3. Run enumeration and vulnerability analysis.
4. Review exploit suggestions and patch recommendations.

> Use Pentesting Mode only in legally authorized environments.

---

## 7. Outputs and Artifacts

ACRS generates both machine-readable and human-readable outputs during analysis and pentesting runs.

Common artifact categories include:

- **Static analysis findings** (Semgrep-derived issues and vulnerability descriptions).
- **Symbolic execution artifacts** from KLEE runs.
- **Segment-focused symbolic analysis outputs** from targeted path exploration.
- **Fuzzing artifacts** (AFL++ queues, crashes, fuzzer stats, and related metadata).
- **Crash analysis summaries** including LLM-assisted interpretation.
- **Patch and exploit-path suggestions** for remediation/security review.
- **Generated reports** using HTML templates and API report endpoints.

Output locations and filenames can vary by run mode and execution context.

---

## 8. Ethical Use / Disclaimer

ACRS is intended for:

- academic research,
- controlled cybersecurity experimentation,
- and authorized security testing.

Do **not** use this project against systems, applications, or networks without explicit permission.

The project may produce false positives/negatives and generated patches/exploit paths should be validated by qualified reviewers before operational use.

---

## 9. Authors

- Waseeq Ur Rehman — FA21 BCT 021
- Abdullah bin Aamir — FA21 BCT 002
- Adil Sheikh — FA21 BCT 001

Final Year Project, BS Cyber Security, COMSATS University Islamabad.

---

## 10. Acknowledgements

This project uses Semgrep rules from:

- https://github.com/0xdea/semgrep-rules

All credit for those rules belongs to the original author/maintainers.
