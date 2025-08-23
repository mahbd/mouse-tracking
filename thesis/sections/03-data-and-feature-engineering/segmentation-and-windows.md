## Segmentation and Windows

We segment raw event streams into fixed 50-event windows to standardize sample length and simplify batch processing. Alternatives include time-based windows and overlapping strides. Fixed windows reduce complexity and encourage consistent feature distributions, at the cost of potential boundary effects.
