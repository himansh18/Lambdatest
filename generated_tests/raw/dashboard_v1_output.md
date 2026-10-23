Dashboard Test Cases

Assumptions: the dashboard has several widgets (KPI cards, charts, tables), global filters (date range, category, etc.), sortable tables, and role-based access (e.g., Admin, Manager, Viewer). Adjust the names to match your app.

1. Widget Loading
ID	Scenario	Steps	Expected result
WL-01	Initial load, all widgets succeed	Log in and open the dashboard	All widgets render with data, no errors, no stuck spinners
WL-02	Loading indicators	Throttle the network to Slow 3G and open the dashboard	Each widget shows a skeleton or spinner until its data arrives, and the layout doesn’t jump
WL-03	Independent widget loading	Delay one widget’s API response	Other widgets render without waiting for it
WL-04	Single widget API failure	Mock a 500 on one widget’s endpoint	That widget shows an error state with a Retry option; the others are unaffected
WL-05	Retry after failure	Click Retry on a failed widget after restoring the API	The widget loads data and the error state clears
WL-06	Empty data	Use an account or filter with no data	Widgets show a clear “No data” state, not blank space, NaN, or 0 masquerading as real data
WL-07	Request timeout	Make an endpoint exceed the timeout	The widget shows a timeout error and doesn’t load indefinitely
WL-08	Session expiry	Let the token expire, then refresh a widget	The user is redirected to login or the session is renewed; no raw 401 error is shown
WL-09	Auto-refresh	Enable the refresh interval (if supported)	Data refreshes at the interval without resetting filters, scroll position, or sort order
WL-10	Large dataset	Load an account with 100k+ records	The dashboard loads within the performance target (e.g., under 3s to first meaningful widget) and the UI stays responsive
WL-11	Rapid navigation	Navigate away mid-load and return	No duplicate requests, console errors, or stale data from aborted calls
2. Data Accuracy
ID	Scenario	Steps	Expected result
DA-01	KPI vs. source	Compare each KPI card to a direct DB query or API response	Values match exactly
DA-02	Chart vs. table consistency	Compare a chart’s totals with its related table	Totals are consistent across widgets
DA-03	Aggregation correctness	Seed known data (e.g., 10 orders totaling 1,250.50)	Sum, count, average, and percentage calculations are correct
DA-04	Rounding and formatting	Use values like 1234.565, 0.005, and very large numbers	Rounding follows spec; thousands separators, decimals, and currency symbols are correct
DA-05	Date and time zone handling	Change the user’s time zone, test records near midnight	Date-bucketed data lands in the correct day for the user’s time zone
DA-06	Date range boundaries	Select a range ending today and one starting at a month boundary	Start and end dates are inclusive or exclusive per spec, with no off-by-one
DA-07	Real-time update	Create a new record in another session	The dashboard reflects it after refresh or auto-update
DA-08	Deleted/archived records	Delete or archive a record	It is excluded from (or included in) metrics per spec
DA-09	Zero and null values	Seed records with null or zero fields	No NaN, “undefined”, or divide-by-zero errors; percentages handle a zero denominator
DA-10	Trend/delta indicators	Compare the current vs. previous period	The up/down arrow, percentage change, and color match the actual difference
DA-11	Tooltip and legend values	Hover over chart points and bars	Tooltip values match the underlying data and legends match the series
DA-12	Currency/locale	Switch the user’s locale	Numbers, dates, and currency format correctly for the locale
3. Filter Behavior
ID	Scenario	Steps	Expected result
FL-01	Single filter	Apply one filter (e.g., Region = EMEA)	All relevant widgets update to reflect it
FL-02	Multiple filters (AND)	Combine date range, category, and status	Results satisfy all filters; widget data stays consistent
FL-03	Date range presets	Select Today, Last 7 days, This month, and Custom	Each preset resolves to the correct range
FL-04	Invalid custom range	Set an end date before the start date	Validation error is shown and the data isn’t updated with bad input
FL-05	Clear/reset filters	Click Reset or Clear all	Filters return to their defaults and the data matches the unfiltered view
FL-06	No results	Apply a filter combination that matches nothing	Widgets show an empty state and the filter stays active and visible
FL-07	Filter persistence	Apply filters, refresh the page, and navigate away and back	Behavior matches spec (persisted via URL, session, or user preference)
FL-08	Shareable URL	Copy the URL with filters applied and open it in a new session	The same filters and view are restored (if supported)
FL-09	Rapid filter changes	Change filters quickly several times	Only the final selection’s data is shown, with no race conditions
FL-10	Multi-select filter	Select and deselect multiple options	The count badge and results are correct
FL-11	Dependent filters	Change Country, then check City options	The City options update and an invalid selection is cleared
FL-12	Global vs. widget filters	Apply a widget-specific filter	It affects only that widget, not the others
4. Sort Behavior
ID	Scenario	Steps	Expected result
SO-01	Ascending and descending	Click a column header repeatedly	Order toggles asc, desc, and default (if applicable), with the indicator icon updating
SO-02	Numeric sorting	Sort a numeric column with 2, 10, 100	Sorted numerically (2, 10, 100), not lexicographically
SO-03	Text sorting	Sort names with mixed case, accents, and symbols	Order is consistent and case-insensitive per spec
SO-04	Date sorting	Sort a date column	Chronological order, not string order
SO-05	Null/blank values	Sort a column containing nulls	Nulls are consistently placed (all first or all last)
SO-06	Sort and filter together	Apply a filter, then sort	Sorting applies only to the filtered data, and the filter persists
SO-07	Sort with pagination	Sort and then go to page 2	The sort applies across the entire dataset, not just the visible page
SO-08	Sort stability	Sort by a column with duplicate values	Ties keep a stable, predictable order
SO-09	Sort persistence	Sort, refresh, and return	Behavior matches spec
SO-10	Multi-column sort	Shift-click a second column (if supported)	Primary and secondary sorts are applied correctly
SO-11	Chart ordering	Check Top N or ranked charts	Bars and items are ordered by value, and “Other” is handled correctly
5. Responsive Layout
ID	Scenario	Steps	Expected result
RL-01	Desktop (≥1440px)	Open the dashboard at 1440 and 1920	The grid uses the space well and nothing is overstretched
RL-02	Laptop (1024-1280px)	Resize to 1024 and 1280	Widgets reflow without overlap or clipping
RL-03	Tablet (768px) portrait and landscape	Test in both orientations	The grid collapses to fewer columns; charts are readable and tap targets are usable
RL-04	Mobile (360-414px)	Test on a phone viewport	Widgets stack in a single column with no horizontal page scroll
RL-05	Wide tables	View a data table on mobile	The table scrolls horizontally in its container or switches to a card layout
RL-06	Chart resizing	Drag the browser width continuously	Charts redraw to fit; labels, legends, and axes don’t overlap or truncate
RL-07	Filter bar on small screens	Open filters on mobile	Filters collapse into a drawer or menu that is fully usable
RL-08	Touch interactions	Tap, swipe, and long-press on a touch device	Tooltips, sorting, and filters work without hover; tap targets are at least 44px
RL-09	Zoom and text scaling	Set browser zoom to 200% and larger system font	Content remains accessible and unbroken
RL-10	Long content	Use very long titles, names, or numbers	Text truncates with an ellipsis or wraps and doesn’t break the layout
RL-11	Cross-browser	Test Chrome, Firefox, Safari, and Edge	Layout and behavior are consistent
RL-12	Navigation/sidebar	Collapse and expand the sidebar	The dashboard grid adjusts without layout glitches
6. Permission-Based Visibility

