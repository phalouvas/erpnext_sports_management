# Sports Management - AI Coding Instructions

## Architecture Overview

**Sports Management** is a Frappe-based ERPNext application for managing sports tournaments, teams, players, and match statistics. It uses the **WebsiteGenerator** pattern for public-facing content (Match, Team, Tournament, Person doctypes).

### Core Domain Model
- **Tournament**: Container for leagues with scheduling (round-robin matches via `circle_method`), rankings calculation, and game days
- **Team/Club**: Organizational structure where teams belong to clubs and participate in tournaments
- **Match**: Generated from tournament scheduling; contains rosters, referees, and events
- **Person**: Athletes/staff with career stats calculated from tournament participation
- **Ranking**: Calculated aggregate of team performance (wins/draws/losses/points) per tournament

### Key Patterns to Understand
1. **Match Generation** (`tournament.py::create_matches`): Tournaments auto-generate round-robin matches via circle method algorithm (lines 200-238)
2. **Ranking Calculation** (`tournament.py::calculate_rankings`): Computed from completed matches, updates team points and person stats (lines 241-261 and beyond)
3. **Context-based Views**: Most public doctypes override `get_context()` to compose related data for web pages (Match/Team/Person/Tournament)
4. **Document Events** (`hooks.py`): User/Customer creation triggers auto-assignment of role profiles and portal access

## Development Workflows

### Running Tests
```bash
bench run-tests --doctype Match  # Run specific doctype tests
bench run-tests sports_management  # Run entire app tests
```

### Database Operations
- Use `frappe.db.sql()` for bulk deletes (e.g., `delete_matches()` in tournament.py)
- Use `frappe.db.set_value()` for batch field updates (see `calculate_rankings()` pattern)
- Use `frappe.get_all()` with field joins for complex queries (e.g., `fields=['person.person_name', 'position.position_name']`)

### Publishing Web Content
Doctypes extending `WebsiteGenerator` (Match, Team, Tournament, Person) automatically generate public routes:
- Set `published=1` to make visible
- Override `get_list_context()` for list views
- Override `get_context()` to compose template variables (teams, matches, rosters)
- Set `route` field explicitly if auto-routing fails (see Match.insert pattern)

## Project Conventions

### File Organization
- **doctype/{doctype_name}**: Standard Frappe structure (`{name}.py`, `{name}.json`, `test_{name}.py`, `{name}.js`)
- **hooks/**: Custom event handlers (e.g., `user.py` for role assignments)
- **web_form/**: User-facing CRUD forms (e.g., `my_teams`, `my_persons`) with `apply_document_permissions=1`
- **web_template/**: Reusable template sections (e.g., `blog_and_rankings`)

### Doctype Patterns

#### WebsiteGenerator Doctypes (Match, Team, Tournament, Person, League, Club, Venue)
```python
from frappe.website.website_generator import WebsiteGenerator

class MyDoctype(WebsiteGenerator):
    def get_context(self, context):
        # Load related documents and filtering (published=1)
        context.related_items = frappe.get_all('RelatedDoctype', 
            filters={'published': 1, 'parent': self.name},
            fields=['field1', 'field2.nested_field'])
        # Order by date/position/rank for display order
        context.items = sorted(context.items, key=lambda x: x.date)
```

#### Business Logic Doctypes (MatchRoster, Ranking, GameDay, MatchEvent)
- Validate constraints in `validate()` or `before_insert()` (e.g., prevent duplicate rosters)
- Use `frappe.throw(_('message'))` with `_()` localization wrapper for errors
- Avoid complex logic; prefer calculation in parent doctype (see `Match.create_match_rosters()`)

#### Document Events in hooks.py
```python
doc_events = {
    "DocTypeName": {
        "after_insert": "path.to.function",
        "on_update": "path.to.function"
    }
}
```
Always use `method` parameter or explicit function signatures with `(doc, method)`.

### Query & Data Loading Conventions
- **Filters with joins**: Use field dotted notation to fetch nested values efficiently
  ```python
  frappe.get_all('Match', 
      filters={'status': 'Completed'}, 
      fields=['home', 'home.team_name', 'full_time_home_result'])
  ```
- **Ordering**: Use `order_by='date asc'`, `order_by='rank asc'` (default ascending)
- **List filtering**: Apply `published=1` in web contexts; use `disabled=0` in Ranking queries

### Calculation Patterns
- **Aggregation**: Loop through matches to calculate stats (wins, points, score_for/score_against)
- **Person stats** from tournament context: Sum goals, yellow cards, minutes played from Match Events
- **Ranking sort**: Use `sorted(list, key=lambda x: x.points, reverse=True)` then reassign rank

## Integration Points

### External APIs/Services
- No external API calls in current codebase; all operations are internal Frappe/ERPNext

### Cross-Module Dependencies
- **ERPNext**: Item, Customer, Supplier (not heavily used; app is self-contained)
- **Frappe Core**: User, Website Item, Web Form, Web Template
- **Custom Roles**: "Sports" role assigned to Website Users via `asign_role_profile()` hook

### Key Middleware/Hooks
- `after_install`: Runs `sports_management.setup.install.after_install`
- `after_insert` on User/Customer: Auto-configures portal access and role profiles

## Critical Conventions

1. **Always use `frappe.throw()` with `_()` for error messages** (localization support)
2. **Query results**: Check list length before indexing (e.g., `home_team[0]` in `calculate_rankings()`)
3. **Bulk operations**: Use `frappe.db.sql()` for deletes; use `frappe.db.set_value()` for updates to avoid trigger loops
4. **Whitelist functions**: Use `@frappe.whitelist()` decorator for methods called from frontend
5. **Test inheritance**: Extend `FrappeTestCase` from `frappe.tests.utils` (currently most tests are empty placeholders)

## Common Tasks

### Adding a New Doctype
1. Create folder in `doctype/` with `{name}.json`, `{name}.py`, `test_{name}.py`
2. Inherit from `Document` or `WebsiteGenerator` based on whether it needs a public page
3. Add `after_insert`, `on_update` hooks in `hooks.py` if dependent documents need updating
4. Use `@frappe.whitelist()` for any methods called from frontend

### Scheduling Match Generation
Tournament scheduling uses `create_matches()` whitelisted function (called from UI).
To add automated scheduling, add to `hooks.py`:
```python
scheduler_events = {
    "weekly": ["sports_management.sports_management.doctype.tournament.tournament.create_matches"]
}
```

### Extending Rankings Calculation
`calculate_rankings()` is the single source of truth. Modify:
1. The points calculation logic (win/draw/loss multipliers configured in Tournament doctype)
2. The ranking tie-breaker (currently sorted by points only; add secondary sort by difference/score_for if needed)
3. Person points aggregation at the end

