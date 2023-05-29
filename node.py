import sys
import toolutils

outputitem = None
inputindex = -1
inputitem = None
outputindex = -1

num_args = 1
h_extra_args = ''
pane = toolutils.activePane(kwargs)
if not isinstance(pane, hou.NetworkEditor):
    pane = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    if pane is None:
       hou.ui.displayMessage(
               'Cannot create node: cannot find any network pane')
       sys.exit(0)
else: # We're creating this tool from the TAB menu inside a network editor
    pane_node = pane.pwd()
    if "outputnodename" in kwargs and "inputindex" in kwargs:
        outputitem = pane_node.item(kwargs["outputnodename"])
        inputindex = kwargs["inputindex"]
        h_extra_args += 'set arg4 = "' + kwargs["outputnodename"] + '"\n'
        h_extra_args += 'set arg5 = "' + str(inputindex) + '"\n'
        num_args = 6
    if "inputnodename" in kwargs and "outputindex" in kwargs:
        inputitem = pane_node.item(kwargs["inputnodename"])
        outputindex = kwargs["outputindex"]
        h_extra_args += 'set arg6 = "' + kwargs["inputnodename"] + '"\n'
        h_extra_args += 'set arg9 = "' + str(outputindex) + '"\n'
        num_args = 9
    if "autoplace" in kwargs:
        autoplace = kwargs["autoplace"]
    else:
        autoplace = False
    # If shift-clicked we want to auto append to the current
    # node
    if "shiftclick" in kwargs and kwargs["shiftclick"]:
        if inputitem is None:
            inputitem = pane.currentNode()
            outputindex = 0
    if "nodepositionx" in kwargs and             "nodepositiony" in kwargs:
        try:
            pos = [ float( kwargs["nodepositionx"] ),
                    float( kwargs["nodepositiony"] )]
        except:
            pos = None
    else:
        pos = None

    if not autoplace and not pane.listMode():
        if pos is not None:
            pass
        elif outputitem is None:
            pos = pane.selectPosition(inputitem, outputindex, None, -1)
        else:
            pos = pane.selectPosition(inputitem, outputindex,
                                      outputitem, inputindex)

    if pos is not None:
        if "node_bbox" in kwargs:
            size = kwargs["node_bbox"]
            pos[0] -= size[0] / 2
            pos[1] -= size[1] / 2
        else:
            pos[0] -= 0.573625
            pos[1] -= 0.220625
        h_extra_args += 'set arg2 = "' + str(pos[0]) + '"\n'
        h_extra_args += 'set arg3 = "' + str(pos[1]) + '"\n'
h_extra_args += 'set argc = "' + str(num_args) + '"\n'

pane_node = pane.pwd()
child_type = pane_node.childTypeCategory().nodeTypes()

if 'subnet' not in child_type:
   hou.ui.displayMessage(
           'Cannot create node: incompatible pane network type')
   sys.exit(0)

# First clear the node selection
pane_node.setSelected(False, True)

