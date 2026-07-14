# Fusion 360 — Complete Step-by-Step Guide
## LOC CubeSat 1U Payload Box
### Owner: Aerospace + EC | Deadline: Day 2 (before 18 July)

---

## Reference: What the Final Model Should Look Like

The model has 3 main views for the report:
- **Isometric exterior** — labelled aluminum box with rail guides
- **Section view** — cut through middle showing all internals
- **Exploded view** — all components separated along Z-axis

---

## STEP 1 — New Design & Units

1. Open **Autodesk Fusion 360**
2. Click **File → New Design**
3. Go to **Preferences → Units → Millimeters**
4. Save as: `LOC_CubeSat_1U.f3d`

---

## STEP 2 — Outer Shell (1U CubeSat Box)

**Sketch the shell:**
1. Click **Create Sketch** → select **XY Plane**
2. Draw a **100 mm × 100 mm rectangle** (centre at origin)
3. Click **Finish Sketch**
4. **Extrude** → 113.5 mm (upward)
5. **Modify → Shell** → select all 6 faces → Thickness: **1.5 mm**
   - This removes the interior, leaving only walls

**Rail guides at corners:**
1. Create Sketch on XY plane
2. At each corner: draw **8.5 mm × 8.5 mm square** in each corner
3. Extrude upward **113.5 mm** (these are structural rails)
4. **Appearance**: Set shell body → Search "Aluminum 6061" → Apply

> 💡 Leave one **face open** (top face) — this is where you'll place the LOC chip tray

---

## STEP 3 — LOC Chip Tray (3-Chamber Petri Dish)

1. **New Component** → name it `LOC_Chip`
2. **Create Sketch** on a plane at Z = 30 mm (from bottom)
3. Draw an **ellipse** → 80 mm wide × 60 mm tall
4. Draw **2 vertical lines** dividing it into 3 equal sections (left, centre, right)
5. Each chamber depth: **Extrude** downward **5 mm**
6. Add a **1 mm divider wall** between chambers (extrude up 6 mm)
7. **Appearance**: Set to `ABS Plastic - Translucent`

**Label chambers** (using Text sketch, size 3 mm):
- Left: `CH-1`
- Centre: `CH-2`
- Right: `CH-3`

---

## STEP 4 — Raspberry Pi Boards (×2)

**Pi 1 — Auxiliary Computer (bottom Pi):**
1. **New Component** → `RPi_Aux`
2. **Create Sketch** → draw rectangle **85 mm × 56 mm**
3. Extrude **1.5 mm** (PCB thickness)
4. Position at Z = 10 mm from bottom
5. Add small rectangular bumps for GPIO pins: **2 mm × 5 mm** rows
6. **Appearance**: Set to `PCB Green`

**Pi 2 — Flight Computer (top Pi):**
1. Duplicate **RPi_Aux** → rename to `RPi_Flight`
2. Position at Z = 35 mm (stacked above Pi 1, with 20 mm gap)

---

## STEP 5 — Sensors

### DHT22 (Temperature & Humidity)
1. **New Component** → `DHT22`
2. Sketch: Rectangle **15 mm × 25 mm**
3. Extrude **5 mm**
4. Position: **right inner wall**, at Z = 70 mm
5. Appearance: White plastic

### Radiation Sensors (×2)
1. **New Component** → `RadSensor_CH2`
2. Sketch: Rectangle **20 mm × 20 mm**
3. Extrude **5 mm**
4. Position: **below LOC tray**, at Z = 23 mm
   - Left sensor below CH-2
   - Right sensor below CH-3
5. Duplicate → rename `RadSensor_CH3` → move to right position
6. Appearance: Pink/beige (`Plastic - Light Pink`)

### Camera Module
1. **New Component** → `Camera`
2. Sketch: Rectangle **25 mm × 25 mm**
3. Extrude **8 mm**
4. Position: **directly below LOC tray centre**, Z = 22 mm
5. Add small circle (5 mm diameter) on top face = lens
6. Appearance: Dark grey/black

