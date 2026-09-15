# Diagrams, figures, and other images - Google developer documentation style guide

- URL: https://developers.google.com/style/images
- Fetched: 2026-09-15
- Source type: official docs
- Last updated (if shown): unknown (page does not show a visible last-updated date in the fetched extraction)

## When to use images

"Use images only when they provide useful visual explanations of information that is otherwise difficult to express with words."

## Screenshot guidelines

- **Consistency**: "Be consistent for a given document or doc set in what operating system you use for screenshots" and maintain visual consistency in appearance.
- **Cropping**: "Crop screenshots to show the relevant information" to help readers focus on key details and improve future-proofing.
- **Privacy**: Never include personally identifiable information. If necessary: "hide it with a solid-color overlay with 100% opacity. Don't rely on blurs, mosaic effects, or similar image-processing effects."
- **Formatting**: Avoid images of text, code, or terminal output; use actual text instead.

## Image formats

For diagrams: "Use SVG files if possible because SVGs stay sharp when you zoom in on the image." If SVG isn't available, use PNG unless justified otherwise. Never use transparent backgrounds, particularly for diagrams used with lightbox widgets.

For animations: Avoid animated GIFs; use resource-efficient formats like MP4 instead.

## Alt text requirements

- Keep it under 155 characters
- Use complete sentences or noun phrases
- Include punctuation
- Avoid phrases like "Image of" or "Photo of"
- Use empty alt text (`alt=""`) for purely decorative images

## Image sizing

Images should not exceed the column width. The guide notes typical constraints: if a column is 856px wide, images shouldn't exceed that; the 2x version should be no wider than 1712px.

Use the `srcset` attribute to provide high-resolution versions for modern displays, specifying both `1x` and `2x` resolutions.

## Organization elements

- Always introduce images with complete sentences.
- Use figure numbers optionally: "Figure 1. Description here."
- Figure captions and descriptions differ; descriptions convey information shown in the image.
- Don't embed captions within graphics themselves.
