# Path Navigation System

Welcome!

This take-home test is designed to evaluate your expertise in **building an interactive map-based application**. While UI implementation is not the focus of this exercise, we aim to tests your ability to work with mapping libraries, implement spatial algorithms, and handle user interactions.

---

## Objective

Create a web application where users can:

1. View a map with randomly distributed house markers
2. Place a person marker on the map by clicking
3. Calculate and visualize the shortest path from the person to the nearest house
4. Experience smooth interactions and clear visual feedback

## Requirements

### Functional Requirements

#### 1. Map Initialization

- Display an interactive map centered on a reasonable default location
- Generate and display 8-12 house markers at random coordinates within the visible map bounds
- Houses should remain in fixed positions throughout the session

#### 2. Person Placement

- Allow users to place a person marker by clicking anywhere on the map
- Only one person marker should exist at a time (placing a new one removes the previous)

#### 3. Navigation Button

- Show a "Find Nearest House" button (or similar) that is:
  - Disabled/hidden when no person marker is placed
  - Enabled when a person marker exists
- Clicking the button should trigger pathfinding

#### 4. Path Visualization

- Calculate the nearest house using straight-line distance (Euclidean or Haversine)
- Display a visible path (line) from the person to the nearest house
- Highlight or emphasize the target house differently from other houses
- Show distance information (e.g., "Nearest house: 2.4 km away")

#### 5. Reset Functionality

- Provide a way to clear the person marker and path to start over

### Technical Requirements

- Use React with TypeScript (strict mode preferred)
- Implement with a mapping library: Deck.GL, Leaflet, or similar
- Use functional components with React Hooks
- Implement proper TypeScript types for your data structures (House, Person, Coordinates, etc.)
- Handle edge cases gracefully (no houses, map boundaries, etc.)

## Guidelines

### What We're Looking For

- **Code Quality**: Clean, readable, well-organized code with appropriate separation of concerns
- **TypeScript Usage**: Proper typing, avoiding any where possible
- **Component Structure**: Logical component breakdown and reusability
- **Problem Solving**: How you approach the pathfinding and distance calculation

### What You Can Skip

- Backend implementation (all data can be generated client-side)
- Complex routing algorithms (straight-line paths are sufficient)
- Mobile responsiveness (desktop-first is fine)

### Bonus Points (Optional)

- Unit tests for utility functions (distance calculation, nearest house finder)
- Show paths to multiple nearest houses (e.g., top 3)
- Allow users to add/remove houses manually
- Implement actual road-based routing using a routing API

## Evaluation Criteria

Your submission will be evaluated on the following:

### Code Quality (30%)

- TypeScript usage and type safety
- Component architecture and separation of concerns
- Code readability and naming conventions
- Proper use of React patterns (hooks, state management)

### Functionality (30%)

- All core requirements are implemented and working
- Application handles user interactions correctly
- Pathfinding logic is accurate
- Edge cases are handled appropriately

### Technical Implementation (30%)

- Effective use of the chosen mapping library
- Efficient algorithms for distance calculation and nearest house finding
- Performance considerations

### Documentation & Communication (10%)

- Clear README with setup instructions
- Code comments where necessary
- Explanation of technical decisions and trade-offs

## Timeline

You will have **7 days** from receiving this task to submit your solution. Please ensure your work is complete and well-tested before submission.

## Submission

- Create a private repo and add AISuhasDattatreya as a reviewer to your PR.
- Submit the PR link and your notes (timelines, breakdown and what you've implented) to suhas@advanced-infrastructure.co.uk
- We'll go over your code together and discuss your architecture

---

We look forward to seeing your expertise in action. Good luck, and happy coding!
