# CareHub Data Engineering Technical Assessment

**Time:** ~1 Hour
**Tools:** Use whatever you'd normally use -- your IDE, AI assistants, documentation, Google, anything you might normally use.

## Background

You're joining a healthcare data team that migrates patient records from legacy EHR systems into a modern platform. We onboard 3-7 new organizations per month. The incoming data is structurally similar across orgs (patients, encounters, medications) but each org exports it differently: different file formats, column names, date conventions, status labels.

**Your project:** Create an ETL pipeline following medallion architecture (bronze/silver layers).

## The Data

In the `input_data_v2/` folder you'll find data from **two organizations**:

**Org A (Springfield PACE):**

- `patients.csv` - Patient demographics
- `encounters.csv` - Clinical encounters / visits

**Org B (Chicago PACE):**

- `patients_org_b.csv` - Same data, different column names
- `encounters_org_b.csv` - Same data, different column names

Different column names (`birth_date` vs `DateOfBirth`, `encounter_id` vs `EncounterID`), different formats. This is realistic. It is useful to note that while these 2 organizations have different column names, in general, an organization's data is consistent based on the system they are migrating from.

This means that all organizations migrating from Competitor_1 will usually have ~90-100% same schema as other organizations migrating from that competitor.

## Context: Why Medallion Architecture?

We get questions like:

- "How many Annual-Assessment encounters were in the source file for this patient?" → **Need to be able to query bronze table for that patient**
- "Can you reprocess with updated logic?" → **Need Bronze raw date, need records connecting target system with source records**
- "How many records failed validation?" → **Need quality checks between layers**

**Medallion approach:**

- **Bronze** = Preserve exact source data as received
- **Silver** = Cleaned, validated, standardized, ready for API/webapp

## Before You Start

Take 2-3 minutes to **explore the `input_data_v2/` folder**. Look at the files, understand the structure.

---

## Part 1: Architecture Design (10-20 min)

Design the bronze and silver layers for our medallion architecture. These decisions are interconnected - your bronze choices will influence what makes sense for silver.

**Background:**

- 2 orgs today, onboarding 3-7 new orgs per month
- Each org has different column names, formats, conventions (explore `input_data_v2/` to see examples)
- Multiple data domains: patients, encounters, medications, providers, facilities
- Need to scale to 50+ orgs over time

---

### Task 1: Bronze Layer Architecture

**Purpose of Bronze:**

- Preserve raw source data as received (audit trail)
- Enable reprocessing without asking clients for files again
- We're often asked to query original source data: "What did the source file say for patient X's enrollment status?"
- Track data quality metrics - Compare source row counts (bronze) to clean row counts (silver) to measure validation pass rates, identify problematic data sources, and monitor data quality per org
- Queries like "how many encounters of this type were in the source data"

**Design Challenge:**

How would you structure your bronze tables/dbs to handle these use cases?

**What to consider:**

- How are you going to structure your bronze tables/dbs
- Do you put data from different _organizations_ in the same table(s) vs separated?
- Do you put data from different _data domains_ in the same table(s) vs separated?
- Explicit columns vs Variant (Snowflake) or JSON?
- What metadata would you add to records in Bronze tables if any?
- Do you make changes like converting strings of dates to DATE format?
- Are there any tradeoffs and scalability considerations of these decisions

---

### Task 2: Silver Layer Architecture

**Purpose of Silver:**

- Cleaned, standardized data ready for API/webapp
- Same schema across all orgs (no org-specific differences)
- Support both cross-org queries AND org-specific operations
- Support adding new domains from Bronze --> Silver as we make improvements to migrate more domains
- Support reporting metrics on data flowing from Bronze
- Allow reloading/reprocessing individual orgs
- Use as cleaned data to load from Silver into target systems (like our web application)

**Design Challenge:**

How would you structure silver to handle these use cases?

**What to consider:**

