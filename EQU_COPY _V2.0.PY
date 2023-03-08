# COPYRIGHT BY JOHNY

import KcsPoint3D
import KcsPoint2D
import KcsStat_point3D_req
import kcs_ui
import kcs_util
import kcs_dex
import kcs_equip
import sys
import kcs_draft
import KcsVector3D
import KcsStringlist
import KcsElementHandle
import KcsModel
import KcsRectangle2D
import KcsVector2D
import KcsModelDrawAssyCriteria
import KcsTransformation3D

def receive_proj_name():
    proj_name=kcs_util.TB_environment_get('SB_PROJ')
    return proj_name



def receive_equip_cord(model_name):
    proj_name=receive_proj_name()
    st1 = "EQUIPMENT(\'" + proj_name +"').ITEM(\'"
    st2 = "\').REF.POINT"
    st3 = model_name
    st = st1 + st3 + st2
    # kcs_ui.message_confirm(" '%s' " %st)
    if kcs_dex.extract(st) == 0:  # was extraction successful?
        # kcs_ui.message_confirm(""+st)
        if kcs_dex.next_result() == 4:  # is a string-type data available?
            comp = kcs_dex.get_reavec3d()

            return comp


def receive_equip_compname(model_name):
    proj_name=receive_proj_name()
    st1 = "EQUIPMENT(\'" + proj_name +"').ITEM(\'"
    st2 = "\').COMP_NAME"
    st3 = model_name
    st = st1 + st3 + st2
    # kcs_ui.message_confirm(" '%s' " %st)
    if kcs_dex.extract(st) == 0:  # was extraction successful?
        # kcs_ui.message_confirm(""+st)
        if kcs_dex.next_result() == 3:  # is a string-type data available?
            comp = kcs_dex.get_string()
            return comp


def prompt_process():
    res = kcs_ui.int_req("input the transform distance")
    if res[0] == kcs_util.ok():  # Has the user provided the value?
        distance = res[1]
        return distance


def PresentModelInformation(model, mark):
    model_name = model.Name
    #kcs_ui.message_confirm(" '%s' " %model_name)
    proj_name=receive_proj_name()
    proj_name1=proj_name + "-"
    model_name = model_name.replace(proj_name1,"")
    #kcs_ui.message_confirm(" '%s' " % model_name)
    #kcs_equip.equip_cancel()
    kcs_equip.equip_activate(model_name)

    module_name = kcs_equip.equip_module_get()

    # kcs_ui.message_confirm("module name is '%s'" % module_name)

    comp_name = receive_equip_compname(model_name)
    equ_cord = receive_equip_cord(model_name)
    # kcs_ui.message_confirm("comp name is '%s'" % comp_name)
    kcs_equip.equip_cancel()
    
    res = kcs_ui.string_req("input new equipment name")
    if res[0] == kcs_util.ok():  # Has the user provided the value?
        new_equipname = res[1]
        if (kcs_equip.equip_exist(new_equipname)):
            kcs_ui.message_confirm("the equip_name is exist!")
            kcs_draft.highlight_off(0)
            return
        # kcs_ui.message_confirm("ok1")
        kcs_equip.equip_new(new_equipname, module_name)
        # kcs_equip.equip_activate(new_equipname)
        kcs_equip.equip_component_set(comp_name)

        kcs_equip.equip_save()
        # kcs_ui.message_confirm("new equipment '%s' is created " % new_equipname)
        kcs_equip.equip_activate(new_equipname)
        point = KcsPoint3D.Point3D(equ_cord[0], equ_cord[1], equ_cord[2])

        vector1 = KcsVector3D.Vector3D(1.0, 0.0, 0.0)
        vector2 = KcsVector3D.Vector3D(0.0, 1.0, 0.0)

        kcs_equip.equip_place(point, vector1, vector2)
        kcs_equip.equip_save()
        kcs_equip.equip_activate(new_equipname)
        if (mark == 1):
            transVector = KcsVector3D.Vector3D(100, 100, 0)
        elif (mark == 2):
            distance = prompt_process()
            transVector = KcsVector3D.Vector3D(distance, 0, 0)
        elif (mark == 3):
            distance = prompt_process()
            transVector = KcsVector3D.Vector3D(0, distance, 0)
        elif (mark == 4):
            distance = prompt_process()
            transVector = KcsVector3D.Vector3D(0, 0, distance)
        transformation = KcsTransformation3D.Transformation3D()
        transformation.Translate(transVector)
        kcs_equip.equip_transform(transformation)
        # kcs_ui.message_confirm("Equipment: " + new_equipname + " has been placed OK.")
        kcs_equip.equip_save()
        model = KcsModel.Model("equipment", proj_name + "-" + new_equipname)
        # kcs_ui.message_confirm("ok1")

        kcs_draft.model_draw(model)
        kcs_draft.highlight_off(0)
    else :
        kcs_draft.highlight_off(0)


