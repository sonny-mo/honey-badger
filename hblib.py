"""
hblib - library functions for honey-badger components.
"""
import clr
from Grasshopper.Kernel import GH_ParamAccess
from GhPython.Assemblies import DotNetCompiledComponent
import Grasshopper
import System
import importlib
import json

def set_up_param(p, name, nickname, description):
    p.Name = name
    p.NickName = nickname
    p.Description = description
    p.Optional = True


# GH_ParamAccess type for input parameters
PARAM_ACCESS_MAP = {
    "item": Grasshopper.Kernel.GH_ParamAccess.item,
    "list": Grasshopper.Kernel.GH_ParamAccess.list,
    "tree": Grasshopper.Kernel.GH_ParamAccess.tree,
}


# Maps badger-file parameter names to the Parameter type to use
# includes all Grasshopper Params
PARAMETER_MAP = {
    'arc': Grasshopper.Kernel.Parameters.Param_Arc,
    'boolean': Grasshopper.Kernel.Parameters.Param_Boolean,
    'box': Grasshopper.Kernel.Parameters.Param_Box,
    'brep': Grasshopper.Kernel.Parameters.Param_Brep,
    'circle': Grasshopper.Kernel.Parameters.Param_Circle,
    'colour': Grasshopper.Kernel.Parameters.Param_Colour,
    'complex': Grasshopper.Kernel.Parameters.Param_Complex,
    'culture': Grasshopper.Kernel.Parameters.Param_Culture,
    'curve': Grasshopper.Kernel.Parameters.Param_Curve,
    'field': Grasshopper.Kernel.Parameters.Param_Field,
    'filepath': Grasshopper.Kernel.Parameters.Param_FilePath,
    'generic': Grasshopper.Kernel.Parameters.Param_GenericObject,
    'geometry': Grasshopper.Kernel.Parameters.Param_Geometry,
    'group': Grasshopper.Kernel.Parameters.Param_Group,
    'guid': Grasshopper.Kernel.Parameters.Param_Guid,
    'integer': Grasshopper.Kernel.Parameters.Param_Integer,
    'interval': Grasshopper.Kernel.Parameters.Param_Interval,
    'interval2d': Grasshopper.Kernel.Parameters.Param_Interval2D,
    'latlonlocation': Grasshopper.Kernel.Parameters.Param_LatLonLocation,
    'line': Grasshopper.Kernel.Parameters.Param_Line,
    'matrix': Grasshopper.Kernel.Parameters.Param_Matrix,
    'mesh': Grasshopper.Kernel.Parameters.Param_Mesh,
    'meshface': Grasshopper.Kernel.Parameters.Param_MeshFace,
    'meshparameters': Grasshopper.Kernel.Parameters.Param_MeshParameters,
    'float': Grasshopper.Kernel.Parameters.Param_Number,
    'oglshader': Grasshopper.Kernel.Parameters.Param_OGLShader,
    'plane': Grasshopper.Kernel.Parameters.Param_Plane,
    'point': Grasshopper.Kernel.Parameters.Param_Point,
    'rectangle': Grasshopper.Kernel.Parameters.Param_Rectangle,
    'scriptvariable': Grasshopper.Kernel.Parameters.Param_ScriptVariable,
    'string': Grasshopper.Kernel.Parameters.Param_String,
    'json': Grasshopper.Kernel.Parameters.Param_String,
    'structurepath': Grasshopper.Kernel.Parameters.Param_StructurePath,
    'surface': Grasshopper.Kernel.Parameters.Param_Surface,
    'time': Grasshopper.Kernel.Parameters.Param_Time,
    'transform': Grasshopper.Kernel.Parameters.Param_Transform,
    'vector': Grasshopper.Kernel.Parameters.Param_Vector,
}