### LED Lighting Panel
1. **New Component** → `LED_Panel`
2. Sketch: Rectangle **35 mm × 35 mm**
3. Extrude **3 mm**
4. Position: **above LOC tray**, at Z = 90 mm
5. Appearance: White translucent

### RTC Module (Real-Time Clock)
1. **New Component** → `RTC`
2. Rectangle **20 mm × 10 mm**, extrude 3 mm
3. Position: Next to Pi 1, at Z = 12 mm
4. Appearance: PCB Green

---

## STEP 6 — LiPo Battery

1. **New Component** → `Battery_LiPo`
2. Sketch: Rectangle **60 mm × 35 mm**
3. Extrude **10 mm**
4. Position: **very bottom** of shell, Z = 2 mm
5. Appearance: Black matte (`Plastic - Black`)

---

## STEP 7 — Cable Routing (Ribbon Cables)

1. **Sweep** tool → draw 3 curved paths from:
   - Pi 1 → DHT22 (blue ribbon)
   - Pi 2 → Radiation sensors (red ribbon)
   - Pi 1 → Camera (yellow ribbon)
2. Cross-section: Rectangle **5 mm × 1 mm**
3. Appearance: Match color to function

> 💡 Cables don't need to be perfectly routed — just show the connection path

---

## STEP 8 — Joints & Assembly

1. **Assemble → Joint** → mate each component inside the shell
2. Use **As-Built Joint** for simplicity
3. Check: No components overlap (use **Inspect → Interference Detection**)

---

## STEP 9 — Visual Setup for Report

### Section View (for interior shot):
1. **Inspect → Section Analysis**
2. Select the **YZ plane** (cuts through the middle)
3. This reveals all internals — Pi boards, LOC tray, sensors, battery
4. Screenshot → Save as `fig_cad_section_view.png`

### Exploded View:
1. **Assemble → Explode Components**
2. Drag each component along Z-axis to separate them
3. Screenshot → Save as `fig_cad_exploded_view.png`

### Render (high quality):
1. Switch to **Render workspace** (top-left dropdown)
2. Set **Environment**: Studio, White background
3. Click **Render** → wait ~2 min
4. Export as PNG → `fig_cad_render.png`

---

## STEP 10 — Export & Save

```
Save as:  LOC_CubeSat_1U.f3d       (Fusion native)
Export:   LOC_CubeSat_1U.step      (universal CAD)
Export:   LOC_CubeSat_1U.stl       (if 3D print required later)
```

Put all exports in: `CAD_notes/`

---

## 3 Required Report Figures from Fusion

| Figure | View | Description |
|--------|------|-------------|
| **Fig CAD-1** | Isometric exterior | Full shell with labels |
| **Fig CAD-2** | Section view | Interior showing Pi + sensors + LOC tray |
| **Fig CAD-3** | Exploded view | All components separated |

---

## Common Mistakes to Avoid

- ❌ Don't make the wall too thin (< 1.5 mm) — shell command will fail
- ❌ Don't forget to make each component a **separate component** (not just a body)
- ❌ Don't extrude the LOC tray through the shell wall
- ✅ Use **Save** frequently (Ctrl+S)
- ✅ Use **Timeline** at the bottom to undo mistakes

---

## Summary of Dimensions

| Component | Width | Depth | Height |
|-----------|-------|-------|--------|
| Outer shell | 100 mm | 100 mm | 113.5 mm |
| Wall thickness | — | — | 1.5 mm |
| LOC chip tray | 80 mm | 60 mm | 5 mm |
| Raspberry Pi (each) | 85 mm | 56 mm | 1.5 mm |
| DHT22 sensor | 15 mm | 25 mm | 5 mm |
| Radiation sensor | 20 mm | 20 mm | 5 mm |
| Camera module | 25 mm | 25 mm | 8 mm |
| LED panel | 35 mm | 35 mm | 3 mm |
| LiPo battery | 60 mm | 35 mm | 10 mm |

---

*Time estimate: 2–3 hours for a clean model with all labels and views.*
