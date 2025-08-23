# Appendix A: Dataset Details

- Users: atiq, masum, rakib, zia.
- Segmentation: 50 events per segment.
- Total segments: 76,693.
- Per-user distribution provided in `results/results.md`.
- Event definitions: DM, VM, HM, LD/LU, RD/RU, MW.
- Collection environments: Windows and Linux/Wayland collectors.

Notes:

- Day Time is encoded as 5-minute buckets (0–287).
- On Linux/Wayland, WindowTitle is 0 due to lack of API access.
