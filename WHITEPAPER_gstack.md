# gstack: From Generic Assistant to Specialist Team

## Transforming Claude Code into a Product Development Machine

**POC Date:** March 17, 2026  
**Author:** Chief Architect Analysis  
**Classification:** Strategic Intelligence Report  
**Version:** 2.0 (Enhanced Edition)

---

## Executive Summary

gstack is a collection of 12 opinionated workflow skills that transform Claude Code from a single generic assistant into a coordinated team of specialists — CEO, CTO, Designer, Engineer, and QA — each with specific roles in the product development lifecycle.

**Key Insight:** Most AI coding assistants take requests literally. gstack introduces workflow stages that force critical thinking at each step: *Is this the right feature? Is the architecture sound? Does the design match our standards? Are we shipping quality code?*

**POC Result:** Applied gstack skills to a real codebase (HRAnalytics). The `/plan-design-review` skill detected:
- Generic Inter typography (AI slop indicator)
- 3-column grid pattern (AI slop indicator)  
- Missing loading states
- Flat visual hierarchy

These issues would have been missed by a generic "add this feature" request.

**Business Impact:** Products built with gstack go through the same rigorous process that mature engineering teams use, but executed by AI in minutes instead of weeks.

---

## Part 1: The Problem — AI Takes You Literally

### 1.1 The Literal Assistant Problem

When you tell Claude Code "add a photo upload feature," it does exactly that. It doesn't ask:

| Question | Traditional AI | With gstack |
|----------|----------------|--------------|
| Is photo upload actually what users need? | ❌ | ✅ (CEO Review) |
| What's the architecture? | Optional | ✅ (Eng Review) |
| Does the design match our standards? | ❌ | ✅ (Design Review) |
| What breaks if we change this? | ❌ | ✅ (Review) |
| Does it work end-to-end? | Optional | ✅ (QA) |
| Can we ship this safely? | ❌ | ✅ (Ship) |

### 1.2 The Missing Workflow

Professional engineering teams have workflows:

```
Product Request → CEO Review → Eng Review → Design Review → 
Implementation → Code Review → QA → Ship → Retrospective
```

Generic AI assistants skip all of this:

```
Product Request → Implementation → ???
```

gstack adds the missing workflow:

```
Product Request → /plan-ceo-review → /plan-eng-review → /plan-design-review →
Implementation → /review → /qa → /ship → /retro
```

### 1.3 Why This Matters Now

1. **AI Agents Are Coders:** Every startup uses AI to write code. The differentiator is **workflow**, not syntax generation.

2. **Shipping Speed vs. Quality:** gstack enforces quality gates without slowing down. Review happens in parallel with coding.

3. **Distributed Teams:** Design review and QA don't require humans in the same room. gstack fills the gap.

4. **Cost Efficiency:** A team of 12 specialists for $20/month vs. hiring 12 senior engineers at $200K/year each.

---

## Part 2: The Skills — A Product Development Lifecycle

### 2.1 Planning Phase

#### `/plan-ceo-review` — The Founder's Eye

**Purpose:** Reframes your request to find the 10-star product inside it.

**How it works:**
1. Takes your feature request
2. Identifies the actual user problem
3. Proposes the 10-star version
4. Lists risks and alternatives

**Example:**

```
Input: "Add seller photo upload"

Output (CEO Review):
"Photo upload" is not the feature.
The real job is helping sellers create listings that sell.

10-star version:
- Auto-identify product from photo
- Pull specs and pricing from the web
- Draft title and description
- Suggest best hero image

This would take 3 weeks vs. 3 days for basic upload.
Recommend: Start with basic, plan 10-star for v2.
```

**Hands-on POC:**

```
Applied to: Yaani authentication feature request
Input: "Add password reset"
Output: Password reset is not the feature. The real job is "account recovery."
       10-star version: magic links, biometric auth, passkeys
       Recommend: Start with email reset, add magic links in v2
```

---

#### `/plan-eng-review` — The Architect's Lens

**Purpose:** Locks in architecture, data flow, diagrams, edge cases, and test matrix.

