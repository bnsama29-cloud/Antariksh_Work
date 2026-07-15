# Fusion 360 — Complete Step-by-Step Guide
## LOC CubeSat 3U Payload Box (with Realistic Electronics)
### Owner: Aerospace + EC | Deadline: Day 2 (before 18 July)

---

## The Goal
To build a 3D structural model of our Lab-on-a-Chip CubeSat. We will model the main structural shell and the custom biological tray ourselves, but **we will import exact 3D models of the electronics** (Raspberry Pi, sensors) to make the render look 100% photorealistic and identical to our Wokwi simulation.

---

## STEP 1 — Download the Electronic Components (GrabCAD)
Instead of drawing rectangles that "look like" an Arduino, we are going to import the real CAD files. GrabCAD Community Library is the industry standard for this.

### Minute Details for GrabCAD Navigation:
1. Open your web browser and navigate directly to the free community library: **`https://grabcad.com/library`** (Do NOT go to the commercial software products page).
2. If you do not have an account, click **"Log In"** at the top right and create a free account (this is mandatory to enable the download buttons).
3. In the search bar at the very top of the library page, search for the following terms one by one:
   - **`3U CubeSat Structure`** (Look for an aluminum rail frame)
   - **`Raspberry Pi Zero W`** (we use two of these)
   - **`DHT22 sensor`** (Look for the white plastic mesh sensor)
   - **`Geiger Counter LND 712`** (or small generic PCBs for radiation sensors)
   - **`Raspberry Pi Camera V2`** (or `OV5647`)
   - **`18650 Battery`** or **`LiPo Battery Pack`**
4. **CRITICAL STEP:** After typing each search term, look at the filter sidebar on the left side of the screen. Under **"Software"**, check the box for **`STEP / IGES`**. This ensures you only see universal 3D models that Fusion 360 can read flawlessly. Avoid `.STL` files (they are just 3D printing meshes and cannot be easily modified).
5. Click on a model that looks realistic and has a high number of likes/downloads.
6. On the model's specific page, look for the big red **"Download files"** button in the top right area and click it. 
7. This will download a `.zip` file to your computer. Repeat this for all 6 components.
8. Create a new folder on your Desktop called `CubeSat_CAD_Parts`.
9. Right-click each downloaded `.zip` file, select **Extract All**, and extract them into the `CubeSat_CAD_Parts` folder. Ensure you can see files ending in `.step` or `.stp`.

---

## STEP 2 — New Design & Import into Fusion 360
1. Open **Autodesk Fusion 360**.
2. Click **File → New Design**.
3. Go to **Preferences → Units → Millimeters**.
4. Save the file immediately by pressing `Ctrl + S` and name it: `LOC_CubeSat_3U_Master`.
5. Open the **Data Panel** (the grid icon in the top left corner of the screen).
6. Click the blue **Upload** button.
7. A window will pop up. Drag and drop all the `.step` files from your `CubeSat_CAD_Parts` folder into this window and click **Upload**. Wait 1-2 minutes for Autodesk's cloud to process them.
8. Once uploaded, right-click the **3U CubeSat Structure** in the Data Panel and select **"Insert into Current Design"**.
9. The frame will appear in the center of your screen. Press `Enter` to accept its position.
10. Right-click the CubeSat structure name in your **Browser Tree** (on the left of the screen) and select **"Ground"**. A small red pin icon will appear. This locks the frame in space so it doesn't accidentally move when you add other parts.

---

## STEP 3 — Outer Shell Adjustments
If the imported 3U CubeSat structure is missing side walls:
1. Click **Create Sketch** → select one of the outer side planes of the rails.
2. Draw a rectangle matching the face of the side wall (approx 100mm x 340.5mm).
3. Click **Finish Sketch**.
4. Click **Extrude** → type **-1.5 mm** (inward) to create an aerospace-grade aluminum wall.
5. Press `A` on your keyboard to open the **Appearance** menu, search for "Aluminum 6061", and drag it onto the new wall.

---

## STEP 4 — LOC Chip Tray (3-Chamber Petri Dish)
*This is the custom biological heart of our payload.*