def get_base_class(component):
    """
    Returns a base class to derive from based on the contents of the component dictionary (see badger file)
    :param component:
    :return:
    """
    class HoneyBadgerComponent(DotNetCompiledComponent):
        def __new__(cls, *args, **kwargs):
            if not len(args) == 5:
                args = ('', '', '', '', '')
            return DotNetCompiledComponent.__new__(cls, component['name'],
                                                   component['abbreviation'],
                                                   component['description'],
                                                   component['category'],
                                                   component['subcategory'])

        def get_ComponentGuid(self):
            return System.Guid(component["id"])

        def RegisterInputParams(self, _):
            for input in component['inputs']:
                p = PARAMETER_MAP[input['type']]()
                set_up_param(p, input['name'], input['nick-name'], input['description'])
                p.Access = PARAM_ACCESS_MAP[input["access"]]
                self.Params.Input.Add(p)

        def RegisterOutputParams(self, _):
            for output in component['outputs']:
                p = PARAMETER_MAP[output['type']]()
                set_up_param(p, output['name'], output['nick-name'], output['description'])
                # p.Access = Grasshopper.Kernel.GH_ParamAccess.item
                self.Params.Output.Add(p)

        def get_Internal_Icon_24x24(self):
            if not "icon" in component:
                icon_base64 = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAASDSURBVEhLnZQLUJRVFMcXvmUXRN47I4OQOk5NM2YSBGalmWYDueKEjizrg0DK5GXaSNhUoERINcLwEHeIQClCVEhwyEcSomBMJINoRKiIgMhrP2B3eazgv+/c3YJ1khjOzH/m7P3uOb9zzz17RU8ye5lM7ujkzDs4OGAqOcqcedprDJu+OTrN4ZNV53C9eQTV9UM496sWJ8s1yD0zgNTjPBJy+hCd1g15yCkGMYZN36i6kkoNlvhmwO05BTzlh7H+o068vc8g8v323seanc3sJMaw6RsFqYr78dRiBdwW+WOBuxIBcV0IPNDNRP6mz7rgG9E0c8D+b9V4yf8IFnoosVyhQlBSL4K/6mMif2tiD9ZG3Zw5IPxQL7Yk9LCEoclq7EjlsTPdIPJpbV3U9f8BcF5yc85buCR3YdOErKzmmfz+Rx9kDzLtyhpEeGa/ALiG+ZaWWCwSmcjTQsR7cCK5yIzz4pMzK3Hr3ijq/hzGpWtDKLuqw4kKLY5d0EJVpkVKiRZJxTrEHtchJt+g6Dwt9uRosC6ihp1g9E4BhmrjMHBWgd6jS3AmyAKeYpFaOII7Lv+uw4rQu3gzso1NBl0e9ZdaQFVSIkr66YlhxBWNMJFPa/KwKgboz7eFOnc2elXW6E6zwu1PJOwkDFB6aRAr32uFz652Nn40IXSJ1GdqBVVLCeNLRnHwp4dM5NOa77sVDDBQ6AT+mA36sgRAuhX+ipFOAPJK+/G6EUAzTmO4Ob4Dythb2BzXhG0HGhH8+U1sT2hA6Bf1CIqrxaa91fALq8AyvxTMd3XSa36cBz5PAHxjjZ6MWfjjw0knSP2+zwSwYV8rViqzH7nOddFTdVNpgZtMf/rgwkeaIhcTQEPkJEBsZrdJi3zCb2Cui4u+vDAWY90VGOsswVhHHsbb0jHemoDx29EYa9wBfV0ARqpWQVf2NAYK7ExaVPf+JEBEYqfJJa8KqWXV6VsKoDlpB12JA4bPOmLkZyeMlsuYyKc1+kZ7Hr/k34ItJgCB0W14Nfgu3gi7h7V7OrBcWc0AI42ZQmW20BTZs0RDZY4sKYl8llz4RntYe7KF9mTOQleKJa4qJwFWh7bg5W0t/97DUn/DZAzVJaD/OxsDRKhSW2wP7WmjBJ/W6BvtUedMVP/gkCWubBQbAGbmXrzrC0fx7OpfsGjNRTzvcwHuvucZQHtlNwuk6qgFlGyw0A7qPFt0ZdmgI202WpKs0RwnTE20JeojpajdLmHV57/G0R9NeCGEp8LsP54KAgyeD2JV0dGpv3SJVNV0RMnZU/EkIwB/6i12ZOorAwkTwv/wDDQXt2C4IQ0Pu2pARnuNYdM3CurN9Wb9pEsjEI0fzbgqWArlMg5H3pGgIUoyc8CD1AW4nyhB55dSdH4tZTBS4FIO/h4cAr05XN4gnjmgLd4G7fst0B5vgY4ECYORDivEULxojowAMUpfMZ8ZYI7Mni/cKkHrxxzuxIjRtFuMG2Ec6kI41Cg5VG3kULneHOkrpHAW9hrDpm8ymb2cAqm6qUR7aK8x7DETif4GWQPKTm78ggMAAAAASUVORK5CYII="
            else:
                icon_base64 = component["icon"]
            return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(icon_base64)))

        def SolveInstance(self, DA):
            try:
                main_function = self.locate_main_function()
                inputs = self.prepare_inputs(DA)

                results = main_function(*inputs)

                self.marshal_results(DA, results)
            except:
                import Rhino, traceback
                Rhino.RhinoApp.WriteLine(traceback.format_exc())
                raise

        def marshal_results(self, DA, results):
            if len(component['outputs']) == 1:
                self.marshal.SetOutput(results, DA, 0, True)
            elif len(component['outputs']) > 1:
                for i, r in enumerate(results):
                    self.marshal.SetOutput(r, DA, i, True)

        def prepare_inputs(self, DA):
            inputs = [self.marshal.GetInput(DA, i) for i in range(len(component['inputs']))]
            # handle special input type "json":
            for i, input_definition in enumerate(component['inputs']):
                if input_definition["type"] == "json":
                    try:
                        inputs[i] = json.loads(inputs[i])
                    except:
                        inputs[i] = None
            # apply default values
            for i, input in enumerate(inputs):
                if input is None and "default" in component["inputs"][i]:
                    inputs[i] = component["inputs"][i]["default"]
            return inputs

        def locate_main_function(self):
            main_module = importlib.import_module(component['main-module'])
            if 'main-function' in component:
                main_function = getattr(main_module, component['main-function'])
            else:
                main_function = getattr(main_module, 'main')
            return main_function

    class HoneyBadgerKwargsComponent(HoneyBadgerComponent):
        """pass args to main-function by name instead of by position"""
        def SolveInstance(self, DA):
            try:
                main_function = self.locate_main_function()
                inputs = self.prepare_inputs(DA)

                results = main_function(self.inputs_as_dict(inputs))

                self.marshal_results(DA, results)

            except:
                import Rhino, traceback
                Rhino.RhinoApp.WriteLine(traceback.format_exc())
                raise

        def inputs_as_dict(self, inputs):
            return {
                input_definition["name"]: inputs[i]
                for i, input_definition in enumerate(component["inputs"])
            }

    if component.get("use-kwargs", False):
        return HoneyBadgerKwargsComponent
    else:
        return HoneyBadgerComponent
