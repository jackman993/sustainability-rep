# ESG Report Generation System - Minimal UI (English)

## 📁 File Structure

```
esg-minimal-en/
├── app.py                      # Main entry point
└── pages/                      # 7 pages (6 steps + home)
    ├── 0_Home.py
    ├── 1_Carbon_TCFD.py
    ├── 2_Environment.py
    ├── 3_Company.py
    ├── 4_Governance.py
    ├── 5_Merge_Report.py
    └── 6_GRI_Index.py
```

## 🎨 Design Features

- ✅ Minimal white design
- ✅ Clear workflow navigation
- ✅ 6 independent steps + home
- ✅ No complex logic (framework only)
- ✅ Easy to extend

## 🚀 How to Run

```bash
cd esg-minimal-en
streamlit run app.py
```

## 📋 Page Overview

1. **Home** - System introduction and workflow preview
2. **Carbon & TCFD** - Carbon emission calculation and TCFD tables
3. **Environment** - Environment report generation (17 pages)
4. **Company** - Company information and report generation
5. **Governance** - Governance & social report generation
6. **Merge Report** - Merge all sections into complete report
7. **GRI Index** - Generate GRI standards index and download

## 🔄 Workflow

```
Home → Carbon & TCFD → Environment → Company → Governance → Merge → GRI Index
```

## 🔧 Next Steps for Development

- [ ] Integrate actual engines
- [ ] Add API Key management
- [ ] Implement progress tracking
- [ ] Error handling
- [ ] File management
- [ ] Real data processing
