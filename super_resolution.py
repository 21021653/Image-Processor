import cv2

def super_resolve(image_path, model_name):
    sr = cv2.dnn_superres.DnnSuperResImpl_create()

    if model_name == "EDSR":
        model_path = "C:/Users/vvu04/Downloads/EDSR_x4.pb"
        sr.readModel(model_path)
        sr.setModel("edsr", 4)
    elif model_name == "ESPCN":
        model_path = "C:/Users/vvu04/Downloads/ESPCN_x4.pb"
        sr.readModel(model_path)
        sr.setModel("espcn", 4)
    elif model_name == "FSRCNN":
        model_path = "C:/Users/vvu04/Downloads/FSRCNN_x4.pb"
        sr.readModel(model_path)
        sr.setModel("fsrcnn", 4)
    elif model_name == "LAPSRN":
        model_path = "C:/Users/vvu04/Downloads/LAPSRN_x8.pb"
        sr.readModel(model_path)
        sr.setModel("lapsrn", 8)

    inp = cv2.imread(image_path)
    out = sr.upsample(inp)

    return out