- Table structure and naming
- How it relates to your bronze design
- How you handle org isolation vs cross-org queries
- How you organize data across domains
- Any metadata you might add and why
- Tradeoffs and reasoning

---

### Deliverable for Part 1:

Write down your architecture (markdown file, text doc, or code comments) covering:

- **Bronze architecture**: Table structure, how you handle schema differences, scalability
- **Silver architecture**: Table structure, relationship to bronze, query patterns
- **Reasoning**: Tradeoffs and why you made these choices

Feel free to pause, talk things out, and ask questions at any point.

_Tip: Think holistically. For example, if you make a certain decision for bronze, how does that influence your silver design? Consider the system as a whole, not isolated decisions._

---

## Part 2: Implement Silver Transformation (30-35 min)

Now implement the transformation from bronze to silver. In Part 1 you designed the architecture - now you'll build it.

## AI Usage Policy

**You may use AI assistants** for:

- Looking up syntax and library documentation
- Debugging specific errors
- Understanding error messages
- Code completion and autocomplete

**Please don't use AI** to:

- Generate entire solution architectures
- Write complete implementations from the README
- Design your config structure

### What You'll Get:

We'll give you **pre-loaded bronze data** (CSVs representing bronze tables). The data is already in bronze - you focus on transforming it to silver.

### Target Silver Schema

Your transformation must produce this standardized schema:

```sql
-- Silver patients table
patient_id          STRING      -- Unique patient identifier
first_name          STRING      -- Patient first name
last_name           STRING      -- Patient last name
date_of_birth       DATE        -- YYYY-MM-DD format
gender              STRING      -- Enum: 'M', 'F', 'Other'
enrollment_status   STRING      -- Enum: 'Active', 'Inactive', 'Prospect', 'Deceased'
phone               STRING      -- Standardized format (your choice)
loaded_at           TIMESTAMP   -- When loaded to silver
org_id              STRING      -- Organization identifier (if multi-tenant silver)
```

**Value mappings you need to handle:**

- **gender**: Male/Female → M/F, handle case variations (MALE, male, etc. - more variations may come in the future)
- **enrollment_status**: Enrolled → Active, Disenrolled → Inactive
- **dates**: Multiple formats (YYYY-MM-DD, MM/DD/YYYY, YYYYMMDD) → YYYY-MM-DD

### Your Task:

Build a transformation pipeline that can be used to populate silver tables:

1. **Reads from bronze** (based on your architecture from Part 1)

2. **Maps columns** - Different orgs have different column names:
   - Springfield: `PatientID`, `FirstName`, `Sex`, `ProgramStatus`
   - Chicago: `patient_id`, `first_name`, `gender`, `enrollment_status`
   - Your code should handle this via org _configs_ as appropriate

3. **Normalizes values** - Different orgs use different conventions:
   - Format Date of Birth as date if possible
   - Format strings into the enum options

4. **Decide how to handle bad records**: Skip? Quarantine table? Flag in silver? Your choice - but explain your reasoning. If short on time, write TODOs in place of coding.

5. **Make it scalable** - Adding Org C next month should require:
   - Minimal changes to transformation logic
   - Be configuration driven where possible - eg column name mapping

### Deliverable for Part 2:

- Code that transforms bronze → silver
- Config (if applicable)
- Demonstration it works (sample output)

---

## Part 3: Discussion (10 min)

We'll discuss these scenarios:

1. **Walk me through your config structure - why this design?**

2. **How would you add a third org?**

3. **"What would you add if you had more time?"**

---

## Important Notes

**You don't need to finish everything.** We'd rather see:

- Well-reasoned architecture decisions
- Thoughtful validation in what you do implement
- Config-driven approach

Than:

- Rushed code that "works" but is brittle
- No validation / just passes data through
- Hard-coded org-specific logic

**If short on time:** Architecture decisions (Part 1) are most important. We can discuss Part 2 implementation even if you don't finish coding it. You can add #TODOs so that I can see your thinking.

Good luck!
