from io import BytesIO

import trimesh
from typing_extensions import override

from comfy_api.latest import ComfyExtension, io
from comfy_extras.nodes_save_3d import mesh_item_to_glb_bytes

Trimesh = io.Custom("TRIMESH")


class MeshToTrimesh(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="LiraMeshToTrimesh",
            display_name="Mesh to TRIMESH (UltraTex)",
            category="3d",
            description="Feeds a native MESH (e.g. VaeDecodeShapeTrellis) into UltraTex Prep. "
                        "Goes through the same GLB bytes Save 3D writes, so the axes match UltraTex Load Mesh.",
            inputs=[io.Mesh.Input("mesh")],
            outputs=[Trimesh.Output(display_name="trimesh")],
        )

    @classmethod
    def execute(cls, mesh) -> io.NodeOutput:
        glb = mesh_item_to_glb_bytes(mesh, 0)
        if glb is None:
            raise ValueError("Mesh to TRIMESH: mesh is empty (no vertices/faces).")
        return io.NodeOutput(trimesh.load(BytesIO(glb), file_type="glb", force="mesh"))


class File3DToTrimesh(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="LiraFile3DToTrimesh",
            display_name="3D File to TRIMESH (UltraTex)",
            category="3d",
            description="Feeds a GLB file (e.g. from the Tripo nodes) into UltraTex Prep, keeping its UVs and PBR textures.",
            inputs=[io.Custom("FILE_3D,FILE_3D_GLB").Input("model_3d")],
            outputs=[Trimesh.Output(display_name="trimesh")],
        )

    @classmethod
    def execute(cls, model_3d) -> io.NodeOutput:
        if model_3d.format != "glb":
            raise ValueError(f"3D File to TRIMESH: expected a GLB file, got {model_3d.format or 'unknown'}.")
        return io.NodeOutput(trimesh.load(model_3d.get_data(), file_type="glb", force="mesh"))


class LiraExtension(ComfyExtension):
    @override
    async def get_node_list(self) -> list[type[io.ComfyNode]]:
        return [MeshToTrimesh, File3DToTrimesh]


async def comfy_entrypoint() -> LiraExtension:
    return LiraExtension()
