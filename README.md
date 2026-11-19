# Thursday 19 November 2026 — The World Today

Entry for make.fun `news-image-20261119`: sum up the world's news of
Thursday 19 November 2026 in one image.

A newspaper front page: masthead with the date, a neon Vice City hero
for the GTA VI global rollout (the day's biggest story), and twelve
illustrated story panels, each in its own coloured box (Trump–Xi–Putin
summit in Shenzhen, ICJ Rohingya verdict in The Hague, Voyager 1 at
one light-day, EU €45bn Ukraine loan, Israeli troops cross the Yellow
Line in Gaza, US loses measles-free status, Australia sanctions
Israeli settlers, Cyclone Akvan nears India, Peltola wins Alaska,
Canada resets China ties, Saudi all-clear, US senators warn on AI
cyber threats) — 13 stories, 6 continents, one day.

`draw.py` composes `entry.png` (1024x1024 JPEG) with Pillow: all text
is drawn (no AI text); every illustration is drawn programmatically.
Fully deterministic. `main.py` copies `entry.png` to the output
directory (no network).

Run: `python3 draw.py` then `python3 main.py`.
