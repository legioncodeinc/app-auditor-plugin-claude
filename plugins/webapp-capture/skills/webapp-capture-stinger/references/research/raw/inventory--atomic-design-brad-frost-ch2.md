# Chapter 2: Atomic Design Methodology - Atomic Design by Brad Frost
- URL: https://atomicdesign.bradfrost.com/chapter-2/
- Fetched: 2026-09-15
- Source type: canonical article
- Last updated (if shown): unknown

## Overview

Brad Frost's Atomic Design is a five-stage methodology for building interface design systems, inspired by chemistry principles (atoms, molecules, and organisms combining to form matter).

## The five stages

**Atoms** are foundational UI elements that cannot be reduced further without losing function, basic HTML elements like buttons, labels, and inputs. Each has distinct properties influencing its application.

**Molecules** are simple UI component groups combining atoms into functional units. For example, a search form molecule unites a label, input field, and button, creating a reusable, portable component that adheres to the single-responsibility principle.

**Organisms** are complex components made from molecules and/or atoms, forming distinct interface sections. A header organism, for instance, combines a logo, navigation, and search form to create a standalone section.

**Templates** place components within layouts and reveal the underlying content structure. Rather than showing final content, templates demonstrate "what content _is made_ from," establishing guardrails for dynamic content variations.

**Pages** are concrete template instances with real representative content, allowing designers to test whether design patterns effectively serve actual content needs and accommodate variations.

## Key insights

Atomic design enables designers to traverse between abstract component views and concrete, content-rich layouts simultaneously. This "dance of switching contexts" mirrors how painters step back to assess their complete work.

The methodology creates deliberate separation between structure (templates) and final content (pages), while acknowledging their mutual influence.

Crucially, atomic design is **not a linear process**, it is a mental model for concurrent system and UI creation, not a strict, waterfall-style build order (atoms are not always built first, then molecules, then organisms).