Sample role matrix (replace with your actual roles):

Widget	Admin	Manager	Viewer
Revenue KPI	✅	✅	❌
Team performance	✅	✅ (own team)	❌
User management	✅	❌	❌
Activity feed	✅	✅	✅
ID	Scenario	Steps	Expected result
PV-01	Admin view	Log in as Admin	All widgets are visible
PV-02	Manager view	Log in as Manager	Only permitted widgets are visible
PV-03	Viewer view	Log in as Viewer	Restricted widgets aren’t rendered, and no empty gaps or placeholders are left in the layout
PV-04	Data scoping	Log in as a manager of Team A	Only Team A’s data appears in shared widgets and totals
PV-05	API enforcement	Call a restricted widget’s API directly with a lower-privilege token	Returns 403 (or 404), with no data leakage
PV-06	Hidden is not just CSS	Inspect the DOM and network tab as a restricted user	Restricted widget markup and data aren’t in the DOM or responses
PV-07	Role change	Change a user’s role while they’re logged in	Visibility updates after refresh or re-login, per spec
PV-08	Permission revocation	Revoke access mid-session and refresh a widget	The widget is removed or an access-denied message is shown, and cached data isn’t displayed
PV-09	Export/action buttons	Check Export, Edit, and Delete buttons per role	Controls appear only for authorized roles, and direct calls are blocked server-side
PV-10	Deep links	A restricted user opens a URL to a restricted widget or view	Redirected or shown access denied; no data is displayed
PV-11	Multi-tenant isolation	Log in as a user from Org A	No Org B data appears anywhere, including filters and dropdown options
PV-12	No-role/new user	Log in as a user with no assigned role	A safe default view or “no access” message is shown
PV-13	Filter options by permission	Open filter dropdowns as a restricted user	Options list only the values the user may access
PV-14	Customization	A user rearranges or hides widgets (if supported)	Changes are saved per user and never expose restricted widgets