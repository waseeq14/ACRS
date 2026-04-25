# ACRS — Automated Cyber Reasoning System

*ACRS* is a Final Year Project that combines different security analysis techniques into one automated framework.  
It is designed to *find vulnerabilities, generate exploits, and even provide mitigation steps* — making it useful for both offensive and defensive security research.

Demonstration: https://youtu.be/ym0mpNBknpw
---

## 🚀 Project Overview

ACRS integrates *static analysis, symbolic execution, fuzzing, and LLMs* into one pipeline.  
The system works in two main modes:

•⁠  ⁠*Analysis Mode:*  
  - Scans source code for vulnerabilities using Semgrep.  
  - Runs symbolic execution with KLEE (both on full programs and isolated vulnerable segments).  
  - Performs fuzzing with AFL++ to trigger crashes.  
  - Uses LLMs to prioritize paths, generate fuzzing seeds, and analyze crashes.  
  - Produces proof-of-concept exploits and patch suggestions.

•⁠  ⁠*Pentesting Mode:*  
  - Connects to a live Linux system over SSH.  
  - Enumerates system information, misconfigurations, and SUID/SGID binaries.  
  - Looks up exploitation techniques from GTFOBins and Exploit-DB.  
  - Simulates exploits safely and provides patch recommendations.  

---

## 🔑 Key Features

•⁠  ⁠Hybrid pipeline: *Static → Symbolic → Fuzzing*.  
•⁠  ⁠*LLM-guided orchestration* for better path selection and fuzzing seeds.  
•⁠  ⁠*Segment-based symbolic execution* to speed up and focus on likely vulnerable code areas.  
•⁠  ⁠*Automated crash analysis* with exploit and patch generation.  
•⁠  ⁠*Live pentesting mode* for safe exploitation and remediation guidance.  
•⁠  ⁠Generates both *machine-readable reports* (JSON) and *human-readable summaries* (HTML).  

---

## 🛠️ Architecture

Source Code ├─ Semgrep → suspicious patterns ├─ KleeProcessor2 → extract segments │     └─ KLEE → symbolic exploration ├─ LLM → path prioritization + seed generation ├─ AFL++ → fuzzing + crashes └─ Crash Analyzer (LLM) → PoCs + patches

Pentesting Mode SSH Target → Enumeration → Vulnerability Classification → Exploit Simulation → Patch Suggestions

---

## 📂 Outputs

Each run produces:

•⁠  ⁠⁠ semgrep.json ⁠ → static analysis results  
•⁠  ⁠⁠ klee_full/ ⁠ → full-program symbolic execution results  
•⁠  ⁠⁠ klee_segments/ ⁠ → segment-based results  
•⁠  ⁠⁠ afl/ ⁠ → fuzzing logs, crashes, queue  
•⁠  ⁠⁠ crash_analysis/ ⁠ → exploit drafts and patch notes  
•⁠  ⁠⁠ reports/ ⁠ → final summarized report  

---

## 🎯 Example Use Cases

•⁠  ⁠*Researchers* → run deep analysis on codebases.  
•⁠  ⁠*Red Teamers* → quickly find and simulate exploits.  
•⁠  ⁠*Blue Teamers* → get patch recommendations and hardening guidance.  
•⁠  ⁠*CI/CD Pipelines* → integrate automated vulnerability detection into development workflow.  

---

## ⚙️ Deployment & Running
 
Instructions for deploying and running ACRS are **under development**.  
Since the project integrates multiple tools (Semgrep, KLEE, AFL++, LLMs, etc.), it requires careful environment setup and configuration.  
A step-by-step deployment guide will be added soon.

---

## 📌 Notes

•⁠  ⁠ACRS is for *educational and authorized security testing only*.  
•⁠  ⁠Pentesting mode should only be used on systems you own or have explicit permission to test.  
•⁠  ⁠The system is modular: rules, harnesses, and models can be swapped or extended.  

---

## 👤 Authors

Waseeq Ur Rehman - FA21 BCT 021
Abdullah bin Aamir - FA21 BCT 002
Adil Sheikh - FA21 BCT 001
Final Year Project 
BS CyberSec. 
Comsats University Islamabad

## Acknowledgements

This project uses Semgrep rules from:
- https://github.com/0xdea/semgrep-rules

All credit for the rules goes to the original author.
---
