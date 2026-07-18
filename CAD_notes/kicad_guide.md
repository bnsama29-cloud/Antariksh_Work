# KiCad PCB Design — Step-by-Step Procedure
## LOC CubeSat Payload Flight Board

Since you are designing the physical flight board for this payload, here is the exact procedure to layout your custom PCB in KiCad 7.0/8.0.

### The Goal
Create a "Hat" (Shield) that mounts directly onto the Raspberry Pi Zero W. This board will route power from the battery and house the MOSFETs and headers for the sensors, valve, and camera.

---

## Phase 1: Schematic Design (`.sch`) — In-Depth

Since you started from the `RaspberryPi-uHAT` template, the main 40-pin GPIO block (`J1`) is already placed and all the pins have beautiful green text "Labels" (like `GPIO14/TXD0`) attached to them. 

Because those labels exist, you **do not need to draw long, messy wires** connecting your components to the Pi! You just place the same label on your component, and KiCad magically connects them. 

Here is exactly what to add to the schematic next:

### Step 1: Add the Sensor Headers
Instead of drawing complex sensor chips, we use simple "Headers" (connector pins) that you will plug the actual sensors into later.
1. Press **`A`** to open the Add Symbol menu. 
2. Search for `Conn_01x03` (a generic 3-pin header). Place two of these on the screen.
3. Search for `Conn_01x04` (a generic 4-pin header). Place one on the screen.
4. **Name them:** Double-click the `J?` text next to them and name them `DHT22`, `GEIGER`, and `RTC`.

### Step 2: Wire the DHT22 (Temp/Hum)
1. Hover over Pin 1 of the DHT22 header and press **`L`** to add a Label. Type exactly `+3V3` and place the label on the pin.
2. Add a Label to Pin 2 and type exactly `GPIO15/RXD0`.
3. Press **`P`** to open the Power Symbol menu. Search for `GND` and place it on Pin 3.

### Step 3: Wire the Geiger Counter
1. Add a Label to Pin 1 of the Geiger header and type `+5V`.
2. Place a `GND` symbol on Pin 2.
3. Add a Label to Pin 3 and type `GPIO16`.

### Step 4: Wire the RTC (Real-Time Clock)
1. Add a Label to Pin 1 and type `+3V3`.
2. Place a `GND` symbol on Pin 2.
3. Add a Label to Pin 3 (SDA) and type `GPIO02/SDA1`.
4. Add a Label to Pin 4 (SCL) and type `GPIO03/SCL1`.

### Step 5: Build the Valve MOSFET Driver (The only complex part!)
A Raspberry Pi cannot output enough power to click a mechanical solenoid valve open. If you connect it directly, you will fry the Pi! We need a MOSFET to act as a heavy-duty switch.
1. Press **`A`** and search for `IRLZ44N` (a logic-level N-Channel MOSFET). Place it.
2. Press **`A`** and search for `Conn_01x02`. Name it `VALVE`.
3. Press **`A`** and search for `R`. Place a resistor. Double click its value and type `10k`.
4. Press **`A`** and search for `1N4007`. Place this diode.
5. **The Connections (Press `W` to draw wires between these):**
   * **Gate Pin (MOSFET):** Add a label `GPIO14/TXD0`. 
   * **Pull-down:** Connect one side of the 10k resistor to the Gate, and the other side to `GND`. (This ensures the valve defaults to CLOSED).
   * **Source Pin (MOSFET):** Connect directly to `GND`.
   * **Drain Pin (MOSFET):** Connect to Pin 2 of the `VALVE` header.
   * **Valve Power:** Add a label `+5V` to Pin 1 of the `VALVE` header. 
   * **The Protection Diode (CRITICAL):** Connect the `1N4007` diode completely in parallel with the `VALVE` header (Pin 1 to Pin 2). **Make sure the line on the diode symbol (cathode) points towards the `+5V` side!** If you forget this, the reverse voltage spike from the solenoid closing will instantly destroy the MOSFET and the Pi!

### Step 6: Add the Power Input
1. Press **`A`** and search for `Conn_01x02`. Name it `POWER_IN`. 
2. Add a `+5V` label to Pin 1, and a `GND` symbol to Pin 2.
*(Note: You will plug your 18650 Battery + Boost Converter module into this header).*

You are now 100% done with Phase 1! Every component is connected to the Pi via those labels!

---

## Phase 2: PCB Layout (`.kicad_pcb`)

1. **Assign Footprints:** Click the "Run Footprint Assignment Tool" button.
   - Assign `Connector_PinHeader_2.54mm:PinHeader_2x20_P2.54mm_Vertical` to the Raspberry Pi.
   - Assign `Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical` to the sensors.
   - Assign `Package_TO_SOT_THT:TO-220-3_Vertical` to the MOSFET.
2. **Update PCB:** Click `F8` to push the schematic to the PCB Editor.
3. **Set Board Shape (Edge.Cuts):**
   - The Raspberry Pi Zero W has dimensions of **65mm × 30mm**.
   - Select the `Edge.Cuts` layer (yellow) and draw a rectangle exactly 65x30mm.
   - Add four 2.75mm mounting holes in the corners to match the Pi's standoffs.
4. **Place Components:**
   - Place the 40-pin header exactly aligned with the board edge.
   - Arrange the sensor headers along the opposite edge so wires don't cross over the Pi's CPU.
   - Place the MOSFET and flyback diode near the 5V power input.
5. **Route Tracks:**
   - Press `X` to route.
   - Use **0.25mm** track width for signal lines (SDA, SCL, GPIOs).
   - Use **0.8mm** or thicker track width for Power lines (5V, GND, Battery, and the Solenoid path) because they carry higher current.
6. **Add Ground Planes (Copper Pours):**
   - Select the `F.Cu` layer and click "Add a filled zone". Assign it to the `GND` net. Draw a box around the whole board. Repeat for `B.Cu`. This gives you excellent shielding and grounding.

---

## Phase 3: Export for the Report

1. Press `Alt + 3` to open the **3D Viewer** in KiCad.
2. You will see a beautiful, photorealistic 3D render of your custom PCB.
3. Take a screenshot and add it to your project folder as `fig_pcb_design.png`.
4. You can inject this image straight into your Word Document under the "Hardware Architecture" section!