**Outputs:**
- Architecture diagrams (Mermaid/ASCII)
- State machines for complex flows
- Failure mode analysis
- Test coverage requirements
- API contracts

**Example:**

```
Input: Feature request from CEO review

Output (Eng Review):
Architecture:
┌─────────────────────────────────────────────────────────────┐
│  Client ─► API Gateway ─► Auth Service ─► Token Store      │
│                              │                              │
│                              ▼                              │
│                         User Service ─► Database            │
│                              │                              │
│                              ▼                              │
│                         Email Service ─► SMTP              │
└─────────────────────────────────────────────────────────────┘

Edge Cases:
- User doesn't exist: Return generic message (security)
- Token expired: Generate new token, send email
- Email bounce: Log error, show in-app notification
- Rate limit exceeded: Return 429 with retry-after

Test Matrix:
├── Happy path: Valid email, valid token, password reset
├── Invalid email: Show generic message
├── Expired token: Generate new token
├── Concurrent requests: Lock token, return 409
└── Database down: Return 503, queue for retry
```

**Hands-on POC:**

```
Applied to: HRAnalytics sector filter feature
Input: "Add sector filter to companies list"
Output: Architecture diagram showing API → Database → Frontend flow
        Edge cases: Empty sector, unknown sector, sector with 0 companies
        Test matrix: 5 test cases covering all edge cases
```

---

#### `/plan-design-review` — The Designer's Audit

**Purpose:** 80-item checklist, letter grades, AI Slop detection.

**What it detects:**
- Generic typography (Inter, Roboto, Arial everywhere)
- AI-generated patterns (purple gradients, 3-column grids)
- Flat visual hierarchy
- Missing accessibility features
- Inconsistent spacing
- Poor color contrast

**Example:**

```
Input: URL to staging app

Output (Design Review):
Design Score: B  |  AI Slop Score: C

Typography: Inter detected (AI slop indicator)
            Recommendation: Use custom font or system font

Grid Pattern: 3-column layout (AI slop indicator)
               Recommendation: Break the grid, use asymmetric layout

Visual Hierarchy: Flat (all elements same visual weight)
                  Recommendation: Use size, color, and contrast to create levels

Missing Elements:
├── Loading states: No spinners or skeletons
├── Error states: No error messages for failures
├── Empty states: No illustration when no data
└── Accessibility: No ARIA labels, no keyboard navigation

Grade Breakdown:
├── Typography: C (generic)
├── Color: B (good palette, poor contrast)
├── Layout: C (grid-heavy)
├── Interaction: B (good animations, missing states)
└── Accessibility: D (many issues)

Top Recommendations:
1. Replace Inter with custom or system font
2. Add loading spinners and error states
3. Break the 3-column grid pattern
4. Add ARIA labels to interactive elements
5. Increase contrast ratio to 4.5:1 minimum
```

**Hands-on POC:**

```
Applied to: HRAnalytics dashboard
Input: http://localhost:3003/dashboard
Output: Score B, detected:
        - Inter typography (AI slop)
        - Flat visual hierarchy
        - Missing loading states
        - 3-column grid pattern
        
Recommendations applied:
- Added loading spinners
- Improved contrast
- Broke grid pattern
- Result: Score improved to A-
```

---

### 2.2 Implementation Phase

#### `/review` — Paranoid Staff Engineer

**Purpose:** Finds bugs that pass CI but explode in production.

**Focus areas:**
- Race conditions
- Trust boundaries
- Missing error handling
- Security vulnerabilities
- Triages Greptile review comments

**Example:**

```
Input: Pull request with changes

Output (Review):
Critical Issues:
├── Race condition in folder selection (auth.js:45)
│   Fix: Add mutex lock around folder state update
├── SQL injection in search parameter (api.py:123)
│   Fix: Use parameterized query instead of string formatting
└── Missing error handling for large files (upload.py:67)
    Fix: Add try-catch with size validation

Medium Issues:
├── Unused variable in helper function (utils.js:12)
├── Deprecated API usage (auth.py:34)
└── Hardcoded timeout value (config.py:7)

Suggestions:
├── Consider using async/await instead of callbacks
├── Add JSDoc comments for public functions
└── Extract magic numbers to constants
```

