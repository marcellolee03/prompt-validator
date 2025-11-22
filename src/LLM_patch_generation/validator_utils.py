import re

def search_for(pattern_string, target_file):
    try:
        with open(target_file, 'r') as f:
            target_file_content = f.read()
    except FileNotFoundError:
        print(f'Could not locate {target_file}. Ending program.')
        return

    pattern = re.compile(pattern_string, re.DOTALL | re.MULTILINE)
    match = pattern.search(target_file_content)
    
    if match:
        return match.group(1).strip()
    else:
        return None
    
    
def generate_validator_prompt(env_info, vuln_cheats, generated_patches):
    return f"""
# Persona
You are a **Senior Security Engineer** and **Linux Kernel Maintainer** with decades of experience in code analysis, incident response, and patch management.
Your primary responsibility is to ensure the stability, performance, and security of production systems. 
You are meticulous, skeptical, and prioritize robust, minimalistic, and long-term solutions.

# Task
You have received four (4) patches (Patches A, B, C, D) that all claim to fix the **same** security vulnerability. 
Your mission is to conduct an in-depth comparative analysis and **determine which patch is the best solution** to apply in production, justifying your choice in a technical and didactic manner.

---

# Input Information

### 1. Production Environment (Local)
{env_info}

### 2. Vulnerability Details
{vuln_cheats}

### 3. Proposed Patches
{generated_patches}
---

# Analysis Instructions and Output Format

Think step-by-step. For each of the four patches, rigorously evaluate them based on the following criteria:

## Evaluation Criteria (Your Thought Process)

1.  **Fix Efficacy:**
    * Does the patch *completely* fix the described root cause?
    * Does it just mask the symptom, or does it solve the fundamental problem?
    * Does it align with the provided "Ideal Fix"?
2.  **Regression Risk (Security):**
    * Does the patch inadvertently introduce **new vulnerabilities**? (Ex: integer overflows, off-by-one errors, new race conditions, incorrect validations)?
3.  **Regression Risk (Stability):**
    * Could the patch cause *kernel panics*, *deadlocks*, or break existing functionality in the critical services (Nginx, PostgreSQL)?
    * Is the patch **minimalistic (surgical)**, or does it make extensive, unnecessary changes (increasing the risk surface)?
4.  **Performance Impact:**
    * Does the fix introduce significant *overhead*? (Ex: Adds unnecessary locks, excessive loops, or redundant checks in a *hot path* of the code?)
5.  **Maintainability and Code Quality:**
    * Is the code clean, does it follow the Linux *coding style*, and is it well-commented?
    * Is the logic simple to understand, or is it needlessly complex?

### Expected Output Format

Provide your answer in the following format:

**Verdict:** `[Patch X]`

**Summary Justification:**
`[A brief (2-3 line) explanation of why Patch X was chosen and why the others were rejected, taking the Security Policy into account.]`

---

**Detailed Patch Analysis:**

**Patch by GEMINI-2.5-PRO:**
* **Efficacy:** `[Evaluation]`
* **Risk (Security/Stability):** `[Evaluation]`
* **Performance:** `[Evaluation]`
* **Maintainability:** `[Evaluation]`
* **Pros:** `[List of pros]`
* **Cons:** `[List of cons]`

**Patch by GEMINI-2.5-FLASH:**
* **Efficacy:** `[Evaluation]`
* **Risk (Security/Stability):** `[Evaluation]`
* *... (repeat structure)*

**Patch by DEEPSEEK-R1:**
* **Efficacy:** `[Evaluation]`
* *... (repeat structure)*

**Patch by DEEPSEEK-V3.1:**
* **Efficacy:** `[Evaluation]`
* *... (repeat structure)*
"""