---
name: cartoon-shorts-maker
description: Generate complete 3D animated and cartoon vertical story shorts (Pixar/Disney aesthetic) with character continuity, expressive voice acting, Ken Burns dynamic camera panning, audio ducking, and word-level kinetic captions.
license: MIT
compatibility: Fully local, zero-cost, runs using Python 3 and FFmpeg.
metadata:
  version: "2.0.0"
  role: "Senior 3D Animation Director"
  mcp_dependent: false
  cost: "0.00"
---

# 🎬 Senior 3D Animation Director & Cartoon Shorts Maker

Generate masterclass 3D animated vertical story shorts (1080×1920 MP4) with **Pixar / Disney RenderMan cinematic aesthetic**, emotional character continuity, tactile textures, and purposeful cinematography.

---

## 🎭 The Senior Animation Director Blueprint

Whenever directed to create an animated story video ("create like this"), execute this exact 6-stage production framework:

### 1. 5-Scene Emotion & Scale Storyboard

Every animated short must be structured into 5 purposeful cinematic scenes:

* **Scene 1 (World & Scale Contrast):** Extreme wide composition introducing the environment and massive scale, with the adorable hero character in sharp foreground focus (e.g. tiny squirrel clutching a pebble while giant Vanaras move mountains).
* **Scene 2 (The Obstacle & Humorous/Dramatic Tension):** Dynamic low-angle perspective showing the towering odds, character grit, or humorous contrast (e.g. giants laughing while squirrel rolls in sand dust).
* **Scene 3 (The Mentor / Divine Grace):** Breathtaking heroic entrance rendered with volumetric golden hour lighting, radiant colors, and gentle compassion (e.g. Lord Rama kneeling upon wet beach sand, extending his open hand).
* **Scene 4 (Intimate Devotion & Emotional Payoff):** Extreme close-up of intimate connection—hero nestled safely in open palm, gazing up with glassy, teary, glistening eyes filled with pure love and devotion.
* **Scene 5 (Cosmic Transformation & Infinite Loop):** Macro hero climax—divine touch gliding across fur/character, sparkling celestial stardust particles materializing, looping seamlessly back into the opening hook phrase.

---

### 2. 10 Dynamic Camera Cuts Choreography (2 Cuts per Scene)

Never linger on a static frame. Every scene receives **2 distinct camera movements** (3.0s–4.5s each) timed to spoken rhythm:

| Cut # | Scene Target | Cinematography Preset | Emotional Purpose |
| :---: | :--- | :--- | :--- |
| **01** | Scene 1 | `Wide Ocean Crane Down` (`zoompan=z='min(zoom+0.0018,1.22)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'`) | Establishes epic scale and setting |
| **02** | Scene 1 | `Punch-in Hero Focus` (`zoompan=z='min(zoom+0.0028,1.35)':x='iw*0.4':y='ih*0.65'`) | Introduces smallness & determination |
| **03** | Scene 2 | `Low-Angle Tension Tilt` (`zoompan=z='min(zoom+0.002,1.26)':x='iw*0.3':y='ih*0.25'`) | Amplifies scale of the giants/obstacle |
| **04** | Scene 2 | `Character Grit Close-up` (`zoompan=z='min(zoom+0.0025,1.38)':x='iw*0.45':y='ih*0.6'`) | Highlights courage and effort |
| **05** | Scene 3 | `Volumetric Sunset Sweep` (`zoompan=z='min(zoom+0.0016,1.24)':x='iw/2-(iw/zoom/2)':y='ih*0.35'`) | Divine, awe-inspiring presence |
| **06** | Scene 3 | `Slow Downward Push` (`zoompan=z='min(zoom+0.0022,1.3)':x='iw*0.48':y='ih*0.55'`) | Reaching out with compassion |
| **07** | Scene 4 | `Intimate Emotional Zoom` (`zoompan=z='min(zoom+0.0025,1.35)':x='iw*0.45':y='ih*0.45'`) | Pure vulnerability & devoted tears |
| **08** | Scene 4 | `Tender Reaction Glide` (`zoompan=z='min(zoom+0.0018,1.25)':x='iw*0.4':y='ih*0.3'`) | Warm smiling confirmation |
| **09** | Scene 5 | `Macro Hero Slow-Pan` (`zoompan=z='min(zoom+0.0022,1.32)':x='iw*0.42':y='ih*0.5'`) | Divine touch bestowing blessing |
| **10** | Scene 5 | `Luminous Stardust Pull-Back` (`zoompan=z='min(zoom+0.003,1.4)':x='iw*0.45':y='ih*0.45'`) | Celestial magic; loops back to start |

---

### 3. Studio Conversational Vocal Mastering

* **Primary Voice:** `en-US-AndrewMultilingualNeural` (+2% rate) — Conversational podcast warmth with zero robotic buzz.
* **Cultural Lore / Indian English:** `en-IN-PrabhatNeural` (+3% rate).
* **Mastering Chain (FFmpeg):**
  ```bash
  -af "highpass=f=80,lowpass=f=11000,equalizer=f=280:t=q:w=1.0:g=3.0,equalizer=f=3200:t=q:w=1.5:g=-2.5,compand=attacks=0.02:decays=0.2:points=-80/-80|-30/-20|0/-12:soft-knee=6,alimiter=limit=-1.5dB:attack=5:release=50:asc=1"
  ```

---

### 4. Acoustic Scoring & Dynamic Ducking

* Authentic acoustic classical piano or strings (e.g. Erik Satie *Gymnopédie* or tender piano solo).
* Dynamically ducked to **18%–20% volume** during speech with 1.5s fade-in and 2.0s fade-out.

---

### 5. Kinetic Safe-Zone Subtitles

* Word-burst ASS kinetic typography in **Pixar Yellow (`#00FFFF`)** or **Amber Gold (`#00D0FF`)**.
* Font: `Impact` or `Arial Bold` at 78–82pt.
* Thick dark outline (`Outline=6`), shadow 2.
* Positioned strictly at `Y=1450px` (`MarginV=450`), completely avoiding platform headers, bottom audio pills, and right-side engagement buttons.

---

### 6. Production Rule Compliance
* **Rule 8 (Anti-Blur Gate):** Every asset must be native high-definition (minimum 768×1376, >250KB) with crisp 3D RenderMan tactile textures.
* **Rule 9 (Duplicate Prevention):** Always execute `.venv/bin/python scripts/check_youtube_duplicates.py --topic "[TOPIC]"` before starting production.