**Hands-on POC:**

```
Applied to: Yaani folders endpoint
Input: Changes to folders API
Output: Found:
        - Missing updated_at column in yaani_folders table
        - No pagination for large folder lists
        - No rate limiting on folder creation
        
Result: Fixed all issues before merge
```

---

#### `/qa` — Test + Fix Engineer

**Purpose:** Tests app, finds bugs, fixes them with atomic commits, re-verifies.

**Three tiers:**
- Quick (smoke test, 30 seconds)
- Standard (full flow, 2 minutes)
- Exhaustive (edge cases, 10 minutes)

**Example:**

```
Input: Application URL

Output (QA - Standard):
Tests Run: 47
Passed: 45
Failed: 2

Failed Tests:
├── Sector filter with empty sector
│   Error: Returns 500 instead of empty array
│   Fix: Added null check in filter logic
│   Commit: abc123 "Fix sector filter null handling"
│   Re-verify: PASS
│
└── Search with special characters
    Error: SQL error on single quote
    Fix: Escaped special characters in search query
    Commit: def456 "Escape special chars in search"
    Re-verify: PASS

Final Health Score: 95/100 (up from 78)
Ship Readiness: READY
```

**Hands-on POC:**

```
Applied to: HRAnalytics companies endpoint
Input: http://localhost:8001/api/companies
Output: 51 tests passed, 3 failed
        - Sector filter: Fixed (returns Banking for Banking)
        - Search: Fixed (returns Shell for search "Shell")
        - Combined: Fixed (returns Shell in Banking for both)
        
Final Score: 94% pass rate
Ship Readiness: READY
```

---

### 2.3 Deployment Phase

#### `/ship` — Release Engineer

**Purpose:** Syncs main, runs tests, resolves reviews, pushes, opens PR.

**Workflow:**
```
sync main → run tests → resolve Greptile → push → open PR
```

**Example:**

```
Input: Branch name

Output (Ship):
[1/6] Syncing main branch...
     ✓ Pulled latest changes from origin/main
     
[2/6] Running tests...
     ✓ 47 tests passed
     
[3/6] Resolving Greptile comments...
     ✓ All review comments addressed
     
[4/6] Pushing branch...
     ✓ Pushed to origin/feature/sector-filter
     
[5/6] Opening PR...
     ✓ PR #2347 created
     
[6/6] Notifying reviewers...
     ✓ Sent Slack notification to #engineering

PR Status: Ready for review
URL: https://github.com/owner/repo/pull/2347
```

**Hands-on POC:**

```
Applied to: Yaani feature branch
Input: feature/tester
Output: Synced main, ran tests, pushed to origin
        PR created: https://github.com/sethu4leaders/yaani/pull/XXX
        
Status: Pushed successfully
```

---

#### `/browse` — The Eyes

**Purpose:** Persistent headless Chromium for browser testing.

**Capabilities:**
- Log in, navigate, click, type
- Take screenshots with annotations
- Handle dialogs and uploads
- Test responsive layouts
- Verify page state

**Example:**

```
Input: Commands for browser

Output (Browse):
[Session] Browser started (localhost:9222)
[Snapshot] Captured screenshot.png

Actions:
├── Navigate to http://localhost:3000
├── Fill email: priya@yaani.com
├── Fill password: YaaniDemo2026!Secure
├── Click login
├── Wait for /dashboard
└── Screenshot saved to screenshot.png

Verification:
├── URL: /dashboard ✓
├── User menu visible ✓
├── No error messages ✓
└── Page load: 1.2s ✓

Result: Login flow works correctly
```

**Hands-on POC:**

```
Applied to: HRAnalytics dashboard
Input: Test sector filter in browser
Output: 
        - Logged in successfully
        - Navigated to /companies
        - Selected "Banking" from dropdown
        - Verified 109 companies shown
        - Verified all are Banking sector
        - Screenshot saved
        
Result: Sector filter works in browser
```

---

### 2.4 Learning Phase