1. Click **Assemble → New Component** → Name it `LOC_Chip`.
2. **Create Sketch** on the internal XY plane (bottom face) but offset it by **Z = 80 mm**.
3. Draw an **ellipse** (or rectangle with rounded corners) → 80 mm wide × 60 mm tall.
4. Draw **2 vertical lines** dividing it into 3 equal sections (left, centre, right).
5. **Extrude** the entire shape downward by **5 mm** to create the base.
6. **Extrude** the outer rim and the two divider walls upward by **6 mm** to create the three separate chambers (CH-1, CH-2, CH-3).
7. Press `A` for Appearance, search for "ABS Plastic - Translucent" or "Acrylic", and apply it so it looks like a clear microfluidic chip.

---

## STEP 5 — Assembling the Electronics
*Now we snap the photorealistic parts into place.*

1. **Insert the Raspberry Pis:** 
   - Right-click the Raspberry Pi in the Data Panel and select **"Insert into Current Design"**.
   - Use the Move arrows to position it inside the CubeSat at Z = 20 mm.
   - Insert it *again* to get a second board, and stack it at Z = 50 mm.
   - Click **Assemble → Joint (J)** to lock them to the inner mounting rails.
2. **Insert the DHT22 Sensor:**
   - Insert from Data Panel. Position it on the **left inner wall**, hovering near the LOC tray.
   - Create a Joint to lock it to the wall.
3. **Insert the Camera & Battery:**
   - Insert the LiPo battery and drag it to the very bottom floor of the CubeSat.
   - Insert the camera module and position it directly below the clear LOC tray, pointing upwards at the biology.
4. **Insert the Radiation Sensors (Geiger Tubes):**
   - Insert two modules and mount them directly under the LOC tray on the opposite side of the camera.

---

## STEP 6 — Visual Setup for Report
*We need 3 specific screenshots to paste into the Word document.*

### Fig 13: Isometric Exterior
1. Zoom out so the whole CubeSat is visible.
2. Rotate the view so you are looking down at a 45-degree angle (Isometric view).
3. Switch workspace from Design to **Render Workspace** (dropdown top left).
4. Click **In-Canvas Render** (the play button) and let it run for 1 min to generate realistic shadows and reflections.
5. Click **Capture Image** (camera icon) and export the image as `fig_cad_isometric.png`.

### Fig 14: Section View (Interior Layout)
1. Go back to the **Design Workspace**.
2. Click **Inspect → Section Analysis**.
3. Select the **YZ or XZ plane** (front or side) and push the arrow exactly halfway (so it cuts the CubeSat down the middle like a cake).
4. This reveals how perfectly your dual Raspberry Pis, camera, and LOC tray fit inside.
5. Switch to Render Workspace, hit In-Canvas render, and capture the image.
6. Export as `fig_cad_section.png`.
7. Turn off Section Analysis in the browser tree (under "Analysis" folder) when done.

### Fig 15: Exploded View
1. Switch to the **Animation Workspace** (top-left dropdown).
2. Select the outer shell in the browser.
3. Click **Transform Components** and drag the shell straight upwards (+Z axis) out of the way.
4. Select the LOC tray and drag it slightly upwards.
5. Leave the Raspberry Pis, camera, and battery stacked at the bottom.
6. This creates a "blow-apart" view showing how all the layers stack together.
7. Capture the image and save as `fig_cad_exploded.png`.

---

## STEP 7 — Final Integration
1. Save your Fusion file (`Ctrl + S`).
2. Move those 3 exported PNGs into your project folder at: `f:\Downloads\Antariksh_Task\LOC_CubeSat\src\figures\`.
3. Open a terminal in that folder and run:
   ```bash
   python html_to_docx.py
   ```
4. This script will automatically grab your 3 new CAD renders and embed them into Sections 7.4 and 7.5 of your `LOC_CubeSat_Report_v2.docx`. You are completely done!

---

*Estimated Time: 1 hour for downloading parts, 2 hours for assembly and rendering.*
