# LANE-1 — Canonical 10 Clean Code principles (Facet A backbone)

- **Task:** t_b90c7846 (RESEARCH-clean-code-ai-agents [LANE-1])
- **Lane scope:** Establish the canonical 10 Clean Code principles (Facet A — the backbone of the whole research). For EACH of the 10: name, one-line definition, and HOW IT WORKS IN PRACTICE (a concrete, real-world example of what a developer actually does). Verify and refine the shared anchor list against primary sources; note any primary-source divergence as a finding (no silent substitution).
- **Source types owned:** official/authoritative software-engineering references — Robert C. Martin "Clean Code" (2008) and "Clean Architecture" (2017), Uncle Bob's blog (butunclebob.com), "The Pragmatic Programmer" (Hunt & Thomas), "Code Complete" (McConnell), "Refactoring" (Fowler), Wikipedia "Clean code" / "SOLID", authoritative book summaries.
- **Language:** English (verbatim quotes in the original language).
- **Date of research:** 2026-10-17.
- **Tier scheme:** **Verified** (authoritative source for this exact target, actually read) / **Plausible** (sound general behavior, not demonstrated on-target) / **Speculative** (mechanism asserted, untested).
  - Sub-distinction used here: **Verified (text read)** = verbatim body text of the primary source was read in this lane. **Verified (TOC)** = the chapter/section was confirmed to exist in the authoritative publisher/Library-of-Congress table of contents, but its body text was NOT read in this lane (the sample PDF only ships Chapter 1 body).

> **Headline finding (read this first):** There is **no single primary source that lists exactly "the 10 Clean Code principles."** The shared anchor list is a **cross-source synthesis**: it takes the core of Robert C. Martin's *Clean Code* (2008) — whose Part I is organized into ~14 principle *chapters*, not a numbered "10" — and folds in **DRY, KISS, YAGNI** (from *The Pragmatic Programmer* / Extreme Programming) and **SOLID** (from Martin's 2000 paper / *Agile Software Development* 2003 / *Clean Architecture* 2017). Three of the ten anchor items (KISS, YAGNI, SOLID) are **not chapters in *Clean Code* at all**. The anchor list is a reasonable, widely-used consolidation — but it is a synthesis, not a quotation from one book. See §0 and the per-principle "provenance" notes.

---

## 0. Structural findings on the anchor list itself

**F0.1 — *Clean Code* (2008) has no "10 principles" list; Part I is organized into principle chapters.**
- Claim: The book's Part I ("The Principles of Clean Code") is a sequence of chapters — Clean Code, Meaningful Names, Functions, Comments, Formatting, Objects and Data Structures, Error Handling, Boundaries, Unit Tests, Classes, Systems, Emergence, Concurrency, Successive Refinement — plus case studies (JUnit Internals, Refactoring SerialDate) and a closing "Smells and Heuristics" chapter. It never presents a numbered "top 10."
- Source: https://www.informit.com/store/clean-code-a-handbook-of-agile-software-craftsmanship-9780132350884 (publisher InformIT/Pearson TOC) + https://catdir.loc.gov/catdir/toc/ecip0820/2008024750.html (Library of Congress TOC) + Pearson sample-pages PDF (book TOC).
- Quote (publisher TOC, abridged): "Chapter 1: Clean Code … Chapter 2: Meaningful Names … Chapter 3: Functions … Chapter 4: Comments … Chapter 5: Formatting … Chapter 6: Objects and Data Structures … Chapter 7: Error Handling … Chapter 8: Boundaries … Chapter 9: Unit Tests … Chapter 10: Classes … Chapter 11: Systems … Chapter 12: Emergence … Chapter 13: Concurrency … Chapter 14: Successive Refinement … Chapter 17: Smells and Heuristics."
- Tier: **Verified (text read)** — full publisher TOC + book TOC read.

**F0.2 — KISS, YAGNI, and SOLID are NOT chapters in *Clean Code* (2008); they come from other primary sources.**
- Claim: The anchor list's items 4 (KISS), 5 (YAGNI), and 6 (SOLID) have no dedicated chapter in *Clean Code*. KISS/YAGNI originate in *The Pragmatic Programmer* and Extreme Programming; SOLID originates in Martin's 2000 paper "Design Principles and Design Patterns" / *Agile Software Development* (2003) / *Clean Architecture* (2017). *Clean Code* only *references* SRP/OCP/DIP, deferring to the PPP book.
- Source: *Clean Code* Ch 1 "Prequel and Principles" (Pearson sample PDF, text read) + Wikipedia "SOLID" (text read) + *Clean Code* TOC (no KISS/YAGNI/SOLID chapters).
- Quote (*Clean Code* Ch 1, verbatim): "In this book you will find sporadic references to various principles of design. These include the Single Responsibility Principle (SRP), the Open Closed Principle (OCP), and the Dependency Inversion Principle (DIP) among others. **These principles are described in depth in PPP.**"
- Tier: **Verified (text read)**.

