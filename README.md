# 🔥 Intelligent Flare Stack Safety Instrumented System (SIS) & SCADA Panel

An enterprise-grade, closed-loop Safety Instrumented System (SIS) prototype designed for the continuous monitoring of industrial flare stacks. This project integrates hardware sensing with a custom Python-based SCADA (Supervisory Control and Data Acquisition) / HMI (Human-Machine Interface) panel to provide real-time flame-out detection, remote manual overrides, and automated commercial shift accounting.

---

## 📸 System Previews

<details open>
  <summary><b> 1.📸 Video Presentation (Click to expand)</b></summary>
  
**
    > ![Normal Status]([https://github.com/Senann05/Flare_Stack_DCS_Simulation/blob/main/F_S_Images/vid.mp4](https://youtu.be/rYOLZfGKNkU))



</details>

<details>
  <summary><b>🖥️ 2. SCADA HMI Dashboard (Click to expand SCADA HMI)</b></summary>
  <br>
  
  * **Normal:**
    > ![Normal Status](https://github.com/Senann05/Flare_Stack_DCS_Simulation/blob/main/F_S_Images/scada1.jpeg)
    > ![Normal Status](https://github.com/Senann05/Flare_Stack_DCS_Simulation/blob/main/F_S_Images/normal.jpeg)

  
  * **Alert:**
    > ![Normal Status](https://github.com/Senann05/Flare_Stack_DCS_Simulation/blob/main/F_S_Images/alert.jpeg)
      ![Normal Status](https://github.com/Senann05/Flare_Stack_DCS_Simulation/blob/main/F_S_Images/scada2.jpeg)

</details>

<details>
  <summary><b>⚙️ 3. Commercial Shift Accounting- Excel/CSV Log (Click to expand)</b></summary>
  
**
    > ![Normal Status](https://github.com/Senann05/Flare_Stack_DCS_Simulation/blob/main/F_S_Images/l%20ex.jpeg)
    > ![Normal Status](https://github.com/Senann05/Flare_Stack_DCS_Simulation/blob/main/F_S_Images/excel.jpeg)


</details>

<details>
  <summary><b>📊 4.Hardware Prototype Simulation (Click to expand)</b></summary>
  
**
    ![Normal Status](https://github.com/Senann05/Flare_Stack_DCS_Simulation/blob/main/F_S_Images/sim.jpeg)
    ![Normal Status](https://github.com/Senann05/Flare_Stack_DCS_Simulation/blob/main/F_S_Images/normal1.jpeg)
    ![Normal Status](https://github.com/Senann05/Flare_Stack_DCS_Simulation/blob/main/F_S_Images/alert1.jpeg)


</details>
---

## 🏭 Industry Context & Problem Statement

**The Problem:** In Oil & Gas refineries and petrochemical plants, flare stacks are critical safety devices used to burn off excess hydrocarbon gases. A **"Flame-Out"** condition (where the flame is extinguished but gas continues to flow) poses catastrophic risks, leading to the release of highly toxic, unburned hydrocarbons into the atmosphere, creating severe environmental hazards and explosive gas clouds. 

**The Solution:** This system completely removes the reliance on manual visual inspections. It acts as an automated SIS that continuously monitors the flame presence. If a flame-out occurs, it instantly triggers local hardware alarms and alerts the central control room (SCADA) while simultaneously logging the exact timestamp and system state for post-incident analysis.

---

## ✨ Core Features & Engineering Logic

* **Dynamic Thresholding (Day/Night Mode):** The system intelligently adjusts its sensitivity based on the time of day. The SCADA system simulates a 24-hour clock, automatically shifting the baseline threshold during night shifts to compensate for ambient light changes.
* **Automated Commercial Accounting:** Replaces manual data entry with automated logging. Every simulated hour, the system appends a clean, single-line record to a CSV file (easily readable in Excel) detailing the shift mode, safety status, raw flame level, and active threshold.
* **Closed-Loop Feedback System:** Unlike open-loop prototypes, remote commands sent from the SCADA panel (e.g., Mute Alarm, Disable LEDs) wait for hardware confirmation before updating the UI buttons, ensuring the operator always sees the *true* state of the field instruments.
* **Edge-Triggered Hardware Overrides:** Operators in the field can manually acknowledge and mute alarms using physical push buttons with built-in debounce logic, which instantly syncs with the remote SCADA dashboard.

---

## 🧮 Mathematical Modeling & Signal Processing

The system processes analog signals through a 10-bit ADC (Analog-to-Digital Converter), mapping physical states to a scale of `0-1023`. The supervisory control layer applies a mathematical offset to dynamically modify thresholds during low-light cycles without requiring mechanical field recalibration.

---

## 🧰 System Architecture

### Hardware (Field Instruments)
* **Controller:** Arduino Uno (C++ Firmware)
* **Flame Sensor (Simulated):** LDR (Photoresistor) on Analog Pin `A0`
* **Calibration:** Potentiometer on Analog Pin `A1` (for base threshold setting)
* **Annunciators:** Red/Green LEDs and Piezo Buzzer
* **Manual Override:** Tactile Push Button

### Software (Control Room)
* **SCADA Backend:** Python 3 with `pyserial` for robust serial communication.
* **HMI Frontend:** `customtkinter` for a modern, dark-themed industrial interface.
* **Data Management:** Standard `csv` and `os` libraries for commercial data logging and one-click report generation.

---