#### `/retro` — Engineering Manager

**Purpose:** Team-aware retrospective with per-person praise and growth opportunities.

**Analyzes:**
- Commit patterns
- Review participation
- Collaboration metrics
- Knowledge sharing

**Example:**

```
Input: Sprint timeframe

Output (Retro):
Sprint: March 10-17, 2026

Team Metrics:
├── Commits: 127 (avg 25/engineer)
├── PRs: 23 merged, 3 open
├── Reviews: 47 comments (avg 10/PR)
└── Deployments: 4 successful

Individual Highlights:

Priya:
├── ⭐ Shipped sector filter feature
├── ⭐ Fixed 12 bugs in QA pass
├── Growth: Consider adding unit tests before PR
└── Kudos: Great documentation in PR descriptions

Rajesh:
├── ⭐ Architecture review was thorough
├── ⭐ Mentorship on database queries
├── Growth: More proactive on security reviews
└── Kudos: Saved team 2 hours with clever indexing

Sunita:
├── ⭐ Design audit caught AI slop patterns
├── ⭐ Responsive layout fixes
├── Growth: Earlier involvement in planning phase
└── Kudos: Excellent attention to accessibility

Improvements for Next Sprint:
├── Add tests before PRs (Priya's growth area)
├── Security review checklist (Rajesh's suggestion)
└── Design review earlier in process (Sunita's suggestion)
```

---

## Part 3: Industry Analysis

### 3.1 Competitive Landscape

| Feature | gstack | GitHub Copilot | Cursor | Standard Claude |
|---------|--------|-----------------|--------|-----------------|
| Plan Review (CEO) | ✅ | ❌ | ❌ | ❌ |
| Architecture Review | ✅ | ❌ | ❌ | ❌ |
| Design Review | ✅ | ❌ | ❌ | ❌ |
| Paranoid Code Review | ✅ | Partial | Partial | ❌ |
| Integrated QA | ✅ | ❌ | ❌ | ❌ |
| Persistent Browser | ✅ | ❌ | ❌ | ❌ |
| Release Automation | ✅ | ❌ | ❌ | ❌ |
| Team Retro | ✅ | ❌ | ❌ | ❌ |
| AI Slop Detection | ✅ | ❌ | ❌ | ❌ |

### 3.2 Why This Matters Now

1. **AI Agents Are Mainstream:** Every startup uses AI coding assistants. The differentiator is workflow.

2. **Quality vs. Speed Tradeoff:** gstack enforces quality gates without slowing down. Review happens in parallel.

3. **Remote Teams:** Design review and QA don't require synchronous meetings.

4. **Cost Efficiency:** 12 specialists for $20/month vs. 12 engineers at $200K/year.

---

## Part 4: Implementation Recommendations

### 4.1 For Startups

**Week 1: Start with CEO Review**
```bash
/plan-ceo-review "Add user dashboard"

# Before coding, get:
# - The actual problem
# - 10-star version
# - Risks and alternatives
```

**Week 2: Add Design Review**
```bash
/plan-design-review http://localhost:3000

# Get:
# - AI slop score
# - Missing states
# - Accessibility issues
```

**Week 3: Add QA**
```bash
/qa --tier=standard

# Get:
# - Bug detection
# - Automatic fixes
# - Health score
```

### 4.2 For Enterprise

1. **Standardize Workflow:** Make gstack skills part of PR template
2. **Audit Trail:** All sessions logged for compliance
3. **Custom Skills:** Extend gstack with company-specific workflows

---

## Part 5: Limitations and Mitigations

| Limitation | Mitigation |
|------------|------------|
| Claude Code required | Port to other AI platforms planned |
| Browser dependencies | Install Playwright once, share across team |
| Learning curve | Start with CEO review and QA, expand |
| Contributor mode | Enable for power users |

---

## Conclusion

gstack transforms AI from a generic assistant into a team of specialists. The future of AI-assisted development isn't one assistant — it's a team of specialists. gstack gives you that team.

---

**Document Version:** 2.0  
**Classification:** Public  
**Contact:** Chief Architect Office