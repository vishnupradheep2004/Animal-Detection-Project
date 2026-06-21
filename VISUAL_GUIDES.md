# 🎯 ANIMAL DETECTION SYSTEM - VISUAL GUIDES

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│              ANIMAL DETECTION SYSTEM - COMPLETE FLOW                 │
└─────────────────────────────────────────────────────────────────────┘

                          📷 VIDEO INPUT
                    ┌──────────────┬──────────────┐
                    │              │              │
              ┌─────▼────┐   ┌─────▼────┐        │
              │  RTSP    │   │ Webcam   │        │
              │ Camera   │   │ (camera  │        │
              └─────┬────┘   │  .py)    │        │
                    │        └─────┬────┘        │
                    │              │             │
                    └──────────────┼─────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │   YOLO Model Inference     │
                    │   ├─ Load Model            │
                    │   ├─ Set Confidence 0.6   │
                    │   └─ Get Detections       │
                    └──────────────┬──────────────┘
                                   │
            ┌──────────────────────┼──────────────────────┐
            │                      │                      │
       ┌────▼────┐          ┌──────▼──────┐        ┌─────▼──┐
       │Detection │          │   Alert     │        │ Storage│
       │Processing│          │  Management │        │Snapshot│
       │(main)    │          │(telegram    │        │ (snap  │
       │- Boxes   │          │_alerts.py)  │        │_storage│
       │- Classes │          │             │        │ .py)   │
       │- Conf    │          └──────┬──────┘        └─────┬──┘
       └────┬─────┘                 │                     │
            │                ┌──────▼──────┐        ┌─────▼──┐
            │                │ Telegram    │        │  Save  │
            │                │  Bot        │        │ Frame  │
            │                │ • Send msg  │        │ + Box  │
            │                │ • Send img  │        └─────┬──┘
            │                └─────────────┘              │
            │                                    ┌────────▼────────┐
       ┌────▼──────────────────┐         ┌──────▼────────────────┐
       │  Event Logging         │         │  Snapshot Storage    │
       │ (event_logging.py)     │         │ (snapshot_storage.py)│
       │ ├─ SQLite DB           │         │ ├─ Organized by type │
       │ ├─ File Logs           │         │ ├─ Cleanup old files │
       │ ├─ Detection record    │         │ └─ Archive old data  │
       │ └─ Event record        │         └──────────────────────┘
       └────┬──────────────────┘
            │
       ┌────▼──────────────────┐
       │   Dashboard           │
       │ (dashboard.py)        │
       │ ├─ Track stats        │
       │ ├─ Count by class     │
       │ ├─ Detection history  │
       │ └─ Generate HTML      │
       └────┬──────────────────┘
            │
       ┌────▼──────────────────┐
       │ Deployment Manager    │
       │ (deployment.py)       │
       │ ├─ Config management  │
       │ ├─ System monitor     │
       │ ├─ Health checks      │
       │ └─ Export info        │
       └──────────────────────┘
```

---

## Data Flow Diagram

```
FRAME CAPTURE
    │
    ▼
YOLO DETECTION ─────────────────┐
    │                           │
    ├─ Class ID ◄──────────────┘
    ├─ Confidence
    ├─ Bounding Box
    │
    ▼
FILTER & PROCESS
    │
    ├─ Confidence check OK? → YES ─┐
    │                              │
    └─ Skip if below threshold     │
                                   │
                    ┌──────────────▼──────────────┐
                    │  PARALLEL PROCESSING       │
                    ├────────────────────────────┤
                    │                            │
        ┌───────────┼──────────────┬─────────────┤
        │           │              │             │
    ┌───▼───┐   ┌───▼────┐  ┌─────▼───┐  ┌─────▼──┐
    │Telegram│  │ Logging │  │Dashboard│  │Snapshot│
    │Check   │  │ to DB   │  │ Update  │  │ Save   │
    │Throttle│  │ & File  │  │ Stats   │  │ Frame  │
    └───┬───┘  └───┬────┘  └─────┬───┘  └─────┬──┘
        │          │             │            │
        │ Under    │ Record to   │ Update    │ Store
        │ Limit?   │ Detections  │ Counters  │ Location
        │          │ Table       │           │ Create
        ▼          ▼             ▼           ▼ Thumb
    ┌─────────────────────────────────────────┐
    │      ALL DATA PERSISTED                 │
    ├─────────────────────────────────────────┤
    │ • Telegram: Notifications sent          │
    │ • Database: detections.db logged        │
    │ • Dashboard: Stats updated              │
    │ • Storage: Snapshots saved              │
    │ • File: Logs written                    │
    └─────────────────────────────────────────┘