def PresentModelInformation1(model):
    proj_name=receive_proj_name()
    model_name = model.Name
    # kcs_ui.message_confirm(" '%s' " %model_name)
    proj_name1=proj_name + "-"
    model_name = model_name.replace(proj_name1,"")
    # kcs_ui.message_confirm(" '%s' " % model_name)
    # kcs_equip.equip_cancel()
    kcs_equip.equip_activate(model_name)

    module_name = kcs_equip.equip_module_get()

    # kcs_ui.message_confirm("module name is '%s'" % module_name)

    comp_name = receive_equip_compname(model_name)
    equ_cord = receive_equip_cord(model_name)
    # kcs_ui.message_confirm("comp name is '%s'" % comp_name)
    kcs_equip.equip_cancel()
    res = kcs_ui.string_req("input new equipment name ",model_name)
    if res[0] == kcs_util.ok():  # Has the user provided the value?
        new_equipname = res[1]
        if (kcs_equip.equip_exist(new_equipname)):
            kcs_ui.message_confirm("the equip_name is exist!")
            kcs_draft.highlight_off(0)
            return
        # kcs_ui.message_confirm("ok1")
        kcs_equip.equip_new(new_equipname, module_name)
        # kcs_equip.equip_activate(new_equipname)
        kcs_equip.equip_component_set(comp_name)

        kcs_equip.equip_save()
        # kcs_ui.message_confirm("new equipment '%s' is created " % new_equipname)
        kcs_equip.equip_activate(new_equipname)
        point = KcsPoint3D.Point3D(equ_cord[0], equ_cord[1], equ_cord[2])

        vector1 = KcsVector3D.Vector3D(1.0, 0.0, 0.0)
        vector2 = KcsVector3D.Vector3D(0.0, 1.0, 0.0)

        kcs_equip.equip_place(point, vector1, vector2)
        kcs_equip.equip_save()

        model = KcsModel.Model("equipment", proj_name + "-" + new_equipname)
        # kcs_ui.message_confirm("ok1")

        kcs_draft.model_draw(model)
        kcs_equip.equip_delete(model_name)
        kcs_draft.highlight_off(0)
    else:
        kcs_draft.highlight_off(0)





def SelectModel():  # select model

    point = KcsPoint2D.Point2D()

    try:
        prompt = 'Indicate component, OC to exit'
        resp = kcs_ui.point2D_req(prompt, point)  # request user for point
        # if resp[0] == kcs_util.ok():
        try:
            handle = kcs_draft.component_identify(point)  # component
            kcs_ui.message_noconfirm('indicated component: ' + str(handle))
            kcs_draft.element_highlight(handle)
            return handle
        except:
            kcs_ui.message_noconfirm('component not found')
    except:
        print
        kcs_ui.error
    return KcsElementHandle.ElementHandle()


try:  # main
    # build actions list
    actions = KcsStringlist.Stringlist('add new equipment')
    actions.AddString("X-Transform ")
    actions.AddString("Y-Transform")
    actions.AddString("Z-Transform")
    actions.AddString("modify equip_name")
    model = KcsModel.Model()


    try:
        while 1:
            res = kcs_ui.choice_select('plcae equipment', 'v2.0', actions)
            if (res[0] == kcs_util.cancel()):
                break
                kcs_util.exit_function()
            # if res[0] == kcs_util.ok():
            if res[1] == 1:  
                # while 1:
                modhandle = SelectModel()
                try:
                    model = kcs_draft.model_properties_get(modhandle, model)
                    PresentModelInformation(model, 1)

                except:
                    print
                    sys.exc_info()[1]
                    PrintDraftError()

            if res[1] == 2:  
                # while 1:
                modhandle = SelectModel()
                try:
                    model = kcs_draft.model_properties_get(modhandle, model)
                    PresentModelInformation(model, 2)

                except:
                    print
                    sys.exc_info()[1]
                    PrintDraftError()

            if res[1] == 3:  
                # while 1:
                modhandle = SelectModel()
                try:
                    model = kcs_draft.model_properties_get(modhandle, model)
                    PresentModelInformation(model, 3)

                except:
                    print
                    sys.exc_info()[1]
                    PrintDraftError()

            if res[1] == 4:  
                # while 1:
                modhandle = SelectModel()
                try:
                    model = kcs_draft.model_properties_get(modhandle, model)
                    PresentModelInformation(model,4)

                except:
                    print
                    sys.exc_info()[1]
                    PrintDraftError()

            if res[1] == 5:  
                # while 1:
                modhandle = SelectModel()
                try:
                    model = kcs_draft.model_properties_get(modhandle, model)
                    PresentModelInformation1(model)

                except:
                    print
                    sys.exc_info()[1]
                    PrintDraftError()

   
    except:
        print
        sys.exc_info()[1]
        PrintDraftError()
        kcs_ui.message_noconfirm('Script interrupted')

except:
    print
    sys.exc_info()[1]