h_path = pane_node.path()
h_preamble = 'set arg1 = "' + h_path + '"\n'
h_cmd = r'''
if ($argc < 2 || "$arg2" == "") then
   set arg2 = 0
endif
if ($argc < 3 || "$arg3" == "") then
   set arg3 = 0
endif
# Automatically generated script
# $arg1 - the path to add this node
# $arg2 - x position of the tile
# $arg3 - y position of the tile
# $arg4 - input node to wire to
# $arg5 - which input to wire to
# $arg6 - output node to wire to
# $arg7 - the type of this node
# $arg8 - the node is an indirect input
# $arg9 - index of output from $arg6

\set noalias = 1
set saved_path = `execute("oppwf")`
opcf $arg1

# Node $_obj_geo1_FrustumCameraOT (Sop/subnet)
set _obj_geo1_FrustumCameraOT = `run("opadd -e -n -v subnet FrustumCameraOT")`
oplocate -x `$arg2 + 0` -y `$arg3 + 0` $_obj_geo1_FrustumCameraOT
opspareds '    parm {         name    "label1"         baseparm         label   "Input #1 Label"         invisible         export  dialog     }     parm {         name    "label2"         baseparm         label   "Input #2 Label"         invisible         export  dialog     }     parm {         name    "label3"         baseparm         label   "Input #3 Label"         invisible         export  dialog     }     parm {         name    "label4"         baseparm         label   "Input #4 Label"         invisible         export  dialog     }     groupsimple {         name    "frustumsettings"         label   "Frustum Settings"          parm {             name    "cam"             label   "Camera"             type    oppath             default { "" }             parmtag { "oprelative" "." }             parmtag { "script_callback_language" "python" }         }         parm {             name    "upperpadd"             label   "Upper Padding"             type    vector2             size    2             default { "0" "0" }             range   { -1 1 }             parmtag { "script_callback_language" "python" }         }         parm {             name    "lowerpadd"             label   "Lower Padding"             type    vector2             size    2             default { "0" "0" }             range   { -1 1 }             parmtag { "script_callback_language" "python" }         }         parm {             name    "depthpadd"             label   "Depth Padding"             type    vector2             size    2             default { "0" "100" }             range   { -1 1 }             parmtag { "script_callback_language" "python" }         }         parm {             name    "timestep"             label   "Start End Step"             type    intvector             size    3             default { "$FSTART" "$FEND" "5" }             range   { -1 1 }             parmtag { "script_callback_language" "python" }         }         parm {             name    "sepparm"             label   "Spacer"             type    separator             default { "" }             parmtag { "sidefx::layout_height" "small" }             parmtag { "sidefx::look" "blank" }         }         parm {             name    "currentf"             label   "Current Frame"             type    toggle             default { "0" }             parmtag { "script_callback_language" "python" }         }         parm {             name    "vis_frustum"             label   "Visualize Frustum"             type    toggle             default { "0" }             parmtag { "script_callback_language" "python" }         }         parm {             name    "color"             label   "Color Guide"             type    color             size    3             default { "0" "0" "1" }             hidewhen "{ vis_frustum == 0 }"             range   { 0 1 }             parmtag { "script_callback_language" "python" }             parmtag { "units" "" }         }     }      groupsimple {         name    "outputsettings"         label   "Output Settings"          parm {             name    "mode"             label   "Mode"             type    oplist             default { "0" }             menu {                 "0" "Group"                 "1" "Cull"                 "2" "Color"                 "3" "Attribute"             }             parmtag { "oprelative" "/" }             parmtag { "script_callback_language" "python" }         }         parm {             name    "groupname"             label   "Group Name"             type    string             default { "__in_frustum" }             hidewhen "{ mode != 0 }"             parmtag { "script_callback_language" "python" }         }         parm {             name    "attname"             label   "Attribute Name"             type    string             default { "mask" }             hidewhen "{ mode != 3 }"             parmtag { "script_callback_language" "python" }         }         parm {             name    "type"             label   "Type"             type    oplist             default { "2" }             hidewhen "{ mode != 3 }"             menu {                 "1" "Primitive"                 "2" "Point"                 "3" "Vertex"             }             parmtag { "oprelative" "/" }             parmtag { "script_callback_language" "python" }         }         parm {             name    "colorgroup"             label   "Color"             type    color             size    3             default { "1" "0" "0" }             hidewhen "{ mode != 2 }"             range   { 0 1 }             parmtag { "script_callback_language" "python" }             parmtag { "units" "" }         }         parm {             name    "removdegprims"             label   "Remove Degenerate Primitives"             type    toggle             default { "1" }             hidewhen "{ mode != 1 }"             parmtag { "script_callback_language" "python" }         }         parm {             name    "typedel"             label   "Type"             type    oplist             default { "1" }             hidewhen "{ mode != 1 }"             menu {                 "0" "Primitives"                 "1" "Points"             }             parmtag { "oprelative" "/" }             parmtag { "script_callback_language" "python" }         }     }  ' $_obj_geo1_FrustumCameraOT
chblockbegin
chadd -t 41.666666666666664 41.666666666666664 $_obj_geo1_FrustumCameraOT timestepx
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F '$FSTART' $_obj_geo1_FrustumCameraOT/timestepx
chadd -t 41.666666666666664 41.666666666666664 $_obj_geo1_FrustumCameraOT timestepy
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F '$FEND' $_obj_geo1_FrustumCameraOT/timestepy
chblockend
opparm -V 19.0.383 $_obj_geo1_FrustumCameraOT
opcolor -c 0.3059999942779541 0.3059999942779541 0.3059999942779541 $_obj_geo1_FrustumCameraOT
opset -d on -r on -h off -f off -y off -t off -l off -s off -u off -F off -c on -e on -b off $_obj_geo1_FrustumCameraOT
opexprlanguage -s hscript $_obj_geo1_FrustumCameraOT
opuserdata -n 'nodeshape' -v 'camera' $_obj_geo1_FrustumCameraOT
opuserdata -n 'wirestyle' -v 'rounded' $_obj_geo1_FrustumCameraOT
opcf $_obj_geo1_FrustumCameraOT

# Node $_obj_geo1_FrustumCameraOT_clean_polys (Sop/clean)
set _obj_geo1_FrustumCameraOT_clean_polys = `run("opadd -e -n -v clean clean_polys")`
oplocate -x `$arg2 + 1.2158515681357014` -y `$arg3 + -1.0563238430712509` $_obj_geo1_FrustumCameraOT_clean_polys
chblockbegin
chadd -t 0 0 $_obj_geo1_FrustumCameraOT_clean_polys deldegengeo
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../removdegprims")' $_obj_geo1_FrustumCameraOT_clean_polys/deldegengeo
chblockend
opparm $_obj_geo1_FrustumCameraOT_clean_polys deldegengeo ( deldegengeo ) delunusedpts ( off )
chautoscope $_obj_geo1_FrustumCameraOT_clean_polys +delete_small
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_FrustumCameraOT_clean_polys
opexprlanguage -s hscript $_obj_geo1_FrustumCameraOT_clean_polys
opuserdata -n '___Version___' -v '' $_obj_geo1_FrustumCameraOT_clean_polys
opcf ..
opcf $_obj_geo1_FrustumCameraOT

# Node $_obj_geo1_FrustumCameraOT___in_frustum_SEQ (Sop/groupcreate)
set _obj_geo1_FrustumCameraOT___in_frustum_SEQ = `run("opadd -e -n -v groupcreate __in_frustum_SEQ")`
oplocate -x `$arg2 + 1.2158515681357014` -y `$arg3 + 3.5535581569287489` $_obj_geo1_FrustumCameraOT___in_frustum_SEQ
opparm -V 19.0.383 $_obj_geo1_FrustumCameraOT___in_frustum_SEQ groupname ( __in_frustum ) grouptype ( point ) mergeop ( union ) groupbase ( off ) groupbounding ( on ) boundtype ( usebobject )
opset -d off -r off -h on -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_FrustumCameraOT___in_frustum_SEQ
opexprlanguage -s hscript $_obj_geo1_FrustumCameraOT___in_frustum_SEQ
opuserdata -n '___Version___' -v '19.0.383' $_obj_geo1_FrustumCameraOT___in_frustum_SEQ

# Node $_obj_geo1_FrustumCameraOT___in_frustum (Sop/groupcreate)
set _obj_geo1_FrustumCameraOT___in_frustum = `run("opadd -e -n -v groupcreate __in_frustum")`
oplocate -x `$arg2 + 1.2158515681357014` -y `$arg3 + 4.7447541569287495` $_obj_geo1_FrustumCameraOT___in_frustum
opparm -V 19.0.383 $_obj_geo1_FrustumCameraOT___in_frustum groupname ( __in_frustum ) grouptype ( point ) mergeop ( union ) groupbase ( off ) groupbounding ( on ) boundtype ( usebobject )
opset -d on -r on -h on -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_FrustumCameraOT___in_frustum
opexprlanguage -s hscript $_obj_geo1_FrustumCameraOT___in_frustum
opuserdata -n '___Version___' -v '19.0.383' $_obj_geo1_FrustumCameraOT___in_frustum

# Node $_obj_geo1_FrustumCameraOT_set_first_frame (Sop/timeshift)
set _obj_geo1_FrustumCameraOT_set_first_frame = `run("opadd -e -n -v timeshift set_first_frame")`
oplocate -x `$arg2 + 9.9754615681357013` -y `$arg3 + 8.4156561569287476` $_obj_geo1_FrustumCameraOT_set_first_frame
chblockbegin
chadd -t 0 0 $_obj_geo1_FrustumCameraOT_set_first_frame frame
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../timestepx")' $_obj_geo1_FrustumCameraOT_set_first_frame/frame
chadd -t 0 0 $_obj_geo1_FrustumCameraOT_set_first_frame time
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F '$T' $_obj_geo1_FrustumCameraOT_set_first_frame/time
chadd -t 0 0 $_obj_geo1_FrustumCameraOT_set_first_frame frange1
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F '$FSTART' $_obj_geo1_FrustumCameraOT_set_first_frame/frange1
chadd -t 0 0 $_obj_geo1_FrustumCameraOT_set_first_frame frange2
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F '$FEND' $_obj_geo1_FrustumCameraOT_set_first_frame/frange2
chadd -t 0 0 $_obj_geo1_FrustumCameraOT_set_first_frame trange1
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F '$TSTART' $_obj_geo1_FrustumCameraOT_set_first_frame/trange1
chadd -t 0 0 $_obj_geo1_FrustumCameraOT_set_first_frame trange2
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F '$TEND' $_obj_geo1_FrustumCameraOT_set_first_frame/trange2
chblockend
opparm -V 19.0.383 $_obj_geo1_FrustumCameraOT_set_first_frame frame ( frame )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_FrustumCameraOT_set_first_frame
opexprlanguage -s hscript $_obj_geo1_FrustumCameraOT_set_first_frame
opuserdata -n '___Version___' -v '19.0.383' $_obj_geo1_FrustumCameraOT_set_first_frame

# Node $_obj_geo1_FrustumCameraOT_source_frustum (Sop/box)
set _obj_geo1_FrustumCameraOT_source_frustum = `run("opadd -e -n -v box source_frustum")`
oplocate -x `$arg2 + 1.2158515681357014` -y `$arg3 + 10.321226156928748` $_obj_geo1_FrustumCameraOT_source_frustum
opparm -V 19.0.383 $_obj_geo1_FrustumCameraOT_source_frustum type ( polymesh ) divrate ( 2 2 2 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_FrustumCameraOT_source_frustum
opexprlanguage -s hscript $_obj_geo1_FrustumCameraOT_source_frustum
opuserdata -n '___Version___' -v '19.0.383' $_obj_geo1_FrustumCameraOT_source_frustum

# Node $_obj_geo1_FrustumCameraOT_deform_frustum (Sop/attribwrangle)
set _obj_geo1_FrustumCameraOT_deform_frustum = `run("opadd -e -n -v attribwrangle deform_frustum")`
oplocate -x `$arg2 + 1.2158515681357014` -y `$arg3 + 9.1917261569287483` $_obj_geo1_FrustumCameraOT_deform_frustum
opspareds '    group {         name    "folder1"         label   "Code"          parm {             name    "group"             baseparm             label   "Group"             export  none             bindselector points "Modify Points"                 "Select the points to affect and press Enter to complete."                 0 1 0xffffffff 0 grouptype 0         }         parm {             name    "grouptype"             baseparm             label   "Group Type"             export  none         }         parm {             name    "class"             baseparm             label   "Run Over"             export  none         }         parm {             name    "vex_numcount"             baseparm             label   "Number Count"             export  none         }         parm {             name    "vex_threadjobsize"             baseparm             label   "Thread Job Size"             export  none         }         parm {             name    "snippet"             baseparm             label   "VEXpression"             export  all         }         parm {             name    "exportlist"             baseparm             label   "Attributes to Create"             export  none         }         parm {             name    "vex_strict"             baseparm             label   "Enforce Prototypes"             export  none         }     }      group {         name    "folder1_1"         label   "Bindings"          parm {             name    "autobind"             baseparm             label   "Autobind by Name"             export  none         }         multiparm {             name    "bindings"             label    "Number of Bindings"             baseparm             default 0             parmtag { "autoscope" "0000000000000000" }             parmtag { "multistartoffset" "1" }              parm {                 name    "bindname#"                 baseparm                 label   "Attribute Name"                 export  none             }             parm {                 name    "bindparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "groupautobind"             baseparm             label   "Autobind Groups by Name"             export  none         }         multiparm {             name    "groupbindings"             label    "Group Bindings"             baseparm             default 0             parmtag { "autoscope" "0000000000000000" }             parmtag { "multistartoffset" "1" }              parm {                 name    "bindgroupname#"                 baseparm                 label   "Group Name"                 export  none             }             parm {                 name    "bindgroupparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "vex_cwdpath"             baseparm             label   "Evaluation Node Path"             export  none         }         parm {             name    "vex_outputmask"             baseparm             label   "Export Parameters"             export  none         }         parm {             name    "vex_updatenmls"             baseparm             label   "Update Normals If Displaced"             export  none         }         parm {             name    "vex_matchattrib"             baseparm             label   "Attribute to Match"             export  none         }         parm {             name    "vex_inplace"             baseparm             label   "Compute Results In Place"             export  none         }         parm {             name    "vex_selectiongroup"             baseparm             label   "Output Selection Group"             export  none         }         parm {             name    "vex_precision"             baseparm             label   "VEX Precision"             export  none         }     }      parm {         name    "expand_x_low"         label   "Expand X Low"         type    float         default { "0" }         range   { 0 1 }     }     parm {         name    "expand_x_upper"         label   "Expand X Upper"         type    float         default { "0" }         range   { 0 1 }     }     parm {         name    "expand_y_upper"         label   "Expand Y Upper"         type    float         default { "0" }         range   { 0 1 }     }     parm {         name    "expand_y_low"         label   "Expand Y Low"         type    float         default { "0" }         range   { 0 1 }     }     parm {         name    "camera"         label   "Camera"         type    string         default { "" }     }     parm {         name    "near_clip"         label   "Near Clip"         type    float         default { "0" }         range   { 0 1 }     }     parm {         name    "far_clip"         label   "Far Clip"         type    float         default { "0" }         range   { 0 1 }     } ' $_obj_geo1_FrustumCameraOT_deform_frustum
opparm $_obj_geo1_FrustumCameraOT_deform_frustum  bindings ( 0 ) groupbindings ( 0 )
chblockbegin
chadd -t 0 0 $_obj_geo1_FrustumCameraOT_deform_frustum expand_x_low
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../lowerpaddx")' $_obj_geo1_FrustumCameraOT_deform_frustum/expand_x_low
chadd -t 0 0 $_obj_geo1_FrustumCameraOT_deform_frustum expand_x_upper
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../upperpaddx")' $_obj_geo1_FrustumCameraOT_deform_frustum/expand_x_upper
chadd -t 0 0 $_obj_geo1_FrustumCameraOT_deform_frustum expand_y_upper
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../lowerpaddy")' $_obj_geo1_FrustumCameraOT_deform_frustum/expand_y_upper
chadd -t 0 0 $_obj_geo1_FrustumCameraOT_deform_frustum expand_y_low
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../upperpaddy")' $_obj_geo1_FrustumCameraOT_deform_frustum/expand_y_low
chadd -t 0 0 $_obj_geo1_FrustumCameraOT_deform_frustum near_clip
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../depthpaddx")' $_obj_geo1_FrustumCameraOT_deform_frustum/near_clip
chadd -t 0 0 $_obj_geo1_FrustumCameraOT_deform_frustum far_clip
chkey -t 0 -v 5 -m 0 -a 0 -A 0 -T a  -F 'ch("../depthpaddy")' $_obj_geo1_FrustumCameraOT_deform_frustum/far_clip
chblockend
opparm $_obj_geo1_FrustumCameraOT_deform_frustum snippet ( 'vector bbox_max = getbbox_max(0);\nvector bbox_min = getbbox_min(0);\nvector pos = @P;\npos += set(bbox_max.x, bbox_max.y, bbox_min.z);\n\n\nvector relbbox = relbbox(0, pos);\n\nif(relbbox.x==0.5){\n    pos.x -= chf(\'expand_x_low\');\n}\nif(relbbox.x==1.5){\n    pos.x += chf(\'expand_x_upper\');\n}\nif(relbbox.y==1.5){\n    pos.y += chf(\'expand_y_low\');\n}\nif(relbbox.y==0.5){\n    pos.y -= chf(\'expand_y_upper\');\n}\nif(relbbox.z==0.5){\n    pos.z -= chf(\'near_clip\');\n}\nif(relbbox.z==-0.5){\n    pos.z -= chf(\'far_clip\');\n}\n@P = fromNDC(chsop(\'camera\'), pos);\n' ) expand_x_low ( expand_x_low ) expand_x_upper ( expand_x_upper ) expand_y_upper ( expand_y_upper ) expand_y_low ( expand_y_low ) camera ( '`chsop("../cam")`' ) near_clip ( near_clip ) far_clip ( far_clip )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_FrustumCameraOT_deform_frustum
opexprlanguage -s hscript $_obj_geo1_FrustumCameraOT_deform_frustum
opuserdata -n '___Version___' -v '' $_obj_geo1_FrustumCameraOT_deform_frustum

# Node $_obj_geo1_FrustumCameraOT_switch_vis_frustum (Sop/switch)
set _obj_geo1_FrustumCameraOT_switch_vis_frustum = `run("opadd -e -n -v switch switch_vis_frustum")`
oplocate -x `$arg2 + 1.2158515588224712` -y `$arg3 + -5.5433738430712518` $_obj_geo1_FrustumCameraOT_switch_vis_frustum
chblockbegin
chadd -t 0 0 $_obj_geo1_FrustumCameraOT_switch_vis_frustum input
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../vis_frustum")' $_obj_geo1_FrustumCameraOT_switch_vis_frustum/input
chblockend
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_FrustumCameraOT_switch_vis_frustum
opexprlanguage -s hscript $_obj_geo1_FrustumCameraOT_switch_vis_frustum
opuserdata -n '___Version___' -v '19.0.383' $_obj_geo1_FrustumCameraOT_switch_vis_frustum

# Node $_obj_geo1_FrustumCameraOT_draw_line (Sop/convertline)
set _obj_geo1_FrustumCameraOT_draw_line = `run("opadd -e -n -v convertline draw_line")`
oplocate -x `$arg2 + 8.0852415681357019` -y `$arg3 + -3.2282838430712513` $_obj_geo1_FrustumCameraOT_draw_line
opparm $_obj_geo1_FrustumCameraOT_draw_line computelength ( off )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_FrustumCameraOT_draw_line
opexprlanguage -s hscript $_obj_geo1_FrustumCameraOT_draw_line
opuserdata -n '___Version___' -v '' $_obj_geo1_FrustumCameraOT_draw_line

# Node $_obj_geo1_FrustumCameraOT_set_color_line (Sop/attribwrangle)
set _obj_geo1_FrustumCameraOT_set_color_line = `run("opadd -e -n -v attribwrangle set_color_line")`
oplocate -x `$arg2 + 8.0822415681357018` -y `$arg3 + -4.2717538430712514` $_obj_geo1_FrustumCameraOT_set_color_line
opspareds '    group {         name    "folder1"         label   "Code"          parm {             name    "group"             baseparm             label   "Group"             export  none             bindselector points "Modify Points"                 "Select the points to affect and press Enter to complete."                 0 1 0xffffffff 0 grouptype 0         }         parm {             name    "grouptype"             baseparm             label   "Group Type"             export  none         }         parm {             name    "class"             baseparm             label   "Run Over"             export  none         }         parm {             name    "vex_numcount"             baseparm             label   "Number Count"             export  none         }         parm {             name    "vex_threadjobsize"             baseparm             label   "Thread Job Size"             export  none         }         parm {             name    "snippet"             baseparm             label   "VEXpression"             export  all         }         parm {             name    "exportlist"             baseparm             label   "Attributes to Create"             export  none         }         parm {             name    "vex_strict"             baseparm             label   "Enforce Prototypes"             export  none         }     }      group {         name    "folder1_1"         label   "Bindings"          parm {             name    "autobind"             baseparm             label   "Autobind by Name"             export  none         }         multiparm {             name    "bindings"             label    "Number of Bindings"             baseparm             default 0             parmtag { "autoscope" "0000000000000000" }             parmtag { "multistartoffset" "1" }              parm {                 name    "bindname#"                 baseparm                 label   "Attribute Name"                 export  none             }             parm {                 name    "bindparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "groupautobind"             baseparm             label   "Autobind Groups by Name"             export  none         }         multiparm {             name    "groupbindings"             label    "Group Bindings"             baseparm             default 0             parmtag { "autoscope" "0000000000000000" }             parmtag { "multistartoffset" "1" }              parm {                 name    "bindgroupname#"                 baseparm                 label   "Group Name"                 export  none             }             parm {                 name    "bindgroupparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "vex_cwdpath"             baseparm             label   "Evaluation Node Path"             export  none         }         parm {             name    "vex_outputmask"             baseparm             label   "Export Parameters"             export  none         }         parm {             name    "vex_updatenmls"             baseparm             label   "Update Normals If Displaced"             export  none         }         parm {             name    "vex_matchattrib"             baseparm             label   "Attribute to Match"             export  none         }         parm {             name    "vex_inplace"             baseparm             label   "Compute Results In Place"             export  none         }         parm {             name    "vex_selectiongroup"             baseparm             label   "Output Selection Group"             export  none         }         parm {             name    "vex_precision"             baseparm             label   "VEX Precision"             export  none         }     }      parm {         name    "color_line"         label   "Color Line"         type    vector         size    3         default { "0" "0" "0" }         range   { 0 1 }     } ' $_obj_geo1_FrustumCameraOT_set_color_line
opparm $_obj_geo1_FrustumCameraOT_set_color_line  bindings ( 0 ) groupbindings ( 0 )
chblockbegin
chadd -t 0 0 $_obj_geo1_FrustumCameraOT_set_color_line color_linex
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../colorr")' $_obj_geo1_FrustumCameraOT_set_color_line/color_linex
chadd -t 0 0 $_obj_geo1_FrustumCameraOT_set_color_line color_liney
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../colorg")' $_obj_geo1_FrustumCameraOT_set_color_line/color_liney
chadd -t 0 0 $_obj_geo1_FrustumCameraOT_set_color_line color_linez
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../colorb")' $_obj_geo1_FrustumCameraOT_set_color_line/color_linez
chblockend
opparm $_obj_geo1_FrustumCameraOT_set_color_line snippet ( '@Cd = chv(\'color_line\');' ) color_line ( color_linex color_liney color_linez )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_FrustumCameraOT_set_color_line
opexprlanguage -s hscript $_obj_geo1_FrustumCameraOT_set_color_line
opuserdata -n '___Version___' -v '' $_obj_geo1_FrustumCameraOT_set_color_line

# Node $_obj_geo1_FrustumCameraOT_switch_mode (Sop/switch)
set _obj_geo1_FrustumCameraOT_switch_mode = `run("opadd -e -n -v switch switch_mode")`
oplocate -x `$arg2 + 1.2158515588224712` -y `$arg3 + -3.1209938430712514` $_obj_geo1_FrustumCameraOT_switch_mode
chblockbegin
chadd -t 0 0 $_obj_geo1_FrustumCameraOT_switch_mode input
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../mode")' $_obj_geo1_FrustumCameraOT_switch_mode/input
chblockend
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_FrustumCameraOT_switch_mode
opexprlanguage -s hscript $_obj_geo1_FrustumCameraOT_switch_mode
opuserdata -n '___Version___' -v '19.0.383' $_obj_geo1_FrustumCameraOT_switch_mode

# Node $_obj_geo1_FrustumCameraOT_cull_polys (Sop/blast)
set _obj_geo1_FrustumCameraOT_cull_polys = `run("opadd -e -n -v blast cull_polys")`
oplocate -x `$arg2 + 1.2158515681357014` -y `$arg3 + -0.047383843071250986` $_obj_geo1_FrustumCameraOT_cull_polys
opparm -V 19.0.383 $_obj_geo1_FrustumCameraOT_cull_polys group ( __in_frustum ) negate ( on )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_FrustumCameraOT_cull_polys
opexprlanguage -s hscript $_obj_geo1_FrustumCameraOT_cull_polys
opuserdata -n '___Version___' -v '19.0.383' $_obj_geo1_FrustumCameraOT_cull_polys

# Node $_obj_geo1_FrustumCameraOT_set_color_mask (Sop/attribwrangle)
set _obj_geo1_FrustumCameraOT_set_color_mask = `run("opadd -e -n -v attribwrangle set_color_mask")`
oplocate -x `$arg2 + 3.7531615681357016` -y `$arg3 + -1.0573238430712513` $_obj_geo1_FrustumCameraOT_set_color_mask
opspareds '    group {         name    "folder1"         label   "Code"          parm {             name    "group"             baseparm             label   "Group"             export  none             bindselector points "Modify Points"                 "Select the points to affect and press Enter to complete."                 0 1 0xffffffff 0 grouptype 0         }         parm {             name    "grouptype"             baseparm             label   "Group Type"             export  none         }         parm {             name    "class"             baseparm             label   "Run Over"             export  none         }         parm {             name    "vex_numcount"             baseparm             label   "Number Count"             export  none         }         parm {             name    "vex_threadjobsize"             baseparm             label   "Thread Job Size"             export  none         }         parm {             name    "snippet"             baseparm             label   "VEXpression"             export  all         }         parm {             name    "exportlist"             baseparm             label   "Attributes to Create"             export  none         }         parm {             name    "vex_strict"             baseparm             label   "Enforce Prototypes"             export  none         }     }      group {         name    "folder1_1"         label   "Bindings"          parm {             name    "autobind"             baseparm             label   "Autobind by Name"             export  none         }         multiparm {             name    "bindings"             label    "Number of Bindings"             baseparm             default 0             parmtag { "autoscope" "0000000000000000" }             parmtag { "multistartoffset" "1" }              parm {                 name    "bindname#"                 baseparm                 label   "Attribute Name"                 export  none             }             parm {                 name    "bindparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "groupautobind"             baseparm             label   "Autobind Groups by Name"             export  none         }         multiparm {             name    "groupbindings"             label    "Group Bindings"             baseparm             default 0             parmtag { "autoscope" "0000000000000000" }             parmtag { "multistartoffset" "1" }              parm {                 name    "bindgroupname#"                 baseparm                 label   "Group Name"                 export  none             }             parm {                 name    "bindgroupparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "vex_cwdpath"             baseparm             label   "Evaluation Node Path"             export  none         }         parm {             name    "vex_outputmask"             baseparm             label   "Export Parameters"             export  none         }         parm {             name    "vex_updatenmls"             baseparm             label   "Update Normals If Displaced"             export  none         }         parm {             name    "vex_matchattrib"             baseparm             label   "Attribute to Match"             export  none         }         parm {             name    "vex_inplace"             baseparm             label   "Compute Results In Place"             export  none         }         parm {             name    "vex_selectiongroup"             baseparm             label   "Output Selection Group"             export  none         }         parm {             name    "vex_precision"             baseparm             label   "VEX Precision"             export  none         }     }      parm {         name    "color_line"         label   "Color Line"         type    vector         size    3         default { "0" "0" "0" }         range   { 0 1 }     } ' $_obj_geo1_FrustumCameraOT_set_color_mask
opparm $_obj_geo1_FrustumCameraOT_set_color_mask  bindings ( 0 ) groupbindings ( 0 )
chblockbegin
chadd -t 0 0 $_obj_geo1_FrustumCameraOT_set_color_mask color_linex
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../colorgroupr")' $_obj_geo1_FrustumCameraOT_set_color_mask/color_linex
chadd -t 0 0 $_obj_geo1_FrustumCameraOT_set_color_mask color_liney
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../colorgroupg")' $_obj_geo1_FrustumCameraOT_set_color_mask/color_liney
chadd -t 0 0 $_obj_geo1_FrustumCameraOT_set_color_mask color_linez
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../colorgroupb")' $_obj_geo1_FrustumCameraOT_set_color_mask/color_linez
chblockend
opparm $_obj_geo1_FrustumCameraOT_set_color_mask group ( __in_frustum ) snippet ( '@Cd = chv(\'color_line\');' ) color_line ( color_linex color_liney color_linez )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_FrustumCameraOT_set_color_mask
opexprlanguage -s hscript $_obj_geo1_FrustumCameraOT_set_color_mask
opuserdata -n '___Version___' -v '' $_obj_geo1_FrustumCameraOT_set_color_mask

# Node $_obj_geo1_FrustumCameraOT_mask_attr (Sop/attribwrangle)
set _obj_geo1_FrustumCameraOT_mask_attr = `run("opadd -e -n -v attribwrangle mask_attr")`
oplocate -x `$arg2 + 6.5394415681357021` -y `$arg3 + 0.72349615692874902` $_obj_geo1_FrustumCameraOT_mask_attr
opparm $_obj_geo1_FrustumCameraOT_mask_attr  bindings ( 0 ) groupbindings ( 0 )
opparm $_obj_geo1_FrustumCameraOT_mask_attr group ( __in_frustum ) snippet ( '@mask=1;' )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_FrustumCameraOT_mask_attr
opexprlanguage -s hscript $_obj_geo1_FrustumCameraOT_mask_attr
opuserdata -n '___Version___' -v '' $_obj_geo1_FrustumCameraOT_mask_attr

# Node $_obj_geo1_FrustumCameraOT_promote_attr (Sop/attribpromote)
set _obj_geo1_FrustumCameraOT_promote_attr = `run("opadd -e -n -v attribpromote promote_attr")`
oplocate -x `$arg2 + 6.5389915681357014` -y `$arg3 + -0.31440384307125147` $_obj_geo1_FrustumCameraOT_promote_attr
chblockbegin
chadd -t 0 0 $_obj_geo1_FrustumCameraOT_promote_attr outclass
chkey -t 0 -v 2 -m 0 -a 0 -A 0 -T a  -F 'ch("../type")' $_obj_geo1_FrustumCameraOT_promote_attr/outclass
chblockend
opparm -V 19.0.383 $_obj_geo1_FrustumCameraOT_promote_attr inname ( mask ) outclass ( outclass )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_FrustumCameraOT_promote_attr
opexprlanguage -s hscript $_obj_geo1_FrustumCameraOT_promote_attr
opuserdata -n '___Version___' -v '19.0.383' $_obj_geo1_FrustumCameraOT_promote_attr

# Node $_obj_geo1_FrustumCameraOT_groupdelete_1 (Sop/groupdelete)
set _obj_geo1_FrustumCameraOT_groupdelete_1 = `run("opadd -e -n -v groupdelete groupdelete_1")`
oplocate -x `$arg2 + 1.2158515681357014` -y `$arg3 + -2.054843843071251` $_obj_geo1_FrustumCameraOT_groupdelete_1
opparm $_obj_geo1_FrustumCameraOT_groupdelete_1  deletions ( 1 )
opparm -V 19.0.383 $_obj_geo1_FrustumCameraOT_groupdelete_1 group1 ( __in_frustum )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_FrustumCameraOT_groupdelete_1
opexprlanguage -s hscript $_obj_geo1_FrustumCameraOT_groupdelete_1
opuserdata -n '___Version___' -v '19.0.383' $_obj_geo1_FrustumCameraOT_groupdelete_1

# Node $_obj_geo1_FrustumCameraOT_groupdelete_2 (Sop/groupdelete)
set _obj_geo1_FrustumCameraOT_groupdelete_2 = `run("opadd -e -n -v groupdelete groupdelete_2")`
oplocate -x `$arg2 + 3.7561615681357012` -y `$arg3 + -2.054843843071251` $_obj_geo1_FrustumCameraOT_groupdelete_2
opparm $_obj_geo1_FrustumCameraOT_groupdelete_2  deletions ( 1 )
opparm -V 19.0.383 $_obj_geo1_FrustumCameraOT_groupdelete_2 group1 ( __in_frustum )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_FrustumCameraOT_groupdelete_2
opexprlanguage -s hscript $_obj_geo1_FrustumCameraOT_groupdelete_2
opuserdata -n '___Version___' -v '19.0.383' $_obj_geo1_FrustumCameraOT_groupdelete_2

# Node $_obj_geo1_FrustumCameraOT_groupdelete_3 (Sop/groupdelete)
set _obj_geo1_FrustumCameraOT_groupdelete_3 = `run("opadd -e -n -v groupdelete groupdelete_3")`
oplocate -x `$arg2 + 6.5424415681357022` -y `$arg3 + -2.054843843071251` $_obj_geo1_FrustumCameraOT_groupdelete_3
opparm $_obj_geo1_FrustumCameraOT_groupdelete_3  deletions ( 1 )
opparm -V 19.0.383 $_obj_geo1_FrustumCameraOT_groupdelete_3 group1 ( __in_frustum )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_FrustumCameraOT_groupdelete_3
opexprlanguage -s hscript $_obj_geo1_FrustumCameraOT_groupdelete_3
opuserdata -n '___Version___' -v '19.0.383' $_obj_geo1_FrustumCameraOT_groupdelete_3

# Node $_obj_geo1_FrustumCameraOT_rename_mask (Sop/attribute)
set _obj_geo1_FrustumCameraOT_rename_mask = `run("opadd -e -n -v attribute rename_mask")`
oplocate -x `$arg2 + 6.5389915681357014` -y `$arg3 + -1.3144038430712515` $_obj_geo1_FrustumCameraOT_rename_mask
opparm $_obj_geo1_FrustumCameraOT_rename_mask  ptrenames ( 5 ) vtxrenames ( 5 ) primrenames ( 5 ) detailrenames ( 5 ) rmanconversions ( 5 )
opparm -V 19.0.383 $_obj_geo1_FrustumCameraOT_rename_mask frompt0 ( mask ) topt0 ( '`chs("../attname")`' ) fromvtx0 ( mask ) tovtx0 ( '`chs("../attname")`' ) frompr0 ( mask ) topr0 ( '`chs("../attname")`' )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_FrustumCameraOT_rename_mask
opexprlanguage -s hscript $_obj_geo1_FrustumCameraOT_rename_mask
opuserdata -n '___Version___' -v '19.0.383' $_obj_geo1_FrustumCameraOT_rename_mask

# Node $_obj_geo1_FrustumCameraOT_grouprename1 (Sop/grouprename)
set _obj_geo1_FrustumCameraOT_grouprename1 = `run("opadd -e -n -v grouprename grouprename1")`
oplocate -x `$arg2 + -0.88970843186429871` -y `$arg3 + 0.025556156928749019` $_obj_geo1_FrustumCameraOT_grouprename1
opparm $_obj_geo1_FrustumCameraOT_grouprename1  renames ( 1 )
opparm -V 19.0.383 $_obj_geo1_FrustumCameraOT_grouprename1 group1 ( __in_frustum ) newname1 ( '`chs("../groupname")`' )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_FrustumCameraOT_grouprename1
opexprlanguage -s hscript $_obj_geo1_FrustumCameraOT_grouprename1
opuserdata -n '___Version___' -v '19.0.383' $_obj_geo1_FrustumCameraOT_grouprename1

# Node $_obj_geo1_FrustumCameraOT_promote_to_del (Sop/grouppromote)
set _obj_geo1_FrustumCameraOT_promote_to_del = `run("opadd -e -n -v grouppromote promote_to_del")`
oplocate -x `$arg2 + 1.2158515681357014` -y `$arg3 + 0.93700615692874889` $_obj_geo1_FrustumCameraOT_promote_to_del
opparm $_obj_geo1_FrustumCameraOT_promote_to_del  promotions ( 1 )
chblockbegin
chadd -t 0 0 $_obj_geo1_FrustumCameraOT_promote_to_del totype1
chkey -t 0 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../typedel")' $_obj_geo1_FrustumCameraOT_promote_to_del/totype1
chblockend
opparm -V 19.0.383 $_obj_geo1_FrustumCameraOT_promote_to_del fromtype1 ( points ) totype1 ( totype1 ) group1 ( __in_frustum ) newname1 ( __in_frustum )
opset -d off -r off -h on -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_FrustumCameraOT_promote_to_del
opexprlanguage -s hscript $_obj_geo1_FrustumCameraOT_promote_to_del
opuserdata -n '___Version___' -v '19.0.383' $_obj_geo1_FrustumCameraOT_promote_to_del

# Node $_obj_geo1_FrustumCameraOT___in_frustum_cframe (Sop/groupcreate)
set _obj_geo1_FrustumCameraOT___in_frustum_cframe = `run("opadd -e -n -v groupcreate __in_frustum_cframe")`
oplocate -x `$arg2 + -3.4072484318642982` -y `$arg3 + 3.718241156928749` $_obj_geo1_FrustumCameraOT___in_frustum_cframe
opparm -V 19.0.383 $_obj_geo1_FrustumCameraOT___in_frustum_cframe groupname ( __in_frustum ) grouptype ( point ) groupbase ( off ) groupbounding ( on ) boundtype ( usebobject )
opset -d off -r off -h on -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_FrustumCameraOT___in_frustum_cframe
opexprlanguage -s hscript $_obj_geo1_FrustumCameraOT___in_frustum_cframe
opuserdata -n '___Version___' -v '19.0.383' $_obj_geo1_FrustumCameraOT___in_frustum_cframe

# Node $_obj_geo1_FrustumCameraOT_switch_current (Sop/switch)
set _obj_geo1_FrustumCameraOT_switch_current = `run("opadd -e -n -v switch switch_current")`
oplocate -x `$arg2 + 1.2158515588224712` -y `$arg3 + 2.4839561569287492` $_obj_geo1_FrustumCameraOT_switch_current
chblockbegin
chadd -t 0 0 $_obj_geo1_FrustumCameraOT_switch_current input
chkey -t 0 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../currentf")' $_obj_geo1_FrustumCameraOT_switch_current/input
chblockend
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_FrustumCameraOT_switch_current
opexprlanguage -s hscript $_obj_geo1_FrustumCameraOT_switch_current
opuserdata -n '___Version___' -v '19.0.383' $_obj_geo1_FrustumCameraOT_switch_current

# Node $_obj_geo1_FrustumCameraOT_get_frustums (Sop/trail)
set _obj_geo1_FrustumCameraOT_get_frustums = `run("opadd -e -n -v trail get_frustums")`
oplocate -x `$arg2 + 1.2158515681357014` -y `$arg3 + 8.0622261569287481` $_obj_geo1_FrustumCameraOT_get_frustums
chblockbegin
chadd -t 41.666666666666664 41.666666666666664 $_obj_geo1_FrustumCameraOT_get_frustums length
chkey -t 41.666666666666664 -v 2 -m 0 -a 0 -A 0 -T a  -F '(ch("../timestepy") - ch("../timestepx") + 1)' $_obj_geo1_FrustumCameraOT_get_frustums/length
chblockend
opparm -V 19.0.383 $_obj_geo1_FrustumCameraOT_get_frustums length ( length ) inc ( 4 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_FrustumCameraOT_get_frustums
opexprlanguage -s hscript $_obj_geo1_FrustumCameraOT_get_frustums
opuserdata -n '___Version___' -v '19.0.383' $_obj_geo1_FrustumCameraOT_get_frustums

# Node $_obj_geo1_FrustumCameraOT_wrap_frustum_seq (Sop/shrinkwrap::2.0)
set _obj_geo1_FrustumCameraOT_wrap_frustum_seq = `run("opadd -e -n -v shrinkwrap::2.0 wrap_frustum_seq")`
oplocate -x `$arg2 + 1.2158515681357014` -y `$arg3 + 5.8032261569287487` $_obj_geo1_FrustumCameraOT_wrap_frustum_seq
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_FrustumCameraOT_wrap_frustum_seq
opexprlanguage -s hscript $_obj_geo1_FrustumCameraOT_wrap_frustum_seq
opuserdata -n '___Version___' -v '19.0.383' $_obj_geo1_FrustumCameraOT_wrap_frustum_seq

# Node $_obj_geo1_FrustumCameraOT_to_last_frame (Sop/timeshift)
set _obj_geo1_FrustumCameraOT_to_last_frame = `run("opadd -e -n -v timeshift to_last_frame")`
oplocate -x `$arg2 + 1.2158515681357014` -y `$arg3 + 6.9327261569287488` $_obj_geo1_FrustumCameraOT_to_last_frame
chblockbegin
chadd -t 41.666666666666664 41.666666666666664 $_obj_geo1_FrustumCameraOT_to_last_frame frame
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../timestepy")' $_obj_geo1_FrustumCameraOT_to_last_frame/frame
chadd -t 41.666666666666664 41.666666666666664 $_obj_geo1_FrustumCameraOT_to_last_frame time
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F '$T' $_obj_geo1_FrustumCameraOT_to_last_frame/time
chadd -t 41.666666666666664 41.666666666666664 $_obj_geo1_FrustumCameraOT_to_last_frame frange1
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F '$FSTART' $_obj_geo1_FrustumCameraOT_to_last_frame/frange1
chadd -t 41.666666666666664 41.666666666666664 $_obj_geo1_FrustumCameraOT_to_last_frame frange2
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F '$FEND' $_obj_geo1_FrustumCameraOT_to_last_frame/frange2
chadd -t 41.666666666666664 41.666666666666664 $_obj_geo1_FrustumCameraOT_to_last_frame trange1
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F '$TSTART' $_obj_geo1_FrustumCameraOT_to_last_frame/trange1
chadd -t 41.666666666666664 41.666666666666664 $_obj_geo1_FrustumCameraOT_to_last_frame trange2
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F '$TEND' $_obj_geo1_FrustumCameraOT_to_last_frame/trange2
chblockend
opparm -V 19.0.383 $_obj_geo1_FrustumCameraOT_to_last_frame frame ( frame )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_FrustumCameraOT_to_last_frame
opexprlanguage -s hscript $_obj_geo1_FrustumCameraOT_to_last_frame
opuserdata -n '___Version___' -v '19.0.383' $_obj_geo1_FrustumCameraOT_to_last_frame

# Node $_obj_geo1_FrustumCameraOT_output (Sop/output)
set _obj_geo1_FrustumCameraOT_output = `run("opadd -e -n -v output output")`
oplocate -x `$arg2 + 1.2158515681356969` -y `$arg3 + -6.915235278547577` $_obj_geo1_FrustumCameraOT_output
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_FrustumCameraOT_output
opexprlanguage -s hscript $_obj_geo1_FrustumCameraOT_output
oporder -e clean_polys __in_frustum_SEQ __in_frustum set_first_frame source_frustum deform_frustum switch_vis_frustum draw_line set_color_line switch_mode cull_polys set_color_mask mask_attr promote_attr groupdelete_1 groupdelete_2 groupdelete_3 rename_mask grouprename1 promote_to_del __in_frustum_cframe switch_current get_frustums wrap_frustum_seq to_last_frame output 
opcf ..
opset -p on $_obj_geo1_FrustumCameraOT

opcf $arg1
opcf $_obj_geo1_FrustumCameraOT
opwire -n $_obj_geo1_FrustumCameraOT_cull_polys -0 $_obj_geo1_FrustumCameraOT_clean_polys
opwire -n $_obj_geo1_FrustumCameraOT___in_frustum -0 $_obj_geo1_FrustumCameraOT___in_frustum_SEQ
opwire -n $_obj_geo1_FrustumCameraOT_set_first_frame -1 $_obj_geo1_FrustumCameraOT___in_frustum_SEQ
opwire -n -i 0 -0 $_obj_geo1_FrustumCameraOT___in_frustum
opwire -n $_obj_geo1_FrustumCameraOT_wrap_frustum_seq -1 $_obj_geo1_FrustumCameraOT___in_frustum
opwire -n $_obj_geo1_FrustumCameraOT_deform_frustum -0 $_obj_geo1_FrustumCameraOT_set_first_frame
opwire -n $_obj_geo1_FrustumCameraOT_source_frustum -0 $_obj_geo1_FrustumCameraOT_deform_frustum
opwire -n $_obj_geo1_FrustumCameraOT_switch_mode -0 $_obj_geo1_FrustumCameraOT_switch_vis_frustum
opwire -n $_obj_geo1_FrustumCameraOT_set_color_line -1 $_obj_geo1_FrustumCameraOT_switch_vis_frustum
opwire -n $_obj_geo1_FrustumCameraOT_deform_frustum -0 $_obj_geo1_FrustumCameraOT_draw_line
opwire -n $_obj_geo1_FrustumCameraOT_draw_line -0 $_obj_geo1_FrustumCameraOT_set_color_line
opwire -n $_obj_geo1_FrustumCameraOT_grouprename1 -0 $_obj_geo1_FrustumCameraOT_switch_mode
opwire -n $_obj_geo1_FrustumCameraOT_groupdelete_1 -1 $_obj_geo1_FrustumCameraOT_switch_mode
opwire -n $_obj_geo1_FrustumCameraOT_groupdelete_2 -2 $_obj_geo1_FrustumCameraOT_switch_mode
opwire -n $_obj_geo1_FrustumCameraOT_groupdelete_3 -3 $_obj_geo1_FrustumCameraOT_switch_mode
opwire -n $_obj_geo1_FrustumCameraOT_promote_to_del -0 $_obj_geo1_FrustumCameraOT_cull_polys
opwire -n $_obj_geo1_FrustumCameraOT_switch_current -0 $_obj_geo1_FrustumCameraOT_set_color_mask
opwire -n $_obj_geo1_FrustumCameraOT_switch_current -0 $_obj_geo1_FrustumCameraOT_mask_attr
opwire -n $_obj_geo1_FrustumCameraOT_mask_attr -0 $_obj_geo1_FrustumCameraOT_promote_attr
opwire -n $_obj_geo1_FrustumCameraOT_clean_polys -0 $_obj_geo1_FrustumCameraOT_groupdelete_1
opwire -n $_obj_geo1_FrustumCameraOT_set_color_mask -0 $_obj_geo1_FrustumCameraOT_groupdelete_2
opwire -n $_obj_geo1_FrustumCameraOT_rename_mask -0 $_obj_geo1_FrustumCameraOT_groupdelete_3
opwire -n $_obj_geo1_FrustumCameraOT_promote_attr -0 $_obj_geo1_FrustumCameraOT_rename_mask
opwire -n $_obj_geo1_FrustumCameraOT_switch_current -0 $_obj_geo1_FrustumCameraOT_grouprename1
opwire -n $_obj_geo1_FrustumCameraOT_switch_current -0 $_obj_geo1_FrustumCameraOT_promote_to_del
opwire -n -i 0 -0 $_obj_geo1_FrustumCameraOT___in_frustum_cframe
opwire -n $_obj_geo1_FrustumCameraOT_deform_frustum -1 $_obj_geo1_FrustumCameraOT___in_frustum_cframe
opwire -n $_obj_geo1_FrustumCameraOT___in_frustum_SEQ -0 $_obj_geo1_FrustumCameraOT_switch_current
opwire -n $_obj_geo1_FrustumCameraOT___in_frustum_cframe -1 $_obj_geo1_FrustumCameraOT_switch_current
opwire -n $_obj_geo1_FrustumCameraOT_deform_frustum -0 $_obj_geo1_FrustumCameraOT_get_frustums
opwire -n $_obj_geo1_FrustumCameraOT_to_last_frame -0 $_obj_geo1_FrustumCameraOT_wrap_frustum_seq
opwire -n $_obj_geo1_FrustumCameraOT_get_frustums -0 $_obj_geo1_FrustumCameraOT_to_last_frame
opwire -n $_obj_geo1_FrustumCameraOT_switch_vis_frustum -0 $_obj_geo1_FrustumCameraOT_output
opcf ..

set oidx = 0
if ($argc >= 9 && "$arg9" != "") then
    set oidx = $arg9
endif

if ($argc >= 5 && "$arg4" != "") then
    set output = $_obj_geo1_FrustumCameraOT
    opwire -n $output -$arg5 $arg4
endif
if ($argc >= 6 && "$arg6" != "") then
    set input = $_obj_geo1_FrustumCameraOT
    if ($arg8) then
        opwire -n -i $arg6 -0 $input
    else
        opwire -n -o $oidx $arg6 -0 $input
    endif
endif
opcf $saved_path
'''
hou.hscript(h_preamble + h_extra_args + h_cmd)
