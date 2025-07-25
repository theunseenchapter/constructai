# ConstructAI 3D Model Generation - File Architecture

## 🏗️ ALL FILES RESPONSIBLE FOR 3D MODEL GENERATION

### 📁 **BACKEND API FILES:**

#### 1. **Main BOQ API Endpoint**
- **File:** `src/app/api/boq/estimate-3d/route.ts`
- **Purpose:** Main API that receives room data and coordinates 3D generation
- **Key Functions:**
  - Receives user room specifications
  - Calls blender-bridge API
  - Returns BOQ data with professional_3d object
  - Manages file paths and response structure

#### 2. **Blender Bridge API**
- **File:** `src/app/api/mcp/blender-bridge/route.ts`
- **Purpose:** Bridge between Node.js and Python 3D generation script
- **Key Functions:**
  - Converts room data to config format
  - Calls Python script
  - Parses Python script response
  - Returns 3D file paths

### 📁 **PYTHON 3D GENERATION:**

#### 3. **Main 3D Generation Script**
- **File:** `architectural_floorplan_wrapper.py`
- **Purpose:** Generates actual 3D model files
- **Key Functions:**
  - Creates OBJ, MTL, BLEND, PNG files
  - Uses timestamp for consistent scene IDs
  - Outputs JSON response with file paths
  - Saves files to public/renders/ directory

### 📁 **FRONTEND COMPONENTS:**

#### 4. **Main UI Component**
- **File:** `src/components/Enhanced3DBOQ.tsx`
- **Purpose:** User interface for 3D model generation
- **Key Functions:**
  - Collects user input (rooms, dimensions)
  - Calls BOQ API
  - Displays result data and debug info
  - Manages result state
  - **ISSUE LOCATION:** Line 648-650 (Result Data display)

#### 5. **3D Model Viewer**
- **File:** `src/components/ThreeJSViewer.tsx`
- **Purpose:** Displays 3D models using Three.js
- **Key Functions:**
  - Loads OBJ/MTL files
  - Renders 3D scene
  - Handles model display and controls

### 📁 **CONFIGURATION FILES:**

#### 6. **Next.js Configuration**
- **File:** `next.config.ts`
- **Purpose:** Handles static file serving for 3D models

#### 7. **Package Dependencies**
- **File:** `package.json`
- **Purpose:** Defines Three.js and other 3D-related dependencies

### 📁 **GENERATED FILES:**

#### 8. **3D Model Files Directory**
- **Directory:** `public/renders/`
- **Purpose:** Stores generated 3D model files
- **File Types:**
  - `.obj` - 3D geometry
  - `.mtl` - Materials
  - `.blend` - Blender files
  - `.png` - Preview images

---

## 🔍 **CURRENT ISSUE ANALYSIS:**

### ✅ **WORKING CORRECTLY:**
1. **API Response:** BOQ API returns correct `professional_3d.blender_files` object
2. **File Generation:** Python script creates all files correctly
3. **File Accessibility:** Files are web-accessible

### ❌ **ISSUE LOCATION:**
**File:** `src/components/Enhanced3DBOQ.tsx` (Lines 648-650)

```tsx
<p>OBJ File: {result.professional_3d?.blender_files?.obj || 'N/A'}</p>
<p>MTL File: {result.professional_3d?.blender_files?.mtl || 'N/A'}</p>
```

**Problem:** The `result` state is not being updated with the API response data.

---

## 🛠️ **DATA FLOW:**

1. **User Input** → Enhanced3DBOQ.tsx
2. **API Call** → `/api/boq/estimate-3d`
3. **BOQ Processing** → route.ts
4. **3D Generation Call** → `/api/mcp/blender-bridge`
5. **Python Execution** → architectural_floorplan_wrapper.py
6. **File Creation** → public/renders/
7. **Response Chain** → blender-bridge → BOQ API → Frontend
8. **State Update** → setResult() in Enhanced3DBOQ.tsx ❌ **BROKEN HERE**
9. **UI Display** → Debug info shows N/A

---

## 🎯 **SPECIFIC FILES TO CHECK:**

### **Primary Issue File:**
- `src/components/Enhanced3DBOQ.tsx` - Result state management

### **Supporting Files:**
- `src/app/api/boq/estimate-3d/route.ts` - API response structure
- `architectural_floorplan_wrapper.py` - File generation
- `src/app/api/mcp/blender-bridge/route.ts` - Response parsing

---

## 📊 **CURRENT STATUS:**

- **Backend:** ✅ Working correctly
- **File Generation:** ✅ Working correctly  
- **API Response:** ✅ Returns correct data
- **Frontend State:** ❌ Not updating with API response
- **UI Display:** ❌ Shows N/A instead of file paths

**Root Cause:** Frontend `result` state is not being properly updated with the API response containing the `blender_files` object.
