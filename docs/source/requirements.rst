==========================
System Requirements
==========================

This section outlines the initial functional and non-functional requirements for the Recipe App project. These were gathered during Coursework 1 and revised as implementation progressed.

Functional Requirements
---------------------------

- The system shall allow users to register and log in to their own profile.
- Users can add ingredients to a virtual pantry.
- The system shall display recipes that match ingredients from the pantry.
- Users shall be able to view the steps, ingredients, and estimated time for each recipe.
- Each recipe shall include a nutritional value estimate per serving.
- The app shall allow users to set and run a customisable cooking timer.
- The system shall provide a shopping list based on missing ingredients.
- Users shall be able to remove ingredients from their pantry.
- Offline access to previously loaded data shall be supported.

Non-Functional Requirements
------------------------------

- The app shall find a recipe in under 3 seconds (on average).
- The interface shall be accessible on all screen sizes, including mobile.
- The app shall allow users to adjust text size for accessibility.
- All core functionality must be available with minimal learning curve.
- The system must run reliably without crashing during user interaction.

Changes During Development
------------------------------

- Web scraping was replaced with a curated local JSON-based recipe dataset to reduce development time and complexity.
- The focus shifted toward implementing core pantry and recipe functionality over advanced features like nutritional breakdown APIs or real-time scraping.
