# KiCad PCB Design — Step-by-Step Procedure
## LOC CubeSat Payload Flight Board

Since you are designing the physical flight board for this payload, here is the exact procedure to layout your custom PCB in KiCad 7.0/8.0.

### The Goal
Create a "Hat" (Shield) that mounts directly onto the Raspberry Pi Zero W. This board will route power from the battery and house the MOSFETs and headers for the sensors, valve, and camera.

---

## Phase 1: Schematic Design (`.sch`)

1. **Open KiCad** and create a New Project named `LOC_Flight_Board`.
2. **Open the Schematic Editor**.
3. **Add the Core Brain:**
   - Press `A` to add a symbol. Search for `Raspberry_Pi_Zero_W` (or a generic 2x20 Pin Header `Conn_02x20_Odd_Even`).
   - Place it in the center.
4. **Add the Power System:**
   - Add a `Battery_Cell` symbol for the 18650.
   - Add a generic Boost Converter symbol (or use a 3-pin header `Conn_01x03` if you are using an off-the-shelf boost module).
   - Connect the Boost Converter's 5V output to **Pin 2 (5V)** and **Pin 6 (GND)** on the Raspberry Pi.
5. **Route the Sensors (Use Headers for external modules):**
   - **DHT22:** Add a `Conn_01x03` header. Connect Pin 1 to Pi's **3.3V (Pin 1)**, Pin 2 to **GPIO 15 (Pin 10)**, and Pin 3 to **GND (Pin 9)**.
   - **Geiger Counter:** Add a `Conn_01x03` header. Connect VCC to **5V (Pin 4)**, GND to **GND (Pin 14)**, and Signal to **GPIO 16 (Pin 36)**.
   - **RTC (DS3231):** Add a `Conn_01x04` header. Connect VCC to **3.3V (Pin 17)**, GND to **GND (Pin 20)**, SDA to **GPIO 2 (Pin 3)**, and SCL to **GPIO 3 (Pin 5)**.
6. **Design the Valve MOSFET Driver:**
   - A Raspberry Pi cannot power a solenoid directly.
   - Add an N-Channel MOSFET (e.g., `IRLZ44N`).
   - Connect the Pi's **GPIO 14 (Pin 8)** to the MOSFET **Gate**. Add a 10k resistor from Gate to GND to keep it closed by default.
   - Connect the MOSFET **Source** to GND.
   - Connect the Solenoid negative terminal (via a `Conn_01x02` header) to the MOSFET **Drain**. Connect the Solenoid positive terminal directly to the **5V rail**.
   - **CRITICAL:** Add a Flyback Diode (e.g., `1N4007`) in parallel with the solenoid header to prevent voltage spikes from frying the Pi when the valve closes!

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
