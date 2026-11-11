# ComfyUI-Lira-Nodes

Small helper nodes used by the Lira 3D workflows.

| Node | What it does |
|---|---|
| Mesh to TRIMESH (UltraTex) (`LiraMeshToTrimesh`) | Feeds a native MESH (e.g. from TRELLIS.2) into UltraTex Prep. |
| 3D File to TRIMESH (UltraTex) (`LiraFile3DToTrimesh`) | Feeds a GLB file (e.g. from the Tripo nodes) into UltraTex Prep, keeping its UVs and PBR textures. |

No extra dependencies: uses ComfyUI's own `trimesh`.
