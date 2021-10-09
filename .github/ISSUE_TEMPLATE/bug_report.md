---
name: Bug report
about: Report a crash or nonsensical description
title: ''
labels: bug
assignees: ''

---

**Describe the bug**
A clear and concise description of what the bug is.

**Offending instruction information**
With the instruction that causes the bug selected, please run the following commands in the Binary Ninja console and paste the output:
```
from binja_explain_instruction import debug_instruction
debug_instruction(bv, here)
```

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Platform Information (please complete the following information):**
 - Binary Ninja Version: [e.g. Dev 2.4.2487]
 - OS: [e.g. Ubuntu Linux]
 - Python Interpreter [e.g. System Python 3.8]

**Additional context**
Add any other context about the problem here.
