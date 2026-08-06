# Cognitive 0.4.14

## Diagram generator

The generator now wraps labels before Graphviz layout, automatically recomposes over-wide diagrams without splitting them, and assigns landscape page orientation only to exceptional cases that remain wider than the portrait limit. Post-layout font scaling is prohibited.

This corrective release adds figure numbers directly to the visible title of every diagram and imported figure. The same number and title are used in the global List of Figures.