**F0.3 — The anchor list's #2 "Small functions / single responsibility" conflates two related-but-distinct ideas.**
- Claim: "Small functions" is a *Clean Code* Ch 3 topic (functions: "Small!", "Do One Thing", "One Level of Abstraction per Function"). "Single responsibility" (SRP) is a SOLID principle that applies to *classes* ("one reason for a class to change"). The book treats "Do One Thing" (function-level) and SRP (class-level) as related but distinct. Merging them into one anchor item is a reasonable shorthand but loses that distinction.
- Source: *Clean Code* Ch 3 TOC + Ch 10 TOC ("The Single Responsibility Principle") + Wikipedia "SOLID" (SRP definition).
- Quote (Wikipedia SOLID, SRP): "there should never be more than one reason for a class to change. In other words, every class should have only one responsibility."
- Tier: **Verified (text read)**.

**F0.4 — The anchor list's #6 "SOLID" is a meta-principle (5 sub-principles), structurally different from the other nine single principles.**
- Claim: SOLID bundles five separate OOP design principles (SRP, OCP, LSP, ISP, DIP) under one mnemonic. Counting it as "one" of the "10" is a convenience; strictly it is one category containing five.
- Source: Wikipedia "SOLID" (text read).
- Quote: "SOLID is a mnemonic acronym for five principles intended to make source code more understandable, flexible, and maintainable."
- Tier: **Verified (text read)**.

---

## 1. Principle 1 — Meaningful / descriptive naming

- **One-line definition:** Names (variables, functions, classes) should reveal intent, be unambiguous, distinguishable, and searchable.
- **How it works in practice:** A developer renames a cryptic `d` to `daysBetweenCreationAndModification`, so the meaning is visible at the call site without reading the body; avoids magic numbers and Hungarian notation; picks one word per concept; makes names searchable (a `grep` for the concept finds it).