```

---

## Module Dependencies

```
main_integrated.py
    │
    ├─── camera.py
    │    └─ (OpenCV, threading)
    │
    ├─── dashboard.py
    │    ├─ (json)
    │    └─ sqlite3
    │
    ├─── telegram_alerts.py
    │    └─ (requests)
    │
    ├─── event_logging.py
    │    ├─ (logging)
    │    ├─ sqlite3
    │    └─ json
    │
    ├─── snapshot_storage.py
    │    ├─ (cv2)
    │    ├─ pathlib
    │    └─ shutil
    │
    └─── deployment.py
         ├─ (json)
         ├─ psutil
         └─ pathlib
```

---

## Configuration Hierarchy

```
┌─────────────────────────────────┐
│  Environment Variables (.env)   │
│  (Highest Priority)             │
│  • TELEGRAM_BOT_TOKEN           │
│  • TELEGRAM_CHAT_ID             │
│  • CAMERA_TYPE                  │
│  • MODEL_CONFIDENCE             │
└──────────┬──────────────────────┘
           │
           ▼ (if not in .env)
┌─────────────────────────────────┐
│ deployment_config.json          │
│ (JSON Configuration)            │
│ • Camera settings               │
│ • Model path & confidence       │
│ • Telegram credentials          │
│ • Alert thresholds              │
│ • Storage settings              │
└──────────┬──────────────────────┘
           │
           ▼ (if not in config)
┌─────────────────────────────────┐
│  Hardcoded Defaults             │
│  (Lowest Priority)              │
│  • camera_type = "webcam"       │
│  • confidence = 0.6             │
│  • fps = 30                     │
│  • storage_dir = "snapshots"    │
└─────────────────────────────────┘
```

---

## State Flow Diagram

```
                        ┌──────────┐
                        │  START   │
                        └────┬─────┘
                             │
                    ┌────────▼────────┐
                    │  Load Config    │
                    │  & Environment  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Initialize      │
                    │ • Camera        │
                    │ • Model         │
                    │ • Dashboard     │
                    │ • Telegram      │
                    └────────┬────────┘
                             │
                        ┌────▼────┐
                        │ RUNNING  │◄──────┐
                        │ (Loop)   │       │
                        └────┬────┘       │
                             │           │
                    ┌────────▼────────┐  │
                    │ Get Frame       │  │
                    └────────┬────────┘  │
                             │           │
                    ┌────────▼────────┐  │
                    │ Run Detection   │  │
                    └────────┬────────┘  │
                             │           │
                    ┌────────▼────────┐  │
                    │ Process Results │  │
                    │ • Log           │  │
                    │ • Alert         │  │
                    │ • Dashboard     │  │
                    │ • Snapshot      │  │
                    └────────┬────────┘  │
                             │           │
                    ┌────────▼────────┐  │
                    │ Display Frame   │  │
                    └────────┬────────┘  │
                             │           │
                    ┌────────▼────────┐  │
                    │ Handle Input    │  │
                    │ • q = quit      │  │
                    │ • s = snapshot  │  │
                    │ • r = reset     │  │
                    └────────┬────────┘  │
                             │           │
         ┌───────────────────┤           │
         │ q pressed?        └─┬─────────┘
         │                     │
    YES  │                     NO
         │                     │
         ▼                     │
    ┌─────────┐           loop back
    │CLEANUP  │
    └────┬────┘
         │
    ┌────▼────────────┐
    │ Close Camera    │
    │ Close Windows   │
    │ Export Logs     │
    │ Send Summary    │
    └────┬────────────┘
         │
    ┌────▼──┐
    │ STOP  │
    └───────┘
```

---

## Time Sequence Diagram

```
Frame 1
├─ 0ms   ─┐
│         │ Capture & Detect (50ms)
├─ 50ms  ─┤
├─ 60ms  ─┐
│         │ Processing (30ms)
├─ 90ms  ─┤
│ ├─ Log to DB (5ms)
│ ├─ Check Alert (3ms)
│ ├─ Save Snapshot (15ms)
│ └─ Update Dashboard (2ms)
├─ 100ms ─┐
│         │ Display (5ms)
└─ 105ms─ Next Frame

