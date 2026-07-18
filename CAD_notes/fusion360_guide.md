# Fusion 360 — Complete Step-by-Step Guide
## LOC CubeSat 3U Payload Box (with Realistic Electronics)
### Owner: Aerospace + EC | Deadline: Day 2 (before 18 July)

---

## The Goal
To assemble our Lab-on-a-Chip CubeSat using the exact 3D models we have already downloaded. We will model the custom biological tray ourselves, and assemble the photorealistic electronics (Raspberry Pi, sensors, battery, frame) to make the render look 100% photorealistic and identical to our Wokwi simulation.

---

## STEP 1 — Import Your Local 3D Parts into Fusion 360
You already have all the required files in the `3D parts/` folder of your project repository. Let's get them into Fusion 360.

1. Open **Autodesk Fusion 360**.
2. Click **File → New Design** (or press `Ctrl + N`).
3. Save the file immediately by pressing `Ctrl + S` and name it: `LOC_CubeSat_3U_Master`.
4. Open your **Data Panel** (the grid icon in the top left corner of the screen).
5. Click the blue **Upload** button.
6. Open your computer's File Explorer, navigate to `f:\Downloads\Antariksh_Task\LOC_CubeSat\3D parts\`, and **select everything in that folder** (including the `Satellite` folder, the `.step` files, and `.SLDPRT` files). Drag them all into the Fusion 360 upload window.
7. Click **Upload** and wait for Autodesk's cloud servers to process and translate the SolidWorks and STEP files into Fusion format (this takes 1-2 minutes).

---

## STEP 2 — Assemble the Main Frame
1. In the Data Panel, locate the **`Assembly2`** file (this is the master SolidWorks assembly of the satellite you uploaded). 
2. Right-click **`Assembly2`** and select **"Insert into Current Design"**.
3. It will appear in the center of your screen. Press `Enter` to accept its default position.
4. **CRITICAL STEP:** Right-click the `Assembly2` component in your **Browser Tree** (on the left side of the screen) and select **"Ground"**. A red pin icon will appear. This locks the frame in space so it doesn't accidentally move when you add other parts.
5. **Clean up the frame:** This assembly came with generic ADCS, PCBs, and antennas that we do not want. In your Browser Tree, expand `Assembly2`, find the sub-folders (or components) for `ADCS`, `Antennas`, `PCBs`, and `Solar Panels`, and **delete them or hide them** (by clicking the eye icon). You only want the bare aluminum frame (rails, end plates, and sides).

---

## STEP 3 — Design the Custom LOC Chip Tray (3-Chamber Petri Dish)
*This is the custom biological heart of our payload.*

1. Click **Assemble → New Component** in the top ribbon. Name it `LOC_Chip`.
2. Click **Create Sketch**. Select the internal floor (bottom face) of your CubeSat frame, but offset it by **Z = +80 mm** so it hovers in the middle of the frame.
3. Draw an **ellipse** (or rectangle with rounded corners) that is 80 mm wide × 60 mm tall.
4. Draw **2 vertical lines** dividing it into 3 equal sections (left, centre, right).
5. Click **Finish Sketch**.
6. Click **Extrude (E)**. Select all 3 sections of the ellipse and pull downward by **-5 mm** to create the solid base.
7. Click **Extrude** again. This time, select only the outer rim and the two divider walls, and pull them upward by **+6 mm** to create the three separate chambers (CH-1, CH-2, CH-3).
8. Press **`A`** on your keyboard to open the **Appearance** menu. Search for "ABS Plastic - Translucent" or "Acrylic", and drag it onto the LOC Chip so it looks like a clear microfluidic chip.

---

## STEP 4 — Inserting the Photorealistic Electronics
*Now we snap the sensors and brains into place using the components from your Data Panel.*

1. **Insert the Raspberry Pis:** 
   - Right-click **`Raspberry PI Zero W`** in the Data Panel and select **"Insert into Current Design"**.
   - Use the Move arrows to position it inside the CubeSat at Z = 20 mm (near the bottom).
   - Insert it *again* to get a second board, and stack it at Z = 50 mm.
   - Click **Assemble → Joint (J)**. Select the mounting hole on the Raspberry Pi, and select the mounting rail inside the CubeSat frame to lock them together.
2. **Insert the Camera:**
   - Right-click **`Raspberry Pi Camera`** and insert it.
   - Position it directly below the clear LOC tray, pointing upwards at the biology chambers. Lock it in place with a Joint.
3. **Insert the DHT22 Sensor:**
   - Insert **`DHT22 Module v3`**. Position it on the **left inner wall**, hovering near the LOC tray.
4. **Insert the Radiation Sensor (Geiger Tube):**
   - Insert **`Geiger counter SBM20`**. 
   - Mount this directly underneath the LOC tray, adjacent to the camera. This simulates how we measure radiation hitting the biology.
5. **Insert the Power System:**
   - Insert the **`18650_Bracket`** and **`18650`** battery cells. 
   - Drag them to the very bottom floor of the CubeSat.

---

## STEP 5 — Visual Setup for Report
*We need 3 specific screenshots to paste into the Word document.*

### Fig 13: Isometric Exterior
1. Zoom out so the whole CubeSat is visible.
2. Rotate the view so you are looking down at a 45-degree angle (Isometric view).
3. Switch your workspace from Design to **Render Workspace** (dropdown at top left).
4. Click **In-Canvas Render** (the play button) and let it run for 1 min to generate realistic shadows and reflections on the aluminum and circuit boards.
5. Click **Capture Image** (camera icon) and export the image as `fig_cad_isometric.png`.

### Fig 14: Section View (Interior Layout)
1. Switch back to the **Design Workspace**.
2. Click **Inspect → Section Analysis**.
3. Select the **YZ or XZ plane** (front or side plane) and push the arrow exactly halfway (so it cuts the CubeSat right down the middle like a cake).
4. This reveals how perfectly your dual Raspberry Pis, camera, and LOC tray fit inside the tall frame.
5. Switch to Render Workspace, hit In-Canvas render, and capture the image.
6. Export as `fig_cad_section.png`.
7. Turn off Section Analysis in the browser tree (under the "Analysis" folder) when done.

### Fig 15: Exploded View
1. Switch to the **Animation Workspace** (top-left dropdown).
2. Select the outer aluminum shell in the browser.
3. Click **Transform Components** and drag the shell straight upwards (+Z axis) out of the way.
4. Select the LOC tray and drag it slightly upwards, below the shell.
5. Leave the Raspberry Pis, camera, and battery stacked at the bottom.
6. This creates a brilliant "blow-apart" view showing how all the layers stack together.
7. Capture the image and save as `fig_cad_exploded.png`.

---

## STEP 6 — Final Integration
1. Save your Fusion file (`Ctrl + S`).
2. Move those 3 exported PNGs into your project folder at: `f:\Downloads\Antariksh_Task\LOC_CubeSat\src\figures\`, replacing the existing images there.
3. Open a terminal in that folder and run the document builder:
   ```bash
   python html_to_docx.py
   ```
4. Since the HTML and Word document scripts are already programmed to look for these exact filenames (`fig_cad_isometric.png`, `fig_cad_section.png`, `fig_cad_exploded.png`), your new custom renders will automatically be injected into **Section 3.4** of the HTML and Word reports, as well as the top of your `README.md`. 
5. Commit your changes to git:
   ```bash
   git add src/figures/fig_cad_*.png LOC_CubeSat_Report_v2.docx
   git commit -m "Update CAD renders with custom Fusion 360 models"
   git push
   ```
6. You are completely done!

---

*Estimated Time: 1 to 2 hours for assembly, joints, and rendering.*