**F1.1 — *Clean Code* Ch 2 "Meaningful Names" is the canonical home; the lead rule is "Use Intention-Revealing Names."**
- Claim: Naming is a dedicated, early chapter (Ch 2) in *Clean Code*, opened by "Use Intention-Revealing Names."
- Source: *Clean Code* publisher TOC (https://www.informit.com/store/clean-code-a-handbook-of-agile-software-craftsmanship-9780132350884) + book TOC (Pearson sample PDF).
- Quote (TOC): "Chapter 2: Meaningful Names … Use Intention-Revealing Names … Avoid Disinformation … Make Meaningful Distinctions … Use Pronounceable Names … Use Searchable Names … Avoid Encodings … Pick One Word per Concept … Don't Pun … Add Meaningful Context."
- Tier: **Verified (TOC)** — section names confirmed; Ch 2 body not read in this lane.

**F1.2 — Dave Thomas (quoted in *Clean Code* Ch 1): clean code "has meaningful names."**
- Claim: One of the six expert definitions of clean code in *Clean Code* Ch 1 explicitly lists meaningful names as a defining property.
- Source: *Clean Code* Ch 1 (Pearson sample PDF, text read).
- Quote (verbatim): "Clean code can be read, and enhanced by a developer other than its original author. It has unit and acceptance tests. **It has meaningful names.** It provides one way rather than many ways for doing one thing. It has minimal dependencies, which are explicitly defined, and provides a clear and minimal API."
- Tier: **Verified (text read)**.

**F1.3 — Ron Jeffries (quoted in *Clean Code* Ch 1): expressiveness "includes meaningful names."**
- Claim: XP co-founder Ron Jeffries ties clean code to expressiveness, which he says includes meaningful names, and notes he renames things repeatedly.
- Source: *Clean Code* Ch 1 (Pearson sample PDF, text read).
- Quote (verbatim): "Expressiveness to me includes meaningful names, and I am likely to change the names of things several times before I settle in. With modern coding tools such as Eclipse, renaming is quite inexpensive, so it doesn't trouble me to change."
- Tier: **Verified (text read)**.

**F1.4 — Concrete practice: intention-revealing, searchable, pronounceable names.**
- Claim: The practice is to choose names that state intent (not `d`, `data`, `info`), are searchable, and map one word to one concept.
- Source: *Clean Code* Ch 2 section names (TOC, F1.1) + F1.2/F1.3.
- Quote: (see F1.1 TOC: "Use Intention-Revealing Names … Use Searchable Names … Pick One Word per Concept").
- Tier: **Plausible** — the specific rename example (`d` → `daysBetweenCreationAndModification`) is the standard illustration of Ch 2; the section is confirmed to exist but its body was not read in this lane.

---

## 2. Principle 2 — Small functions / single responsibility

- **One-line definition:** Functions do one thing, are short, and stay at one level of abstraction; each class has one reason to change (SRP).
- **How it works in practice:** A developer keeps functions a handful of lines, each doing one thing at one level of abstraction; splits a 200-line function into small named sub-functions (Extract Method); ensures each class has a single responsibility so a change touches one place.

**F2.1 — Bjarne Stroustrup (quoted in *Clean Code* Ch 1): "Clean code does one thing well."**
- Claim: The C++ inventor's definition of clean code centers on single-minded focus.
- Source: *Clean Code* Ch 1 (Pearson sample PDF, text read).
- Quote (verbatim): "I like my code to be elegant and efficient. The logic should be straightforward to make it hard for bugs to hide, the dependencies minimal to ease maintenance, error handling complete according to an articulated strategy, and performance close to optimal so as not to tempt people to make the code messy with unprincipled optimizations. **Clean code does one thing well.**"
- Tier: **Verified (text read)**.

**F2.2 — Dave Thomas (quoted in *Clean Code* Ch 1): "one way rather than many ways for doing one thing."**
- Claim: Clean code provides a single, clear way to do one thing.
- Source: *Clean Code* Ch 1 (Pearson sample PDF, text read).
- Quote (verbatim): "It provides one way rather than many ways for doing one thing."
- Tier: **Verified (text read)**.

**F2.3 — *Clean Code* Ch 3 "Functions" is the canonical home: "Small!", "Do One Thing", "One Level of Abstraction per Function."**
- Claim: Function discipline is a dedicated chapter with these exact section headings.
- Source: *Clean Code* publisher TOC + book TOC (Pearson sample PDF).
- Quote (TOC): "Chapter 3: Functions … Small! … Do One Thing … One Level of Abstraction per Function … Reading Code from Top to Bottom: The Stepdown Rule … Have No Side Effects … Command Query Separation … Prefer Exceptions to Returning Error Codes … Don't Repeat Yourself."
- Tier: **Verified (TOC)** — section names confirmed; Ch 3 body not read in this lane.

**F2.4 — SRP (SOLID): "never be more than one reason for a class to change."**
- Claim: The class-level single-responsibility rule is the "S" in SOLID.
- Source: Wikipedia "SOLID" (text read), citing Martin, *Agile Software Development* (2003) p.95.
- Quote (verbatim): "The single-responsibility principle (SRP) states that there should never be more than one reason for a class to change. In other words, every class should have only one responsibility."
- Tier: **Verified (text read)**.

**F2.5 — Provenance note: "small functions" (Ch 3) and "single responsibility" (SRP) are related but distinct; the anchor merges them.**
- Claim: The anchor item #2 fuses a function-level rule (Clean Code Ch 3) with a class-level SOLID rule (SRP). Both are real and canonical, but they operate at different levels of the design.
- Source: F2.1–F2.4.
- Tier: **Verified (text read)** (finding).

**F2.6 — Concrete practice: Extract Method; keep functions short; one level of abstraction.**
- Claim: The everyday action is to break large functions into small named ones and keep each class single-purpose.
- Source: *Clean Code* Ch 3 TOC (F2.3) + Ron Jeffries (Ch 1, text read).
- Quote (Ron Jeffries, *Clean Code* Ch 1, verbatim): "If it's a method, I will always use the Extract Method refactoring on it, resulting in one method that says more clearly what it does, and some submethods saying how it is done."
- Tier: **Verified (text read)** for the Extract Method practice (Jeffries quote); the "handful of lines" sizing is **Plausible** (standard Ch 3 guidance, body not read).

---

## 3. Principle 3 — DRY (Don't Repeat Yourself)

- **One-line definition:** Every piece of knowledge/logic should have a single, unambiguous representation in the system; no duplication.
- **How it works in practice:** A developer spots the same validation/formatting logic in three places and extracts it into one shared function; keeps a config value in one place (single source of truth) instead of hard-coding it repeatedly.

**F3.1 — *The Pragmatic Programmer* (20th anniv., Topic 9 "DRY—The Evils of Duplication"): the canonical DRY definition.**
- Claim: The DRY principle is defined as a single authoritative representation of each piece of knowledge.
- Source: *The Pragmatic Programmer: Your Journey to Mastery*, 20th Anniversary Edition (Dave Thomas & Andy Hunt, 2019), Topic 9 (raw PDF, text read).
- Quote (verbatim): "We feel that the only way to develop software reliably, and to make our developments easier to understand and maintain, is to follow what we call the DRY principle: **Every piece of knowledge must have a single, unambiguous, authoritative representation within a system.**"
- Tier: **Verified (text read)**.

**F3.2 — *The Pragmatic Programmer*: DRY is about duplication of *knowledge/intent*, not just copy-paste.**
- Claim: DRY extends beyond duplicated code to duplicated intent expressed in different ways.
- Source: *The Pragmatic Programmer* 20th anniv., Topic 9 (raw PDF, text read).
- Quote (verbatim): "DRY is about the duplication of *knowledge,* of *intent.* It's about expressing the same thing in two different places, possibly in two totally different ways."
- Tier: **Verified (text read)**.

**F3.3 — Ron Jeffries (quoted in *Clean Code* Ch 1, Beck's rules of simple code): "Contains no duplication."**
- Claim: Duplication-free is one of the four rules of simple code in *Clean Code* Ch 1.
- Source: *Clean Code* Ch 1 (Pearson sample PDF, text read).
- Quote (verbatim): "In priority order, simple code: Runs all the tests; **Contains no duplication**; Expresses all the design ideas that are in the system; Minimizes the number of entities such as classes, methods, functions, and the like."
- Tier: **Verified (text read)**.

**F3.4 — *Clean Code* also has dedicated DRY sections (Ch 3 "Don't Repeat Yourself", Ch 12 "No Duplication").**
- Claim: DRY appears as a named section in both the Functions chapter and the Emergence chapter.
- Source: *Clean Code* publisher TOC + book TOC.
- Quote (TOC): "Chapter 3 … Don't Repeat Yourself" / "Chapter 12: Emergence … No Duplication … Expressive … Minimal Classes and Methods."
- Tier: **Verified (TOC)**.

**F3.5 — Concrete practice: extract shared logic; single source of truth.**
- Claim: The everyday action is to pull repeated logic into one function and keep each fact in one place.
- Source: F3.1–F3.4.
- Tier: **Plausible** (standard application of the verified definitions).

---

## 4. Principle 4 — KISS (Keep It Simple, Stupid)

- **One-line definition:** Prefer the simplest solution that works; avoid unnecessary complexity.
- **How it works in practice:** A developer picks a plain function + a simple query over a heavyweight framework/design pattern when the simple approach already works; resists adding abstractions, layers, or configuration that no current requirement needs.

**F4.1 — Grady Booch (quoted in *Clean Code* Ch 1): "Clean code is simple and direct."**
- Claim: Simplicity is a defining property of clean code per the UML author.
- Source: *Clean Code* Ch 1 (Pearson sample PDF, text read).
- Quote (verbatim): "Clean code is simple and direct. Clean code reads like well-written prose. Clean code never obscures the designer's intent but rather is full of crisp abstractions and straightforward lines of control."
- Tier: **Verified (text read)**.

**F4.2 — KISS = "Keep It Simple, Stupid"; origin attributed to the U.S. Navy / Kelly Johnson (Lockheed Skunk Works), ~1960.**
- Claim: KISS predates software; it is a general engineering maxim popularized in programming by *The Pragmatic Programmer*.
- Source: boldare.com "KISS, YAGNI, DRY" (secondary, text read) + henriquesd.com (secondary, text read).
- Quote (boldare.com, verbatim): "It was actually first noted in the U.S. Navy in 1960. And the idea that it's generally more effective to keep things simple rather than complex, is much older."
- Tier: **Plausible** — secondary sources; the precise origin (Kelly Johnson / Lockheed Skunk Works vs. U.S. Navy) is debated across references, so the exact attribution is not pinned to a single primary source here.

**F4.3 — Provenance note: KISS is NOT a chapter in *Clean Code* (2008); its canonical home is *The Pragmatic Programmer* (1st ed., Ch 11 "Simple Design").**
- Claim: *Clean Code* has no KISS chapter; the principle is carried by the Pragmatic Programmer and general engineering culture.
- Source: *Clean Code* TOC (no KISS chapter) + *Pragmatic Programmer* 20th anniv. (restructured; KISS not a standalone topic in the 2019 edition).
- Tier: **Verified (TOC)** for the absence in *Clean Code*; the 1st-edition Ch 11 "Simple Design" placement is **Plausible** (1st-edition body not read in this lane).

**F4.4 — Concrete practice: choose the simplest working solution.**
- Claim: The everyday action is to default to the least-complex option that satisfies the requirement.
- Source: F4.1 + F4.2.
- Tier: **Plausible**.

---

## 5. Principle 5 — YAGNI (You Aren't Gonna Need It)

- **One-line definition:** Don't build functionality before it is actually needed; implement when the need is real, not foreseen.
- **How it works in practice:** A developer does not add an "export to PDF" button or a plugin architecture until a real requirement demands it; ships the minimal working version and adds capability only when a concrete need appears.

**F5.1 — YAGNI = "You Aren't Gonna Need It"; a principle from Extreme Programming (XP).**
- Claim: YAGNI originates in XP and means not building unneeded features.
- Source: henriquesd.com "DRY, KISS & YAGNI" (secondary, text read).
- Quote (verbatim): "YAGNI stands for You Ain't Gonna Need It. It's a principle from software development methodology of Extreme Programming (XP). This principle says that you should not create features that it's not really necessary."
- Tier: **Plausible** (secondary source; the XP origin is well-established but not read from a primary XP text in this lane).

**F5.2 — Ron Jeffries (XP co-founder): implement only when actually needed.**
- Claim: The XP founder's formulation of YAGNI.
- Source: henriquesd.com (secondary, text read), attributing the quote to Ron Jeffries.
- Quote (verbatim): "Always implement things when you actually need them, never when you just foresee that you need them."
- Tier: **Plausible** (secondary attribution of a Jeffries quote).

**F5.3 — Ron Jeffries (quoted in *Clean Code* Ch 1, Beck's rules): "Minimizes the number of entities."**
- Claim: The YAGNI-adjacent rule in *Clean Code* Ch 1 is to minimize the number of classes/methods/functions.
- Source: *Clean Code* Ch 1 (Pearson sample PDF, text read).
- Quote (verbatim): "Minimizes the number of entities such as classes, methods, functions, and the like."
- Tier: **Verified (text read)**.

**F5.4 — Provenance note: YAGNI is NOT a chapter in *Clean Code* (2008); its canonical home is XP / *The Pragmatic Programmer*.**
- Claim: *Clean Code* has no YAGNI chapter; the principle is carried by XP and the Pragmatic Programmer.
- Source: *Clean Code* TOC (no YAGNI chapter).
- Tier: **Verified (TOC)** for the absence in *Clean Code*.

**F5.5 — Concrete practice: defer unneeded features until the need is concrete.**
- Claim: The everyday action is to ship minimal and add only on real demand.
- Source: F5.1–F5.3.
- Tier: **Plausible**.

---

## 6. Principle 6 — SOLID design (SRP, OCP, LSP, ISP, DIP)

- **One-line definition:** Five object-oriented design principles that make code more understandable, flexible, and maintainable.
- **How it works in practice:** A developer splits a "god class" (SRP), adds new behavior via a strategy/interface without editing existing code (OCP), keeps subclasses honoring the base contract (LSP), breaks a fat interface into role-specific ones (ISP), and depends on abstractions injected at runtime rather than concrete classes (DIP).

**F6.1 — SOLID = SRP, OCP, LSP, ISP, DIP; five principles for understandable/flexible/maintainable code.**
- Claim: SOLID is a mnemonic for five OOP design principles.
- Source: Wikipedia "SOLID" (text read).
- Quote (verbatim): "SOLID is a mnemonic acronym for five principles intended to make source code more understandable, flexible, and maintainable."
- Tier: **Verified (text read)**.

**F6.2 — SOLID was introduced by Robert C. Martin (2000 paper); the acronym was coined ~2004 by Michael Feathers.**
- Claim: Martin introduced the underlying principles; Feathers coined the "SOLID" acronym.
- Source: Wikipedia "SOLID" (text read).
- Quote (verbatim): "Robert C. Martin introduced the basic principles of SOLID design in his 2000 paper *Design Principles and Design Patterns* about software rot. The SOLID acronym was coined around 2004 by Michael Feathers."
- Tier: **Verified (text read)**.

**F6.3 — Provenance note: SOLID is NOT in *Clean Code* (2008); it is described in depth in *Agile Software Development* (2003) and *Clean Architecture* (2017).**
- Claim: *Clean Code* only references SRP/OCP/DIP and defers to the PPP book; the full treatment is in Martin's other works.
- Source: *Clean Code* Ch 1 "Prequel and Principles" (text read) + Wikipedia "SOLID" references (Martin 2003 PPP p.95; Martin 2018 *Clean Architecture* p.58; objectmentor.com per-principle PDFs).
- Quote (*Clean Code* Ch 1, verbatim): "These include the Single Responsibility Principle (SRP), the Open Closed Principle (OCP), and the Dependency Inversion Principle (DIP) among others. These principles are described in depth in PPP."
- Tier: **Verified (text read)**.

**F6.4 — The five principles' definitions.**
- Claim: Each SOLID letter has a standard one-line definition.
- Source: Wikipedia "SOLID" (text read), citing Martin's PPP (2003) p.95 and objectmentor.com PDFs.
- Quote (verbatim, per principle):
  - SRP: "there should never be more than one reason for a class to change."
  - OCP: "software entities should be open for extension, but closed for modification."
  - LSP: "functions that use pointers or references to base classes must be able to use pointers or references of derived classes without knowing it."
  - ISP: "clients should not be forced to depend upon interface methods that they do not use."
  - DIP: "one should depend upon abstractions, not concretes."
- Tier: **Verified (text read)**.

**F6.5 — Structural note: SOLID is a meta-principle (5 sub-principles), not a single principle like the other nine.**
- Claim: Counting SOLID as "one" of the "10" is a convenience; strictly it is one category containing five.
- Source: F6.1.
- Tier: **Verified (text read)** (finding).

**F6.6 — Concrete practice: apply the five principles at design time.**
- Claim: The everyday actions are the per-letter practices (split god classes, extend via interfaces, honor contracts, segregate interfaces, depend on abstractions / use DI).
- Source: F6.4.
- Tier: **Plausible** (standard application of the verified definitions).

---

## 7. Principle 7 — Error handling

- **One-line definition:** Handle errors completely and deliberately — prefer exceptions over error codes, never return or pass null, never ignore errors.
- **How it works in practice:** A developer throws a specific exception (`UserNotFoundException`) instead of returning `null` or a magic error code; writes the try/catch/finally first; provides context in the exception; and never swallows an exception silently.

**F7.1 — Bjarne Stroustrup (quoted in *Clean Code* Ch 1): "error handling complete according to an articulated strategy."**
- Claim: Complete, strategy-driven error handling is a defining property of clean code.
- Source: *Clean Code* Ch 1 (Pearson sample PDF, text read).
- Quote (verbatim): "…error handling complete according to an articulated strategy…" (within Bjarne's definition, see F2.1).
- Tier: **Verified (text read)**.

**F7.2 — *Clean Code* Ch 7 "Error Handling" is the canonical home: exceptions over return codes, no nulls.**
- Claim: Error handling is a dedicated chapter with these exact section headings.
- Source: *Clean Code* publisher TOC + book TOC.
- Quote (TOC): "Chapter 7: Error Handling … Use Exceptions Rather Than Return Codes … Write Your Try-Catch-Finally Statement First … Use Unchecked Exceptions … Provide Context with Exceptions … Define the Normal Flow … Don't Return Null … Don't Pass Null."
- Tier: **Verified (TOC)** — section names confirmed; Ch 7 body not read in this lane.

**F7.3 — Concrete practice: throw specific exceptions, no nulls, never ignore.**
- Claim: The everyday actions are to use exceptions (not error codes/nulls) and to handle every error path.
- Source: F7.1 + F7.2.
- Tier: **Plausible** (standard application of the verified chapter's stated rules).

---

## 8. Principle 8 — Unit testing / TDD

- **One-line definition:** Tests are first-class citizens; write them to drive development (TDD) and keep them small, fast, isolated, deterministic.
- **How it works in practice:** A developer writes a failing test first, then the minimal code to pass it, then refactors (red–green–refactor); keeps each test fast, independent, repeatable, self-validating, and timely (F.I.R.S.T.); uses one assert per test.

**F8.1 — Dave Thomas (quoted in *Clean Code* Ch 1): clean code "has unit and acceptance tests"; "Code, without tests, is not clean."**
- Claim: Tests are a defining property of clean code; code without tests is unclean.
- Source: *Clean Code* Ch 1 (Pearson sample PDF, text read).
- Quote (verbatim): "It has unit and acceptance tests." / "Dave ties cleanliness to tests! … Code, without tests, is not clean. No matter how elegant it is, no matter how readable and accessible, if it hath not tests, it be unclean."
- Tier: **Verified (text read)**.

**F8.2 — *Clean Code* Ch 9 "Unit Tests" is the canonical home: "The Three Laws of TDD", "F.I.R.S.T."**
- Claim: Unit testing / TDD is a dedicated chapter with these exact section headings.
- Source: *Clean Code* publisher TOC + book TOC.
- Quote (TOC): "Chapter 9: Unit Tests … The Three Laws of TDD … Keeping Tests Clean … Clean Tests … One Assert per Test … Single Concept per Test … F.I.R.S.T."
- Tier: **Verified (TOC)** — section names confirmed; Ch 9 body not read in this lane.

**F8.3 — F.I.R.S.T. = Fast, Independent, Repeatable, Self-validating, Timely.**
- Claim: The F.I.R.S.T. acronym (a *Clean Code* Ch 9 section) expands to these five test qualities.
- Source: *Clean Code* Ch 9 TOC (F8.2) + standard expansion.
- Tier: **Plausible** — the acronym is confirmed in the TOC; the letter-by-letter expansion is the standard one but the Ch 9 body was not read in this lane.

**F8.4 — Concrete practice: red–green–refactor; one assert per test.**
- Claim: The everyday action is to write the failing test first, then minimal code, then refactor; keep tests isolated and deterministic.
- Source: F8.1 + F8.2.
- Tier: **Plausible** (standard application of the verified chapter's stated rules).

---

## 9. Principle 9 — Refactoring / Boy Scout Rule

- **One-line definition:** Continuously improve design without changing behavior; leave the code cleaner than you found it.
- **How it works in practice:** While fixing a bug, a developer also renames a confusing variable and extracts a small method — a small, behavior-preserving cleanup each time they touch code, so the codebase trends cleaner over time.

**F9.1 — *Clean Code* Ch 1 "The Boy Scout Rule": "Leave the campground cleaner than you found it."**
- Claim: The Boy Scout Rule is stated explicitly in *Clean Code* Ch 1.
- Source: *Clean Code* Ch 1 (Pearson sample PDF, text read).
- Quote (verbatim): "The Boy Scouts of America have a simple rule that we can apply to our profession. **Leave the campground cleaner than you found it.**"
- Tier: **Verified (text read)**.

**F9.2 — *Clean Code* Ch 1: the cleanup is small and incremental.**
- Claim: The rule is about tiny, per-check-in improvements, not big rewrites.
- Source: *Clean Code* Ch 1 (Pearson sample PDF, text read).
- Quote (verbatim): "If we all checked-in our code a little cleaner than when we checked it out, the code simply could not rot. The cleanup doesn't have to be something big. Change one variable name for the better, break up one function that's a little too large, eliminate one small bit of duplication, clean up one composite if statement."
- Tier: **Verified (text read)**.

**F9.3 — Refactoring as a practice: *Clean Code* Ch 14 "Successive Refinement" + Ch 16 "Refactoring SerialDate" ("First, Make It Work / Then Make It Right").**
- Claim: Refactoring is a first-class theme in *Clean Code* (a dedicated case-study chapter on refactoring SerialDate, plus successive refinement).
- Source: *Clean Code* publisher TOC + book TOC.
- Quote (TOC): "Chapter 14: Successive Refinement … Chapter 16: Refactoring SerialDate … First, Make It Work … Then Make It Right."
- Tier: **Verified (TOC)**.

**F9.4 — Martin Fowler's *Refactoring* is the canonical standalone refactoring reference (code smells → transformations).**
- Claim: Fowler's *Refactoring* is the standard reference for behavior-preserving transformations; it is the natural companion to the Boy Scout Rule.
- Source: general SE canon (not read in this lane).
- Tier: **Plausible** — Fowler's *Refactoring* is the universally-cited reference, but its text was not read in this lane.

**F9.5 — Concrete practice: leave it cleaner; behavior-preserving transformations.**
- Claim: The everyday action is a small cleanup on every touch, using refactors (rename, extract method, inline) that don't change behavior.
- Source: F9.1 + F9.2 + F9.3.
- Tier: **Verified (text read)** for the Boy Scout Rule practice; the specific Fowler transformations are **Plausible**.

---

## 10. Principle 10 — Readability & maintainability

- **One-line definition:** Code is read far more than it is written; write it to be read by humans (consistency, formatting, review).
- **How it works in practice:** A developer follows the team's formatting/style guide, writes code that reads like prose, and gets it peer-reviewed — because the people who maintain it (often not the author) will read it many times.

**F10.1 — *Clean Code* Ch 1 "We Are Authors": "the ratio of time spent reading vs. writing is well over 10:1."**
- Claim: Reading dominates writing by an order of magnitude — the core argument for readability.
- Source: *Clean Code* Ch 1 (Pearson sample PDF, text read).
- Quote (verbatim): "You get the drift. Indeed, the ratio of time spent reading vs. writing is well over 10:1. We are constantly reading old code as part of the effort to write new code."
- Tier: **Verified (text read)**.

**F10.2 — *Clean Code* Ch 1: "if you want your code to be easy to write, make it easy to read."**
- Claim: Readability is what makes code fast to change.
- Source: *Clean Code* Ch 1 (Pearson sample PDF, text read).
- Quote (verbatim): "So if you want to go fast, if you want to get done quickly, if you want your code to be easy to write, make it easy to read."
- Tier: **Verified (text read)**.

**F10.3 — Grady Booch (quoted in *Clean Code* Ch 1): "Clean code reads like well-written prose."**
- Claim: Readability is a defining property of clean code.
- Source: *Clean Code* Ch 1 (Pearson sample PDF, text read).
- Quote (verbatim): "Clean code reads like well-written prose."
- Tier: **Verified (text read)**.

**F10.4 — *Clean Code* Ch 5 "Formatting" + Ch 17 "Smells and Heuristics" support readability/maintainability.**
- Claim: Formatting (vertical/horizontal, team rules) and the smells/heuristics catalog are the book's readability/maintainability machinery.
- Source: *Clean Code* publisher TOC + book TOC.
- Quote (TOC): "Chapter 5: Formatting … The Purpose of Formatting … Vertical Formatting … Horizontal Formatting … Team Rules … Uncle Bob's Formatting Rules" / "Chapter 17: Smells and Heuristics … Comments … Functions … General … Names … Tests."
- Tier: **Verified (TOC)**.

**F10.5 — Concrete practice: consistent formatting, code that reads like prose, peer review.**
- Claim: The everyday actions are to follow a shared style, write readable code, and review it.
- Source: F10.1–F10.4.
- Tier: **Plausible** (standard application of the verified arguments).

---

## 11. Searched, found nothing (evidence of absence)

- **A single primary source listing exactly "the 10 Clean Code principles"** — none found. *Clean Code* (2008) is chapter-organized, not a numbered "10"; the "10" is a community synthesis. (This is a positive finding, not a gap — see F0.1.)
- ***Clean Code* Chapter 2/3/7/9 body text** — the Pearson sample-pages PDF ships only **Chapter 1 body** (plus full TOC + index). The section names for Ch 2 (Meaningful Names), Ch 3 (Functions), Ch 7 (Error Handling), Ch 9 (Unit Tests) were confirmed via the authoritative publisher/LOC TOC, but the body text of those chapters was NOT read in this lane. → Per-section practice details for naming/functions/error-handling/TDD are tiered **Plausible** (or **Verified (TOC)** for section existence), not **Verified (text read)**.
- ***The Pragmatic Programmer* 1st edition (1999) KISS / YAGNI / Boy Scout chapter body** — the freely-available 20th-anniversary (2019) edition **restructured** the book into "Topics" and dropped the standalone "KISS", "YAGNI", and "Boy Scout Rule" chapter titles (Boy Scout appears only in a "situational awareness" aside). The 1st-edition Ch 11 "Simple Design" body (classic KISS/YAGNI/Boy Scout text) was NOT read in this lane. → KISS/YAGNI are sourced via secondary references (Plausible) + *Clean Code* Ch 1 adjacent quotes (Verified).
- ***Code Complete* (McConnell) and *Refactoring* (Fowler) primary text** — not read in this lane. They are standard references (Fowler for refactoring, McConnell for naming/functions), but this lane relied on *Clean Code* + *Pragmatic Programmer* + Wikipedia for the core. → Fowler/McConnell claims are tiered **Plausible**.
- **Uncle Bob's blog (butunclebob.com) specific posts** — the InformIT page lists "Clean Code Tip of the Week" articles (e.g., #2 Inverse Scope Law of Function Names, #10 Avoid Too Many Arguments, #12 Eliminate Boolean Arguments) and "What Is Clean Code?", but none were extracted in this lane. → Not used as a citation here.
- **A definitive single origin for KISS** — references disagree (U.S. Navy 1960 vs. Kelly Johnson / Lockheed Skunk Works). → KISS origin left at **Plausible** with the disagreement noted (F4.2).

---

## 12. Source-universe checklist (coverage)

| Source type | Status |
|---|---|
| Official/authoritative — *Clean Code* (2008) | **Covered** — full publisher (InformIT/Pearson) TOC + LOC TOC + book TOC + **Chapter 1 body read** (Pearson sample PDF). Ch 2/3/7/9 body NOT read (sample ships Ch 1 only). |
| Official/authoritative — *Clean Architecture* (2017) | **Cited, not read** — referenced via Wikipedia SOLID (p.58) for SOLID provenance; body not read in this lane. |
| Official/authoritative — *The Pragmatic Programmer* | **Covered (20th anniv.)** — Topic 9 "DRY" body read (raw PDF). 1st-edition KISS/YAGNI/Boy Scout body NOT read (restructured in 2019 ed). |
| Official/authoritative — *Agile Software Development* (PPP, 2003) | **Cited, not read** — referenced via Wikipedia SOLID (p.95) + *Clean Code* Ch 1 for SRP/OCP/DIP provenance. |
| Semi-official — Wikipedia "SOLID" | **Covered** — full article read (5 principles + Martin 2000 paper / Feathers 2004 acronym + PPP/Clean Architecture/objectmentor.com citations). |
| Semi-official — Wikipedia "Clean code" | **Skipped (reason)** — the *Clean Code* book + TOC is the stronger primary source; the Wikipedia "Clean code" article was not needed once the book TOC + Ch 1 were read. |
| Community — Uncle Bob's blog (butunclebob.com) | **Skipped (reason)** — the book itself (primary) was read directly; blog "Tip of the Week" posts are derivative of the book and not needed for the backbone. |
| Code (GitHub) | **N/A** — not applicable to a principles-research lane. |
| Practice — authoritative book summaries / secondary articles | **Covered** — henriquesd.com + boldare.com (KISS origin, YAGNI/XP, Ron Jeffries quote) used as secondary citations (Plausible). |
| Upstream | **N/A** — no wrapped-engine dimension for this topic. |

---

## 13. Synthesis summary table (for the collector / Facet A backbone)

| # | Principle | One-line definition | Canonical primary source | How it works in practice (concrete) | Strongest quote (tier) |
|---|---|---|---|---|---|
| 1 | Meaningful naming | Names reveal intent; unambiguous, distinguishable, searchable | *Clean Code* Ch 2 | Rename `d` → `daysBetweenCreationAndModification`; one word per concept | "It has meaningful names." — Dave Thomas in *Clean Code* Ch 1 (Verified, text read) |
| 2 | Small functions / SRP | Functions do one thing, short, one abstraction level; one reason for a class to change | *Clean Code* Ch 3 + SOLID SRP | Extract Method; split god classes | "Clean code does one thing well." — Bjarne in *Clean Code* Ch 1 (Verified, text read) |
| 3 | DRY | Single unambiguous representation of each piece of knowledge | *Pragmatic Programmer* Topic 9 | Extract shared logic; single source of truth | "Every piece of knowledge must have a single, unambiguous, authoritative representation within a system." (Verified, text read) |
| 4 | KISS | Simplest solution that works | *Pragmatic Programmer* (1st ed) / US Navy origin | Pick plain function over heavyweight pattern | "Clean code is simple and direct." — Booch in *Clean Code* Ch 1 (Verified, text read); KISS origin (Plausible) |
| 5 | YAGNI | Don't build until actually needed | XP / *Pragmatic Programmer* | Ship minimal; add on real demand | "Minimizes the number of entities…" — Ron Jeffries in *Clean Code* Ch 1 (Verified, text read); Jeffries YAGNI quote (Plausible) |
| 6 | SOLID (SRP/OCP/LSP/ISP/DIP) | 5 OOP design principles for flexible, maintainable code | Martin 2000 paper / PPP 2003 / Clean Architecture 2017 | Split god class; extend via interface; DI | "…open for extension, but closed for modification." (OCP) — Wikipedia SOLID (Verified, text read) |
| 7 | Error handling | Complete, deliberate; exceptions over codes; no nulls | *Clean Code* Ch 7 | Throw `UserNotFoundException`; never return null | "error handling complete according to an articulated strategy" — Bjarne in *Clean Code* Ch 1 (Verified, text read) |
| 8 | Unit testing / TDD | Tests first-class; drive development; F.I.R.S.T. | *Clean Code* Ch 9 | Red–green–refactor; one assert per test | "Code, without tests, is not clean." — Dave Thomas in *Clean Code* Ch 1 (Verified, text read) |
| 9 | Refactoring / Boy Scout Rule | Improve design without changing behavior; leave it cleaner | *Clean Code* Ch 1 + Ch 14/16; Fowler *Refactoring* | Small behavior-preserving cleanup each touch | "Leave the campground cleaner than you found it." — *Clean Code* Ch 1 (Verified, text read) |
| 10 | Readability & maintainability | Code read ≫ written; write to be read by humans | *Clean Code* Ch 1 "We Are Authors" + Ch 5/17 | Team style guide; code reads like prose; peer review | "the ratio of time spent reading vs. writing is well over 10:1" — *Clean Code* Ch 1 (Verified, text read) |

**Key caveats for downstream (Facet B — AI agents) lanes:**
1. The "10" is a **synthesis**, not a single book's list — if a downstream lane needs a defensible "canonical 10," cite *Clean Code* (2008) Part I as the backbone and note KISS/YAGNI (Pragmatic Programmer/XP) + SOLID (Martin PPP/Clean Architecture) as the cross-source additions.
2. **Verified (text read)** vs **Verified (TOC)**: only *Clean Code* Ch 1 body, *Pragmatic Programmer* Topic 9 (DRY) body, and Wikipedia SOLID were read as body text. Ch 2/3/7/9 of *Clean Code* are confirmed by TOC only — their per-section practice details are Plausible.
3. KISS origin (Navy vs. Kelly Johnson) and the exact 1st-edition KISS/YAGNI/Boy Scout wording remain **Plausible** — flagged for any lane that needs them pinned to a primary source.
