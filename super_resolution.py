import cv2

def super_resolve(image_path, model_name):
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    inp = cv2.imread(image_path)
    if model_name == "EDSR_x3":
        model_path = "models/EDSR_x3.pb"
        sr.readModel(model_path)
        sr.setModel("edsr", 3)
        out = sr.upsample(inp)
    elif model_name == "EDSR_x4":
        model_path = "models/EDSR_x4.pb"
        sr.readModel(model_path)
        sr.setModel("edsr", 4)
        out = sr.upsample(inp)
    elif model_name == "ESPCN_x3":
        model_path = "models/ESPCN_x3.pb"
        sr.readModel(model_path)
        sr.setModel("espcn", 3)
        out = sr.upsample(inp)
    elif model_name == "ESPCN_x4":
        model_path = "models/ESPCN_x4.pb"
        sr.readModel(model_path)
        sr.setModel("espcn", 4)
        out = sr.upsample(inp)
    elif model_name == "FSRCNN_x4":
        model_path = "models/FSRCNN_x4.pb"
        sr.readModel(model_path)
        sr.setModel("fsrcnn", 4)
        out = sr.upsample(inp)
    elif model_name == "LAPSRN_x4":
        model_path = "models/LAPSRN_x4.pb"
        sr.readModel(model_path)
        sr.setModel("lapsrn", 4)
        out = sr.upsample(inp)
    elif model_name == "Bicubic_x3":
        out = cv2.resize(inp, (int(inp.shape[1]*3), int(inp.shape[0]*3)), interpolation=cv2.INTER_CUBIC)
    elif model_name == "Bicubic_x4":
        out = cv2.resize(inp, (int(inp.shape[1]*4), int(inp.shape[0]*4)), interpolation=cv2.INTER_CUBIC)
    elif model_name == "Lanczos_x3":
        out = cv2.resize(inp, (int(inp.shape[1]*3), int(inp.shape[0]*3)), interpolation=cv2.INTER_LANCZOS4)
    elif model_name == "Lanczos_x4":
        out = cv2.resize(inp, (int(inp.shape[1]*4), int(inp.shape[0]*4)), interpolation=cv2.INTER_LANCZOS4)
    
    return out

