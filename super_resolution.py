import cv2

def super_resolve(image_path, model_name):
    sr = cv2.dnn_superres.DnnSuperResImpl_create()

    if model_name == "EDSR_x3":
        model_path = "models/EDSR_x3.pb"
        sr.readModel(model_path)
        sr.setModel("edsr", 3)
    elif model_name == "EDSR_x4":
        model_path = "models/EDSR_x4.pb"
        sr.readModel(model_path)
        sr.setModel("edsr", 4)
    elif model_name == "ESPCN_x3":
        model_path = "models/ESPCN_x3.pb"
        sr.readModel(model_path)
        sr.setModel("espcn", 3)
    elif model_name == "ESPCN_x4":
        model_path = "models/ESPCN_x4.pb"
        sr.readModel(model_path)
        sr.setModel("espcn", 4)
    elif model_name == "FSRCNN_x4":
        model_path = "models/FSRCNN_x4.pb"
        sr.readModel(model_path)
        sr.setModel("fsrcnn", 4)
    elif model_name == "LAPSRN_x4":
        model_path = "models/LAPSRN_x4.pb"
        sr.readModel(model_path)
        sr.setModel("lapsrn", 4)

    inp = cv2.imread(image_path)
    out = sr.upsample(inp)

    return out