≈ 30 FPS (33.3ms per frame)
Current overhead: ~100ms per frame
Result: ~10ms buffer/frame
```

---

## Storage Organization

```
snapshots/
├── detections/              # All detection snapshots
│   ├── Lion/
│   │   ├── Lion_20240101_120000_000_0_95.jpg
│   │   ├── Lion_20240101_120100_000_0_92.jpg
│   │   └── ...
│   ├── Rabbit/
│   │   ├── Rabbit_20240101_120030_000_0_87.jpg
│   │   └── ...
│   └── ...
├── alerts/                  # Manual alert snapshots
│   ├── alert_Lion_20240101_120500.jpg
│   └── ...
├── archive/                 # Old archived snapshots
│   └── (organized by class)
└── temp/                    # Temporary files

logs/
├── detection_20240101.log   # Daily log file
├── detection_20240102.log
└── detections.db            # SQLite database
    ├── detections table
    └── events table

dashboard_output/
└── index.html               # Generated dashboard
```

---

## Database Schema Visualization

```
detections table
┌─────────┬────────────┬────────────┬────────────┐
│ id      │ timestamp  │ class_name │ confidence │
├─────────┼────────────┼────────────┼────────────┤
│ 1       │ 2024-01-01 │ Lion       │ 0.95       │
│ 2       │ 2024-01-01 │ Rabbit     │ 0.87       │
│ 3       │ 2024-01-01 │ Lion       │ 0.92       │
│ ...     │ ...        │ ...        │ ...        │
└─────────┴────────────┴────────────┴────────────┘
│ x1  │ y1  │ x2  │ y2   │ image_path    │ alert_sent │
├─────┼─────┼─────┼──────┼───────────────┼────────────┤
│ 100 │ 100 │ 200 │ 200  │ snap_001.jpg  │ 1          │
│ 300 │ 300 │ 350 │ 350  │ snap_002.jpg  │ 0          │
│ 150 │ 150 │ 250 │ 250  │ snap_003.jpg  │ 1          │
└─────┴─────┴─────┴──────┴───────────────┴────────────┘

events table
┌──────┬───────────────┬────────────┬─────────────┐
│ id   │ event_type    │ description│ severity    │
├──────┼───────────────┼────────────┼─────────────┤
│ 1    │ System        │ Started    │ INFO        │
│ 2    │ Detection     │ Found lion │ INFO        │
│ 3    │ Error         │ Camera off │ ERROR       │
└──────┴───────────────┴────────────┴─────────────┘
```

---

## Configuration Precedence

```
FINAL CONFIGURATION
        ▲
        │
   .env file (highest priority)
        │
        ▼
deployment_config.json
        │
        ▼
   Hardcoded defaults (lowest priority)

Example - Model Confidence:
1. Check .env: MODEL_CONFIDENCE=0.7
2. If not: Check JSON: "confidence": 0.6
3. If not: Use default: 0.6
```

---

## Error Handling Flow

```
Try Operation
    │
    ├─ SUCCESS ──────┐
    │                │
    └─ EXCEPTION     │
        │            │
        ├─ Log Error  │
        │ (file + db) │
        │            │
        ├─ Create    │
        │ Event      │
        │ Record     │
        │            │
        ├─ Send     │
        │ Alert     │
        │ (Telegram)│
        │            │
        └─ Retry or │
          Fallback   │
                     │
                     ▼
                 Continue
```

---

## Performance Metrics

```
Resource Usage Over Time:

Memory:   ▁▂▂▂▃▃▃▄▄▄▅▅▅▅ (2.5 - 4 GB)
           │ Peak at startup
           │ Stabilizes after warming up

CPU:      ▃▄▃▄▄▅▄▅▅▆▅▆▄▅ (30-60%)
           │ Varies with scene complexity

Disk:     ▁▁▁▂▂▂▃▃▃▄▄▄▅▅ (50MB/hour)
           │ Linear with detection frequency

Network:  ▁▁▂▁▂▂▁▂▁▂▂▁▂▁ (<100 KB/s)
           │ Spikes when sending to Telegram
```

---

## Deployment Options Comparison

```
┌──────────────┬─────────┬─────────┬─────────┐
│ Option       │ Local   │ Docker  │ Cloud   │
├──────────────┼─────────┼─────────┼─────────┤
│ Setup Time   │ 5 min   │ 10 min  │ 20 min  │
│ Maintenance  │ Manual  │ Auto    │ Full    │
│ Scalability  │ Limited │ Good    │ Great   │
│ Cost         │ Free    │ Free    │ $$$     │
│ Portability  │ Low     │ High    │ Very    │
└──────────────┴─────────┴─────────┴─────────┘
```

---

This document provides visual references for understanding the system architecture and data flow.

**For more details, see the comprehensive documentation files.**
