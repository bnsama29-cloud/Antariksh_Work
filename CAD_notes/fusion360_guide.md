# Fusion 360 — Complete Step-by-Step Guide
## LOC CubeSat 1U Payload Box (with Realistic Electronics)
### Owner: Aerospace + EC | Deadline: Day 2 (before 18 July)

---

## The Goal
To build a 3D structural model of our Lab-on-a-Chip CubeSat. We will model the main structural shell and the custom biological tray ourselves, but **we will import exact 3D models of the electronics** (Arduino, sensors) to make the render look 100% photorealistic and identical to our Wokwi simulation.

---

## STEP 1 — Download the Electronic Components (GrabCAD)
Instead of drawing rectangles that "look like" an Arduino, we are going to import the real CAD files.

1. Create a free account on **[GrabCAD.com](https://grabcad.com/)**.
2. Search and download the `.step` (or `.f3d` or `.iges`) files for the following components:
   - **"Arduino Uno"** (or Raspberry Pi Zero if preferred for space)
   - **"DHT22 sensor"**
   - **"Geiger Counter Module"** (or just use a generic PCB model to represent the radiation sensor)
   - **"16x2 LCD Display"** (if you want to mount it to the exterior for the render)
   - **"5mm LED"**
3. Save all these downloaded `.step` files into a folder on your computer called `CubeSat_CAD_Parts`.

---

## STEP 2 — New Design & Units
1. Open **Autodesk Fusion 360**
2. Click **File → New Design**
3. Go to **Preferences → Units → Millimeters**
4. Save as: `LOC_CubeSat_1U.f3d`

---

## STEP 3 — Outer Shell (1U CubeSat Box)
*The structural frame follows the exact CubeSat Design Specification (10cm x 10cm x 11.35cm).*

1. Click **Create Sketch** → select **XY Plane**.
2. Draw a **100 mm × 100 mm rectangle** (centre at origin).
3. Click **Finish Sketch**.
4. Click **Extrude** → type **113.5 mm** (upward).
5. Click **Modify → Shell** → select all 6 faces → set Thickness to **1.5 mm**.
   - *This hollows out the cube, leaving only the 1.5mm aerospace-grade aluminum walls.*
6. **Rail guides at corners:**
   - Create a Sketch on the XY plane.
   - At each corner, draw an **8.5 mm × 8.5 mm square**.
   - Extrude upward **113.5 mm**.
7. **Appearance (A):** Press `A` on your keyboard, search for "Aluminum 6061", and drag it onto the shell.

---

## STEP 4 — LOC Chip Tray (3-Chamber Petri Dish)
*This is the custom biological heart of our payload.*

1. Click **Assemble → New Component** → Name it `LOC_Chip`.
2. **Create Sketch** on a new offset plane at **Z = 40 mm** (from the bottom).
3. Draw an **ellipse** (or rectangle with rounded corners) → 80 mm wide × 60 mm tall.
4. Draw **2 vertical lines** dividing it into 3 equal sections (left, centre, right).
5. **Extrude** the entire shape downward by **5 mm** to create the base.
6. **Extrude** the outer rim and the two divider walls upward by **6 mm** to create the three separate chambers (CH-1, CH-2, CH-3).
7. **Appearance (A):** Search for "ABS Plastic - Translucent" or "Acrylic" and apply it so it looks like a clear microfluidic chip.

---

## STEP 5 — Importing and Assembling the Electronics
*Now we bring in the photorealistic downloaded parts.*

1. **Upload to Fusion:** Open your Fusion 360 Data Panel (grid icon, top left) → Click **Upload** → Select all the `.step` files you downloaded from GrabCAD. Wait for them to process.
2. **Import the Arduino:** 
   - Right-click the uploaded Arduino Uno in the Data Panel and select **"Insert into Current Design"**.
   - Use the Move/Copy arrows to position it at the bottom of the CubeSat (Z = 5 mm).
   - Click **Assemble → Joint** (or As-Built Joint) to lock it to the inner wall.
3. **Import the DHT22 Sensor:**
   - Insert it into the design.
   - Position it on the **right inner wall**, hovering near the LOC tray.
   - Create a Joint to lock it to the wall.
4. **Import the LEDs (Nutrient Valves):**
   - Insert the 5mm LED.
   - Duplicate it (Ctrl+C, Ctrl+V).
   - Make one Red and one Green using the Appearance menu.
   - Mount them near the LOC tray to represent the biological valves.
5. **Import the Radiation Sensor / Potentiometer:**
   - Insert it and mount it on the wall opposite the Arduino.

*Because these are imported `.step` files, they already contain all the tiny capacitors, pins, and textures, making your CubeSat look incredibly complex and professional!*

---

## STEP 6 — Cable Routing (Virtual Wires)
*To make it look like a real wired satellite, we will route a few cables.*

1. Create a **3D Sketch** (check the "3D Sketch" box in the sketch palette).
2. Use the **Spline** tool to draw a curvy path from the Arduino GPIO pins to the DHT22 sensor.
3. Click **Finish Sketch**.
4. Click **Create → Pipe**.
5. Select the spline path you just drew. Set Section Size to **1.5 mm**.
6. Set the Operation to **New Body**.
7. Change its Appearance to red, blue, or yellow plastic to look like a wire.
8. Repeat for a few more connections.

---

## STEP 7 — Visual Setup for Report
*We need 3 specific screenshots to paste into the Word document.*

### Fig CAD-1: Isometric Exterior
1. Zoom out so the whole CubeSat is visible.
2. Ensure you are in a nice angle showing the rails and inside.
3. Switch to **Render Workspace**. Click **In-Canvas Render** (let it run for 1 min to get realistic shadows).
4. Export the image as `fig_cad_isometric.png`.

### Fig CAD-2: Section View (Interior Layout)
1. Go back to Design Workspace.
2. Click **Inspect → Section Analysis**.
3. Select the **YZ plane** and push the arrow exactly halfway (so it cuts the CubeSat in half).
4. This reveals how perfectly your Arduino and LOC tray fit inside.
5. Go to Render Workspace and capture the image.
6. Export as `fig_cad_section.png`.
7. Turn off Section Analysis in the browser tree when done.

### Fig CAD-3: Exploded View
1. Switch to the **Animation Workspace** (top-left dropdown).
2. Click **Transform Components**.
3. Click the outer shell and drag it upwards (+Z).
4. Click the LOC tray and drag it slightly upwards.
5. Click the Arduino and leave it at the bottom.
6. This creates a "blow-apart" view showing how everything stacks.
7. Capture the image and save as `fig_cad_exploded.png`.

---

## STEP 8 — Final Submission
1. Save your Fusion file.
2. Take those 3 exported PNGs.
3. Open `LOC_CubeSat_Report_Final.docx`.
4. Scroll to the very end (Section 7.4).
5. Delete the text inside the 3 grey placeholder boxes and paste your actual screenshots inside them.
6. **Save as PDF and Submit!**

---

*Estimated Time: 1 hour for downloading parts, 2 hours for assembly and rendering.*
